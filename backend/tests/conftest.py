from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import cast

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config.settings import Settings
from app.db.base import Base
from app.features.auth.routes import get_auth_service, router as auth_router
from app.features.auth.schemas import TelegramCheckResponse, TelegramIntentResponse
from app.features.auth.telegram_client import TelegramVerificationClient
from app.features.auth.service import AuthService
from app.features.auth import routes as auth_routes


class FakeTelegramVerificationClient:
    async def create_intent(self, payload):  # noqa: ANN001
        return TelegramIntentResponse(
            intent_id="test-intent",
            short_token="123456",
            bot_url="https://t.me/workroom_verification_bot",
            expires_at=datetime.now(UTC),
        )

    async def check_code(self, payload):  # noqa: ANN001
        return TelegramCheckResponse(verified=True, status="verified", expires_at=None)


@pytest_asyncio.fixture
async def db_session_factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    try:
        yield session_factory
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def app(db_session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[FastAPI]:
    app = FastAPI()
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

    async def override_db_session() -> AsyncIterator[AsyncSession]:
        async with db_session_factory() as session:
            yield session

    def override_auth_service() -> AuthService:
        settings = Settings(database_url="sqlite+aiosqlite:///:memory:")
        fake_client = cast(TelegramVerificationClient, FakeTelegramVerificationClient())
        return AuthService(settings=settings, telegram_client=fake_client)

    auth_routes.settings = Settings(database_url="sqlite+aiosqlite:///:memory:", cookie_domain=None, cookie_secure=False)

    from app.db.session import get_db_session

    app.dependency_overrides[get_db_session] = override_db_session
    app.dependency_overrides[get_auth_service] = override_auth_service

    yield app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as async_client:
        yield async_client
