import json

from redis.asyncio import Redis

from app.domain import VerificationIntent


class RedisVerificationStore:
    def __init__(self, redis: Redis, ttl_seconds: int) -> None:
        self._redis = redis
        self._ttl_seconds = ttl_seconds

    @staticmethod
    def _intent_key(short_token: str) -> str:
        return f"tg_verify:intent:{short_token}"

    @staticmethod
    def _phone_key(phone_number: str) -> str:
        return f"tg_verify:phone:{phone_number}"

    @staticmethod
    def _user_key(telegram_user_id: int) -> str:
        return f"tg_verify:user:{telegram_user_id}"

    async def save_intent(self, intent: VerificationIntent) -> None:
        payload = intent.model_dump(mode="json")
        await self._redis.setex(self._intent_key(intent.short_token), self._ttl_seconds, json.dumps(payload))
        await self._redis.setex(self._phone_key(intent.phone_number), self._ttl_seconds, intent.short_token)

    async def get_intent_by_token(self, short_token: str) -> VerificationIntent | None:
        payload = await self._redis.get(self._intent_key(short_token))
        if payload is None:
            return None

        return VerificationIntent.model_validate_json(payload)

    async def get_intent_by_phone(self, phone_number: str) -> VerificationIntent | None:
        short_token = await self._redis.get(self._phone_key(phone_number))
        if short_token is None:
            return None

        return await self.get_intent_by_token(short_token)

    async def bind_user_to_token(self, telegram_user_id: int, short_token: str) -> None:
        await self._redis.setex(self._user_key(telegram_user_id), self._ttl_seconds, short_token)

    async def get_token_by_user(self, telegram_user_id: int) -> str | None:
        return await self._redis.get(self._user_key(telegram_user_id))

    async def update_intent(self, intent: VerificationIntent) -> None:
        await self.save_intent(intent)