from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings
from app.features.auth.models import Invitation, RefreshSession, User, Workspace
from app.features.auth.schemas import (
    AuthResponse,
    InvitationAcceptRequest,
    InvitationCreateRequest,
    InvitationListResponse,
    InvitationResponse,
    InvitationTokenResponse,
    InvitationUpdateRoleRequest,
    InitTelegramVerificationRequest,
    InitTelegramVerificationResponse,
    INVITER_ROLES,
    LoginRequest,
    RoleDescription,
    RegisterWorkspaceRequest,
    SessionResponse,
    TelegramIntentRequest,
    TelegramCheckRequest,
    UserResponse,
    VerifyTelegramCodeRequest,
    VerifyTelegramCodeResponse,
    WorkspaceResponse,
)
from app.features.auth.security import (
    create_access_token,
    create_invite_token,
    create_refresh_token,
    hash_invite_token,
    hash_password,
    hash_refresh_token,
    normalize_phone,
    verify_password,
)
from app.features.auth.telegram_client import TelegramVerificationClient


class AuthService:
    def __init__(self, settings: Settings, telegram_client: TelegramVerificationClient) -> None:
        self._settings = settings
        self._telegram_client = telegram_client

    async def login(self, session: AsyncSession, payload: LoginRequest) -> AuthResponse:
        statement = select(User).where(User.email == payload.email.lower())
        user = await session.scalar(statement)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        user.last_login = datetime.now(UTC)
        await session.commit()
        await session.refresh(user)
        await session.refresh(user, attribute_names=["workspace"])
        return self._build_auth_response(user)

    async def init_telegram_verification(
        self,
        session: AsyncSession,
        payload: InitTelegramVerificationRequest,
    ) -> InitTelegramVerificationResponse:
        normalized_phone = normalize_phone(payload.phone_number)
        existing_user = await session.scalar(select(User).where(User.phone_number == normalized_phone))
        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone number already exists")

        verification = await self._telegram_client.create_intent(
            payload=self._build_intent_request(payload.phone_number)
        )
        return InitTelegramVerificationResponse(
            bot_url=verification.bot_url,
            expires_at=verification.expires_at,
        )

    async def verify_telegram_code(
        self,
        payload: VerifyTelegramCodeRequest,
    ) -> VerifyTelegramCodeResponse:
        result = await self._telegram_client.check_code(
            TelegramCheckRequest(phone_number=normalize_phone(payload.phone_number), code=payload.code)
        )
        return VerifyTelegramCodeResponse(
            verified=result.verified,
            status=result.status,
            expires_at=result.expires_at,
        )

    async def register_workspace(
        self,
        session: AsyncSession,
        payload: RegisterWorkspaceRequest,
    ) -> AuthResponse:
        normalized_email = payload.email.lower()
        normalized_phone = normalize_phone(payload.phone_number)

        await self._ensure_unique_user(session, normalized_email, normalized_phone)
        verification = await self.verify_telegram_code(
            VerifyTelegramCodeRequest(phone_number=normalized_phone, code=payload.telegram_code)
        )
        if not verification.verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Telegram verification failed: {verification.status}",
            )

        workspace = Workspace(
            company_name=payload.company_name.strip(),
            business_direction=payload.business_direction,
            usage_purpose=payload.usage_purpose,
            team_size=payload.team_size,
            has_team=payload.additional_boolean_question,
        )
        user = User(
            workspace=workspace,
            email=normalized_email,
            hashed_password=hash_password(payload.password),
            phone_number=normalized_phone,
            role_description=RoleDescription.ADMIN_OWNER,
            is_verified=True,
            last_login=datetime.now(UTC),
        )
        session.add_all([workspace, user])
        await session.flush()

        invitations = self._build_invitations(payload.invited_members, workspace.id, user.id)
        if invitations:
            session.add_all(invitations)

        await session.commit()
        await session.refresh(user)
        await session.refresh(user, attribute_names=["workspace"])
        return self._build_auth_response(user)

    async def create_refresh_session(
        self,
        session: AsyncSession,
        user: User,
        request: Request,
        remember_me: bool = True,
    ) -> str:
        raw_token = create_refresh_token(remember_me=remember_me)
        token_hash = hash_refresh_token(raw_token)
        refresh_session = RefreshSession(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(UTC) + timedelta(seconds=self._settings.refresh_token_ttl_seconds),
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None,
        )
        session.add(refresh_session)
        await session.commit()
        return raw_token

    async def rotate_refresh_token(
        self,
        session: AsyncSession,
        refresh_token: str,
        request: Request,
    ) -> tuple[AuthResponse, str]:
        refresh_session = await self._get_valid_refresh_session(session, refresh_token)
        
        is_persistent = not refresh_token.startswith("sm.")
        new_token = create_refresh_token(remember_me=is_persistent)
        refresh_session.rotation_counter += 1
        refresh_session.last_used_at = datetime.now(UTC)
        refresh_session.token_hash = hash_refresh_token(new_token)
        refresh_session.expires_at = datetime.now(UTC) + timedelta(seconds=self._settings.refresh_token_ttl_seconds)
        refresh_session.user_agent = request.headers.get("user-agent")
        refresh_session.ip_address = request.client.host if request.client else None
        await session.commit()

        user = await session.get(User, refresh_session.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is invalid")

        await session.refresh(user, attribute_names=["workspace"])
        return self._build_auth_response(user), new_token

    async def get_session(self, session: AsyncSession, user_id: str) -> SessionResponse:
        user = await session.get(User, user_id)
        if user is None:
            return SessionResponse(authenticated=False)

        await session.refresh(user, attribute_names=["workspace"])
        auth = self._build_auth_response(user)
        return SessionResponse(authenticated=True, user=auth.user, workspace=auth.workspace)

    async def logout(self, session: AsyncSession, refresh_token: str | None) -> None:
        if not refresh_token:
            return

        refresh_session = await session.scalar(
            select(RefreshSession).where(RefreshSession.token_hash == hash_refresh_token(refresh_token))
        )
        if refresh_session is None:
            return

        refresh_session.revoked_at = datetime.now(UTC)
        await session.commit()

    async def validate_active_session(
        self,
        session: AsyncSession,
        refresh_token: str | None,
        user_id: str,
    ) -> None:
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        refresh_session = await self._get_valid_refresh_session(session, refresh_token)
        if refresh_session.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is invalid")

    async def create_invitation(
        self,
        session: AsyncSession,
        actor: User,
        payload: InvitationCreateRequest,
    ) -> InvitationTokenResponse:
        self._ensure_inviter_role(actor.role_description)
        invite_email = payload.email.lower()

        duplicate_user = await session.scalar(
            select(User).where(User.workspace_id == actor.workspace_id, User.email == invite_email)
        )
        if duplicate_user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already in workspace")

        duplicate_invite = await session.scalar(
            select(Invitation).where(
                Invitation.workspace_id == actor.workspace_id,
                Invitation.email == invite_email,
                Invitation.status == "pending",
                Invitation.revoked_at.is_(None),
            )
        )
        if duplicate_invite is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pending invitation already exists")

        token = create_invite_token()
        invitation = Invitation(
            workspace_id=actor.workspace_id,
            email=invite_email,
            invited_by_user_id=actor.id,
            role_description=payload.role_description,
            token_hash=hash_invite_token(token),
            status="pending",
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )
        session.add(invitation)
        await session.commit()
        await session.refresh(invitation)
        return InvitationTokenResponse(invitation=self._map_invitation(invitation), token=token)

    async def list_invitations(self, session: AsyncSession, actor: User) -> InvitationListResponse:
        self._ensure_inviter_role(actor.role_description)
        items = await session.scalars(
            select(Invitation)
            .where(Invitation.workspace_id == actor.workspace_id)
            .order_by(Invitation.created_at.desc())
        )
        return InvitationListResponse(items=[self._map_invitation(item) for item in items.all()])

    async def resend_invitation(
        self,
        session: AsyncSession,
        actor: User,
        invitation_id: str,
    ) -> InvitationTokenResponse:
        self._ensure_inviter_role(actor.role_description)
        invitation = await self._get_workspace_invitation(session, actor.workspace_id, invitation_id)
        self._assert_pending_invitation(invitation)
        token = create_invite_token()
        invitation.token_hash = hash_invite_token(token)
        invitation.resent_at = datetime.now(UTC)
        invitation.expires_at = datetime.now(UTC) + timedelta(days=7)
        await session.commit()
        await session.refresh(invitation)
        return InvitationTokenResponse(invitation=self._map_invitation(invitation), token=token)

    async def revoke_invitation(self, session: AsyncSession, actor: User, invitation_id: str) -> None:
        self._ensure_inviter_role(actor.role_description)
        invitation = await self._get_workspace_invitation(session, actor.workspace_id, invitation_id)
        self._assert_pending_invitation(invitation)
        invitation.status = "revoked"
        invitation.revoked_at = datetime.now(UTC)
        await session.commit()

    async def update_invitation_role(
        self,
        session: AsyncSession,
        actor: User,
        invitation_id: str,
        payload: InvitationUpdateRoleRequest,
    ) -> InvitationResponse:
        self._ensure_inviter_role(actor.role_description)
        invitation = await self._get_workspace_invitation(session, actor.workspace_id, invitation_id)
        self._assert_pending_invitation(invitation)
        invitation.role_description = payload.role_description
        await session.commit()
        await session.refresh(invitation)
        return self._map_invitation(invitation)

    async def accept_invitation(
        self,
        session: AsyncSession,
        payload: InvitationAcceptRequest,
    ) -> AuthResponse:
        invitation = await session.scalar(
            select(Invitation).where(Invitation.token_hash == hash_invite_token(payload.token))
        )
        if invitation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")

        self._assert_pending_invitation(invitation)

        if self._is_expired(invitation.expires_at):
            invitation.status = "expired"
            await session.commit()
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="Invitation expired")

        existing_user = await session.scalar(select(User).where(User.email == invitation.email))
        if existing_user is not None and existing_user.workspace_id == invitation.workspace_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already in workspace")

        if existing_user is not None and existing_user.workspace_id != invitation.workspace_id:
            if not payload.transfer_confirmed:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Transfer confirmation required",
                )
            existing_user.workspace_id = invitation.workspace_id
            existing_user.role_description = invitation.role_description
            existing_user.last_login = datetime.now(UTC)
            target_user = existing_user
        else:
            target_user = User(
                workspace_id=invitation.workspace_id,
                email=invitation.email,
                hashed_password=hash_password(create_invite_token()),
                phone_number=self._generate_invited_phone(),
                role_description=invitation.role_description,
                is_verified=True,
                last_login=datetime.now(UTC),
            )
            session.add(target_user)

        invitation.status = "accepted"
        invitation.accepted_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(target_user)
        await session.refresh(target_user, attribute_names=["workspace"])
        return self._build_auth_response(target_user)

    def build_access_token(self, user: User) -> str:
        return create_access_token(
            settings=self._settings,
            subject=user.id,
            workspace_id=user.workspace_id,
            role=user.role_description,
        )

    def cookie_settings(self) -> dict[str, object]:
        return {
            "httponly": True,
            "secure": self._settings.cookie_secure,
            "samesite": "lax",
            "domain": self._settings.cookie_domain,
            "path": "/",
        }

    def _build_auth_response(self, user: User) -> AuthResponse:
        workspace = user.workspace
        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                phone_number=user.phone_number,
                role_description=self._canonical_role(user.role_description),
                is_verified=user.is_verified,
                workspace_id=user.workspace_id,
            ),
            workspace=WorkspaceResponse(
                id=workspace.id,
                company_name=workspace.company_name,
                business_direction=workspace.business_direction,
                usage_purpose=workspace.usage_purpose,
                team_size=workspace.team_size,
                has_team=workspace.has_team,
            ),
        )

    def _build_invitations(self, invited_members: list[str], workspace_id: str, user_id: str) -> list[Invitation]:
        unique_emails = {email.lower().strip() for email in invited_members if email.strip()}
        return [
            Invitation(
                workspace_id=workspace_id,
                email=email,
                invited_by_user_id=user_id,
                role_description=RoleDescription.TEAM_MEMBER,
                token_hash=hash_invite_token(create_invite_token()),
                status="pending",
                expires_at=datetime.now(UTC) + timedelta(days=7),
            )
            for email in sorted(unique_emails)
        ]

    def _map_invitation(self, invitation: Invitation) -> InvitationResponse:
        return InvitationResponse(
            id=invitation.id,
            workspace_id=invitation.workspace_id,
            email=invitation.email,
            invited_by_user_id=invitation.invited_by_user_id,
            role_description=RoleDescription(invitation.role_description),
            status=invitation.status,
            expires_at=invitation.expires_at,
            accepted_at=invitation.accepted_at,
            revoked_at=invitation.revoked_at,
            created_at=invitation.created_at,
        )

    def _ensure_inviter_role(self, role: str) -> None:
        if role not in {value.value for value in INVITER_ROLES}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    def _canonical_role(self, role: str) -> RoleDescription:
        try:
            return RoleDescription(role)
        except ValueError:
            return RoleDescription.TEAM_MEMBER

    async def _get_workspace_invitation(
        self,
        session: AsyncSession,
        workspace_id: str,
        invitation_id: str,
    ) -> Invitation:
        invitation = await session.scalar(
            select(Invitation).where(
                Invitation.id == invitation_id,
                Invitation.workspace_id == workspace_id,
            )
        )
        if invitation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")
        return invitation

    def _assert_pending_invitation(self, invitation: Invitation) -> None:
        if invitation.status != "pending" or invitation.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation is not pending")

    def _generate_invited_phone(self) -> str:
        digits = "".join(char for char in uuid4().hex if char.isdigit())
        return f"+1{(digits + '0' * 11)[:11]}"

    def _is_expired(self, value: datetime) -> bool:
        check = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
        return check < datetime.now(UTC)

    def _build_intent_request(self, phone_number: str) -> TelegramIntentRequest:
        return TelegramIntentRequest(phone_number=normalize_phone(phone_number))

    async def _ensure_unique_user(self, session: AsyncSession, email: str, phone_number: str) -> None:
        existing_user = await session.scalar(
            select(User).where((User.email == email) | (User.phone_number == phone_number))
        )
        if existing_user is None:
            return

        if existing_user.email == email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone number already exists")

    async def _get_valid_refresh_session(
        self,
        session: AsyncSession,
        refresh_token: str,
    ) -> RefreshSession:
        refresh_session = await session.scalar(
            select(RefreshSession).where(RefreshSession.token_hash == hash_refresh_token(refresh_token))
        )
        if refresh_session is None or refresh_session.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh session is invalid")

        if self._is_expired(refresh_session.expires_at):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh session expired")

        return refresh_session