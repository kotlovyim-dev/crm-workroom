import httpx

from app.config.settings import Settings
from app.features.auth.schemas import (
    TelegramCheckRequest,
    TelegramCheckResponse,
    TelegramIntentRequest,
    TelegramIntentResponse,
)


class TelegramVerificationClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.telegram_service_url

    async def create_intent(self, payload: TelegramIntentRequest) -> TelegramIntentResponse:
        async with httpx.AsyncClient(base_url=self._base_url, timeout=10.0) as client:
            response = await client.post("/internal/verifications/intents", json=payload.model_dump())
            response.raise_for_status()
            return TelegramIntentResponse.model_validate(response.json())

    async def check_code(self, payload: TelegramCheckRequest) -> TelegramCheckResponse:
        async with httpx.AsyncClient(base_url=self._base_url, timeout=10.0) as client:
            response = await client.post("/internal/verifications/check", json=payload.model_dump())
            response.raise_for_status()
            return TelegramCheckResponse.model_validate(response.json())