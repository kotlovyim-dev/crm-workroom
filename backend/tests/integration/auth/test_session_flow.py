from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from app.features.auth.models import RefreshSession, User, Workspace
from app.features.auth.security import hash_password, hash_refresh_token


async def _seed_user(db_session_factory):
    async with db_session_factory() as session:
        workspace = Workspace(
            company_name="Acme",
            business_direction="Software",
            usage_purpose="CRM",
            team_size="2 - 5",
            has_team=True,
        )
        user = User(
            workspace=workspace,
            email="admin@example.com",
            hashed_password=hash_password("Password123"),
            phone_number="+12345678901",
            role_description="Admin/Owner",
            is_verified=True,
            last_login=datetime.now(UTC),
        )
        session.add_all([workspace, user])
        await session.commit()


def _set_auth_cookies(client, access_token: str, refresh_token: str) -> None:
    client.headers["Cookie"] = f"access_token={access_token}; refresh_token={refresh_token}"


def _set_refresh_cookie(client, refresh_token: str) -> None:
    client.headers["Cookie"] = f"refresh_token={refresh_token}"


@pytest.mark.asyncio
async def test_login_refresh_logout_and_invalid_refresh(client, db_session_factory):
    await _seed_user(db_session_factory)

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "Password123", "remember_me": True},
    )
    assert login.status_code == 200
    access_token = login.cookies.get("access_token")
    refresh_token = login.cookies.get("refresh_token")
    assert access_token is not None
    assert refresh_token is not None
    _set_auth_cookies(client, access_token, refresh_token)
    assert login.json()["user"]["role_description"] == "Admin/Owner"

    me = await client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["authenticated"] is True

    previous_refresh = refresh_token
    refreshed = await client.post("/api/v1/auth/refresh")
    assert refreshed.status_code == 200
    rotated_access = refreshed.cookies.get("access_token")
    rotated_refresh = refreshed.cookies.get("refresh_token")
    assert rotated_access is not None
    assert rotated_refresh is not None
    assert rotated_refresh != previous_refresh
    _set_auth_cookies(client, rotated_access, rotated_refresh)

    logout = await client.post("/api/v1/auth/logout")
    assert logout.status_code == 204

    _set_refresh_cookie(client, previous_refresh)
    old_refresh_attempt = await client.post(
        "/api/v1/auth/refresh",
    )
    assert old_refresh_attempt.status_code == 401

    _set_refresh_cookie(client, "rm.invalid")
    invalid_refresh_attempt = await client.post(
        "/api/v1/auth/refresh",
    )
    assert invalid_refresh_attempt.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_current_refresh_only(client, db_session_factory):
    await _seed_user(db_session_factory)

    first_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "Password123", "remember_me": True},
    )
    assert first_login.status_code == 200
    first_refresh = first_login.cookies.get("refresh_token")
    first_access = first_login.cookies.get("access_token")
    assert first_access is not None
    assert first_refresh is not None

    second_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "Password123", "remember_me": True},
    )
    assert second_login.status_code == 200
    second_refresh = second_login.cookies.get("refresh_token")
    second_access = second_login.cookies.get("access_token")
    assert second_access is not None
    assert second_refresh is not None
    assert second_refresh != first_refresh

    _set_auth_cookies(client, second_access, second_refresh)

    logout = await client.post("/api/v1/auth/logout")
    assert logout.status_code == 204

    async with db_session_factory() as session:
        sessions = (await session.scalars(select(RefreshSession))).all()
        revoked = [item for item in sessions if item.revoked_at is not None]
        assert len(sessions) == 2
        assert len(revoked) == 1

    _set_refresh_cookie(client, first_refresh)
    still_valid = await client.post(
        "/api/v1/auth/refresh",
    )
    assert still_valid.status_code == 200
    rotated_after_refresh = still_valid.cookies.get("refresh_token")
    assert rotated_after_refresh is not None

    async with db_session_factory() as session:
        expire_target = await session.scalar(
            select(RefreshSession).where(RefreshSession.token_hash == hash_refresh_token(rotated_after_refresh))
        )
        assert expire_target is not None
        expire_target.expires_at = datetime.now(UTC) - timedelta(minutes=1)
        await session.commit()

    _set_refresh_cookie(client, rotated_after_refresh)
    expired_attempt = await client.post(
        "/api/v1/auth/refresh",
    )
    assert expired_attempt.status_code == 401
