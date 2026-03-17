from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from app.features.auth.models import Invitation, User, Workspace
from app.features.auth.security import hash_password


async def _seed_workspace_user(
    db_session_factory,
    *,
    email: str,
    phone: str,
    role: str,
    workspace_name: str,
) -> tuple[str, str]:
    async with db_session_factory() as session:
        workspace = Workspace(
            company_name=workspace_name,
            business_direction="Software",
            usage_purpose="CRM",
            team_size="2 - 5",
            has_team=True,
        )
        user = User(
            workspace=workspace,
            email=email,
            hashed_password=hash_password("Password123"),
            phone_number=phone,
            role_description=role,
            is_verified=True,
            last_login=datetime.now(UTC),
        )
        session.add_all([workspace, user])
        await session.commit()
        return user.id, workspace.id


async def _login(client, email: str, password: str = "Password123"):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password, "remember_me": True},
    )
    assert response.status_code == 200
    access_token = response.cookies.get("access_token")
    refresh_token = response.cookies.get("refresh_token")
    assert access_token is not None
    assert refresh_token is not None
    client.headers["Cookie"] = f"access_token={access_token}; refresh_token={refresh_token}"


@pytest.mark.asyncio
async def test_invitation_lifecycle_and_duplicate_rejection(client, db_session_factory):
    await _seed_workspace_user(
        db_session_factory,
        email="owner@example.com",
        phone="+12345670001",
        role="Admin/Owner",
        workspace_name="Main",
    )

    await _login(client, "owner@example.com")

    created = await client.post(
        "/api/v1/auth/invitations",
        json={"email": "new.member@example.com", "role_description": "Team Member"},
    )
    assert created.status_code == 201
    created_payload = created.json()
    invitation_id = created_payload["invitation"]["id"]
    first_token = created_payload["token"]

    duplicate = await client.post(
        "/api/v1/auth/invitations",
        json={"email": "new.member@example.com", "role_description": "Team Member"},
    )
    assert duplicate.status_code == 409

    listed = await client.get("/api/v1/auth/invitations")
    assert listed.status_code == 200
    assert len(listed.json()["items"]) == 1

    edited = await client.patch(
        f"/api/v1/auth/invitations/{invitation_id}",
        json={"role_description": "PM/Team Lead"},
    )
    assert edited.status_code == 200
    assert edited.json()["role_description"] == "PM/Team Lead"

    resent = await client.post(f"/api/v1/auth/invitations/{invitation_id}/resend")
    assert resent.status_code == 200
    second_token = resent.json()["token"]
    assert second_token != first_token

    revoked = await client.delete(f"/api/v1/auth/invitations/{invitation_id}")
    assert revoked.status_code == 204

    accept_revoked = await client.post(
        "/api/v1/auth/invitations/accept",
        json={"token": second_token, "transfer_confirmed": False},
    )
    assert accept_revoked.status_code == 400


@pytest.mark.asyncio
async def test_expired_invite_and_cross_workspace_transfer_confirmation(client, db_session_factory):
    await _seed_workspace_user(
        db_session_factory,
        email="owner@example.com",
        phone="+12345670002",
        role="Admin/Owner",
        workspace_name="Target",
    )
    existing_user_id, existing_workspace_id = await _seed_workspace_user(
        db_session_factory,
        email="existing@example.com",
        phone="+12345670003",
        role="Team Member",
        workspace_name="Source",
    )

    await _login(client, "owner@example.com")

    invite = await client.post(
        "/api/v1/auth/invitations",
        json={"email": "existing@example.com", "role_description": "Team Member"},
    )
    assert invite.status_code == 201
    token = invite.json()["token"]
    invitation_id = invite.json()["invitation"]["id"]
    target_workspace_id = invite.json()["invitation"]["workspace_id"]

    transfer_required = await client.post(
        "/api/v1/auth/invitations/accept",
        json={"token": token, "transfer_confirmed": False},
    )
    assert transfer_required.status_code == 409

    accepted = await client.post(
        "/api/v1/auth/invitations/accept",
        json={"token": token, "transfer_confirmed": True},
    )
    assert accepted.status_code == 200
    assert accepted.json()["user"]["workspace_id"] == target_workspace_id

    async with db_session_factory() as session:
        moved_user = await session.get(User, existing_user_id)
        assert moved_user is not None
        assert moved_user.workspace_id != existing_workspace_id

    second_invite = await client.post(
        "/api/v1/auth/invitations",
        json={"email": "expired@example.com", "role_description": "Team Member"},
    )
    assert second_invite.status_code == 201
    second_invite_id = second_invite.json()["invitation"]["id"]
    second_token = second_invite.json()["token"]

    async with db_session_factory() as session:
        invitation = await session.get(Invitation, second_invite_id)
        assert invitation is not None
        invitation.expires_at = datetime.now(UTC) - timedelta(minutes=1)
        await session.commit()

    expired = await client.post(
        "/api/v1/auth/invitations/accept",
        json={"token": second_token, "transfer_confirmed": False},
    )
    assert expired.status_code == 410

    async with db_session_factory() as session:
        invitation = await session.get(Invitation, invitation_id)
        assert invitation is not None
        assert invitation.status == "accepted"
