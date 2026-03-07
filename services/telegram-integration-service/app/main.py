from contextlib import asynccontextmanager

from aiogram import Bot
from fastapi import Depends, FastAPI, HTTPException, Request, status
from redis.asyncio import Redis

from app.bot import build_dispatcher, handle_update
from app.config import Settings, get_settings
from app.domain import (
    CheckVerificationCodeRequest,
    CheckVerificationCodeResponse,
    CreateVerificationIntentRequest,
    CreateVerificationIntentResponse,
)
from app.service import VerificationService
from app.storage import RedisVerificationStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    store = RedisVerificationStore(redis=redis, ttl_seconds=settings.verification_ttl_seconds)
    verification_service = VerificationService(
        store=store,
        bot_username=settings.telegram_bot_username,
        ttl_seconds=settings.verification_ttl_seconds,
    )
    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = build_dispatcher(verification_service)

    app.state.redis = redis
    app.state.bot = bot
    app.state.dispatcher = dispatcher
    app.state.verification_service = verification_service

    try:
        yield
    finally:
        await bot.session.close()
        await redis.aclose()


app = FastAPI(title="Telegram Integration Service", version="0.1.0", lifespan=lifespan)


def get_verification_service(request: Request) -> VerificationService:
    return request.app.state.verification_service


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/internal/verifications/intents", response_model=CreateVerificationIntentResponse)
async def create_verification_intent(
    payload: CreateVerificationIntentRequest,
    verification_service: VerificationService = Depends(get_verification_service),
) -> CreateVerificationIntentResponse:
    return await verification_service.create_intent(payload)


@app.post("/internal/verifications/check", response_model=CheckVerificationCodeResponse)
async def check_verification_code(
    payload: CheckVerificationCodeRequest,
    verification_service: VerificationService = Depends(get_verification_service),
) -> CheckVerificationCodeResponse:
    return await verification_service.validate_code(payload.phone_number, payload.code)


@app.post("/webhooks/telegram/{secret}", status_code=status.HTTP_202_ACCEPTED)
async def telegram_webhook(
    secret: str,
    payload: dict,
    request: Request,
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    if secret != settings.telegram_webhook_secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found")

    await handle_update(request.app.state.bot, request.app.state.dispatcher, payload)
    return {"status": "accepted"}