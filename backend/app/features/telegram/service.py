import secrets
from datetime import UTC, datetime, timedelta

from app.features.telegram.domain import (
    CheckVerificationCodeResponse,
    CreateVerificationIntentRequest,
    CreateVerificationIntentResponse,
    VerificationIntent,
)
from app.features.telegram.storage import RedisVerificationStore


class VerificationService:
    def __init__(self, store: RedisVerificationStore, bot_username: str, ttl_seconds: int) -> None:
        self._store = store
        self._bot_username = bot_username
        self._ttl_seconds = ttl_seconds

    @staticmethod
    def normalize_phone(phone_number: str) -> str:
        allowed = set("+0123456789")
        return "".join(char for char in phone_number if char in allowed)

    def build_bot_url(self, short_token: str) -> str:
        return f"https://t.me/{self._bot_username}?start={short_token}"

    async def create_intent(
        self,
        payload: CreateVerificationIntentRequest,
    ) -> CreateVerificationIntentResponse:
        normalized_phone = self.normalize_phone(payload.phone_number)
        short_token = secrets.token_urlsafe(18)
        expires_at = datetime.now(UTC) + timedelta(seconds=self._ttl_seconds)

        intent = VerificationIntent(
            short_token=short_token,
            phone_number=normalized_phone,
            workspace_id=payload.workspace_id,
            correlation_id=payload.correlation_id,
            expires_at=expires_at,
        )
        await self._store.save_intent(intent)

        return CreateVerificationIntentResponse(
            intent_id=intent.intent_id,
            short_token=short_token,
            bot_url=self.build_bot_url(short_token),
            expires_at=expires_at,
        )

    async def validate_code(self, phone_number: str, code: str) -> CheckVerificationCodeResponse:
        intent = await self._store.get_intent_by_phone(self.normalize_phone(phone_number))
        if intent is None:
            return CheckVerificationCodeResponse(verified=False, status="not_found")

        if intent.expires_at < datetime.now(UTC):
            return CheckVerificationCodeResponse(verified=False, status="expired", expires_at=intent.expires_at)

        if intent.code != code or intent.status != "verified":
            return CheckVerificationCodeResponse(verified=False, status="mismatch", expires_at=intent.expires_at)

        return CheckVerificationCodeResponse(verified=True, status="verified", expires_at=intent.expires_at)

    async def attach_user_session(self, telegram_user_id: int, short_token: str) -> VerificationIntent | None:
        intent = await self._store.get_intent_by_token(short_token)
        if intent is None:
            return None

        await self._store.bind_user_to_token(telegram_user_id, short_token)
        return intent

    async def confirm_contact(self, telegram_user_id: int, phone_number: str) -> VerificationIntent | None:
        short_token = await self._store.get_token_by_user(telegram_user_id)
        if short_token is None:
            return None

        intent = await self._store.get_intent_by_token(short_token)
        if intent is None:
            return None

        if self.normalize_phone(intent.phone_number) != self.normalize_phone(phone_number):
            intent.status = "mismatch"
            await self._store.update_intent(intent)
            return intent

        intent.status = "verified"
        intent.telegram_user_id = telegram_user_id
        intent.code = f"{secrets.randbelow(1_000_000):06d}"
        await self._store.update_intent(intent)
        return intent