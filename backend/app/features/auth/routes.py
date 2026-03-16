from dataclasses import dataclass

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings, get_settings
from app.db.session import get_db_session
from app.features.auth.models import User
from app.features.auth.schemas import (
    AuthResponse,
    InitTelegramVerificationRequest,
    InitTelegramVerificationResponse,
    LoginRequest,
    RegisterWorkspaceRequest,
    SessionResponse,
    VerifyTelegramCodeRequest,
    VerifyTelegramCodeResponse,
)
from app.features.auth.security import decode_access_token
from app.features.auth.service import AuthService
from app.features.auth.telegram_client import TelegramVerificationClient

router = APIRouter()
settings = get_settings()


@dataclass(frozen=True)
class AuthContext:
    user_id: str
    workspace_id: str


def get_auth_service(settings_: Settings = Depends(get_settings)) -> AuthService:
    return AuthService(settings=settings_, telegram_client=TelegramVerificationClient(settings_))


async def get_current_auth_context(
    access_token: str | None = Cookie(default=None, alias="access_token"),
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    settings_: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthContext:
    if not access_token or not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_access_token(access_token, settings_)
    except Exception as error: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session") from error

    user_id = payload.get("sub")
    workspace_id = payload.get("workspace_id")
    if not user_id or not workspace_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    await auth_service.validate_active_session(session, refresh_token, user_id)

    return AuthContext(user_id=str(user_id), workspace_id=str(workspace_id))


async def get_current_user_id(auth_context: AuthContext = Depends(get_current_auth_context)) -> str:
    return auth_context.user_id


def set_auth_cookies(response: Response, auth_service: AuthService, access_token: str, refresh_token: str) -> None:
    cookie_settings = auth_service.cookie_settings()
    
    is_persistent = not refresh_token.startswith("sm.")
    refresh_max_age = settings.refresh_token_ttl_seconds if is_persistent else None

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.access_token_ttl_seconds,
        **cookie_settings,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=refresh_max_age,
        **cookie_settings,
    )


def clear_auth_cookies(response: Response, auth_service: AuthService) -> None:
    cookie_settings = auth_service.cookie_settings()
    response.delete_cookie(key="access_token", **cookie_settings)
    response.delete_cookie(key="refresh_token", **cookie_settings)


@router.post("/login", response_model=AuthResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    auth_response = await auth_service.login(session, payload)
    user_record = await session.get(User, auth_response.user.id)
    if user_record is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    refresh_token = await auth_service.create_refresh_session(session, user_record, request, payload.remember_me)
    access_token = auth_service.build_access_token(user_record)
    set_auth_cookies(response, auth_service, access_token, refresh_token)
    return auth_response


@router.post(
    "/init-telegram-verification",
    response_model=InitTelegramVerificationResponse,
)
async def init_telegram_verification(
    payload: InitTelegramVerificationRequest,
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> InitTelegramVerificationResponse:
    return await auth_service.init_telegram_verification(session, payload)


@router.post("/verify-telegram-code", response_model=VerifyTelegramCodeResponse)
async def verify_telegram_code(
    payload: VerifyTelegramCodeRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> VerifyTelegramCodeResponse:
    return await auth_service.verify_telegram_code(payload)


@router.post("/register-workspace", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_workspace(
    payload: RegisterWorkspaceRequest,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    auth_response = await auth_service.register_workspace(session, payload)
    user_record = await session.get(User, auth_response.user.id)
    if user_record is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Registration failed")
    refresh_token = await auth_service.create_refresh_session(session, user_record, request)
    access_token = auth_service.build_access_token(user_record)
    set_auth_cookies(response, auth_service, access_token, refresh_token)
    return auth_response


@router.post("/refresh", response_model=AuthResponse)
async def refresh_session(
    response: Response,
    request: Request,
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    auth_response, new_refresh_token = await auth_service.rotate_refresh_token(session, refresh_token, request)
    user_record = await session.get(User, auth_response.user.id)
    if user_record is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    access_token = auth_service.build_access_token(user_record)
    set_auth_cookies(response, auth_service, access_token, new_refresh_token)
    return auth_response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    await auth_service.logout(session, refresh_token)
    clear_auth_cookies(response, auth_service)
    return response


@router.get("/me", response_model=SessionResponse)
async def me(
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> SessionResponse:
    return await auth_service.get_session(session, user_id)


@router.get("/validate-token", status_code=status.HTTP_200_OK)
async def validate_token(
    response: Response,
    auth_context: AuthContext = Depends(get_current_auth_context),
) -> dict[str, str]:
    """
    Internal endpoint for the API Gateway to validate cookies via auth_request.
    Returns 200 OK and injects identity headers if valid.
    """
    response.headers["X-User-Id"] = auth_context.user_id
    response.headers["X-Workspace-Id"] = auth_context.workspace_id
    return {"status": "ok"}

