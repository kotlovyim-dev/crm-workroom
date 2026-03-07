from contextlib import asynccontextmanager

from fastapi import Cookie, Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import Base, engine, get_db_session
from app.models import User
from app.schemas import (
    AuthResponse,
    InitTelegramVerificationRequest,
    InitTelegramVerificationResponse,
    LoginRequest,
    RegisterWorkspaceRequest,
    SessionResponse,
    VerifyTelegramCodeRequest,
    VerifyTelegramCodeResponse,
)
from app.security import decode_access_token
from app.service import AuthService
from app.telegram_client import TelegramVerificationClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Auth Service", version="0.1.0", lifespan=lifespan)
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_auth_service(settings: Settings = Depends(get_settings)) -> AuthService:
    return AuthService(settings=settings, telegram_client=TelegramVerificationClient(settings))


async def get_current_user_id(
    access_token: str | None = Cookie(default=None, alias="access_token"),
    settings: Settings = Depends(get_settings),
) -> str:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_access_token(access_token, settings)
    except Exception as error:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session") from error

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    return user_id


def set_auth_cookies(response: Response, auth_service: AuthService, access_token: str, refresh_token: str) -> None:
    cookie_settings = auth_service.cookie_settings()
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.access_token_ttl_seconds,
        **cookie_settings,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.refresh_token_ttl_seconds,
        **cookie_settings,
    )


def clear_auth_cookies(response: Response, auth_service: AuthService) -> None:
    cookie_settings = auth_service.cookie_settings()
    response.delete_cookie(key="access_token", **cookie_settings)
    response.delete_cookie(key="refresh_token", **cookie_settings)


@app.get("/health", status_code=status.HTTP_200_OK)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/auth/login", response_model=AuthResponse)
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
    refresh_token = await auth_service.create_refresh_session(session, user_record, request)
    access_token = auth_service.build_access_token(user_record)
    set_auth_cookies(response, auth_service, access_token, refresh_token)
    return auth_response


@app.post(
    "/api/v1/auth/init-telegram-verification",
    response_model=InitTelegramVerificationResponse,
)
async def init_telegram_verification(
    payload: InitTelegramVerificationRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> InitTelegramVerificationResponse:
    return await auth_service.init_telegram_verification(payload)


@app.post("/api/v1/auth/verify-telegram-code", response_model=VerifyTelegramCodeResponse)
async def verify_telegram_code(
    payload: VerifyTelegramCodeRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> VerifyTelegramCodeResponse:
    return await auth_service.verify_telegram_code(payload)


@app.post("/api/v1/auth/register-workspace", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
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


@app.post("/api/v1/auth/refresh", response_model=AuthResponse)
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


@app.post("/api/v1/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    await auth_service.logout(session, refresh_token)
    clear_auth_cookies(response, auth_service)
    return response


@app.get("/api/v1/auth/me", response_model=SessionResponse)
async def me(
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> SessionResponse:
    return await auth_service.get_session(session, user_id)