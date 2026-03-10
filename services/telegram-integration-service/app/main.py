import asyncio
import contextlib
from contextlib import asynccontextmanager
from typing import Any

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


def build_lifespan():
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
        app.state.polling_task = None

        if settings.telegram_delivery_mode == "polling":
            await bot.delete_webhook(drop_pending_updates=True)
            app.state.polling_task = asyncio.create_task(dispatcher.start_polling(bot))

        try:
            yield
        finally:
            polling_task = app.state.polling_task
            if polling_task is not None:
                polling_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await polling_task
            await bot.session.close()
            await redis.aclose()

    return lifespan


def create_app(*, enable_runtime: bool = True) -> FastAPI:
    app = FastAPI(
        title="Telegram Integration Service",
        version="0.1.0",
        lifespan=build_lifespan() if enable_runtime else None,
    )

    if not enable_runtime:
        app.state.redis = None
        app.state.bot = None
        app.state.dispatcher = None
        app.state.verification_service = None
        app.state.polling_task = None

    @app.get("/health", status_code=status.HTTP_200_OK)
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready", status_code=status.HTTP_200_OK)
    async def readiness(request: Request) -> dict[str, str]:
        verification_service = getattr(request.app.state, "verification_service", None)
        redis = getattr(request.app.state, "redis", None)

        if verification_service is None or redis is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready")

        await redis.ping()
        return {"status": "ready"}

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
        payload: dict[str, Any],
        request: Request,
        settings: Settings = Depends(get_settings),
    ) -> dict[str, str]:
        if secret != settings.telegram_webhook_secret:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found")

        await handle_update(request.app.state.bot, request.app.state.dispatcher, payload)
        return {"status": "accepted"}

    return app


def get_verification_service(request: Request) -> VerificationService:
    verification_service = getattr(request.app.state, "verification_service", None)
    if verification_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready")
    return verification_service


app = create_app()