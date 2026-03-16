from typing import Any

from aiogram import Bot, Dispatcher
from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.asyncio import Redis

from app.config.settings import Settings, get_settings
from app.features.telegram.bot import handle_update
from app.features.telegram.domain import (
    CheckVerificationCodeRequest,
    CheckVerificationCodeResponse,
    CreateVerificationIntentRequest,
    CreateVerificationIntentResponse,
)
from app.features.telegram.service import VerificationService

router = APIRouter()


def get_verification_service(request: Request) -> VerificationService:
    verification_service = getattr(request.app.state, "verification_service", None)
    if verification_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready")
    return verification_service


@router.get("/health", status_code=status.HTTP_200_OK)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness(request: Request) -> dict[str, str]:
    verification_service = getattr(request.app.state, "verification_service", None)
    redis = getattr(request.app.state, "redis", None)

    if verification_service is None or not isinstance(redis, Redis):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready")

    await redis.ping()
    return {"status": "ready"}


@router.post("/internal/verifications/intents", response_model=CreateVerificationIntentResponse)
async def create_verification_intent(
    payload: CreateVerificationIntentRequest,
    verification_service: VerificationService = Depends(get_verification_service),
) -> CreateVerificationIntentResponse:
    return await verification_service.create_intent(payload)


@router.post("/internal/verifications/check", response_model=CheckVerificationCodeResponse)
async def check_verification_code(
    payload: CheckVerificationCodeRequest,
    verification_service: VerificationService = Depends(get_verification_service),
) -> CheckVerificationCodeResponse:
    return await verification_service.validate_code(payload.phone_number, payload.code)


@router.post("/webhooks/telegram/{secret}", status_code=status.HTTP_202_ACCEPTED)
async def telegram_webhook(
    secret: str,
    payload: dict[str, Any],
    request: Request,
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    if secret != settings.telegram_webhook_secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found")

    bot = getattr(request.app.state, "bot", None)
    dispatcher = getattr(request.app.state, "dispatcher", None)
    if not isinstance(bot, Bot) or not isinstance(dispatcher, Dispatcher):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Bot runtime is disabled")

    await handle_update(bot, dispatcher, payload)
    return {"status": "accepted"}
