from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "telegram-integration-service"
    app_env: str = "development"
    redis_url: str = "redis://localhost:6379/0"
    telegram_bot_token: str
    telegram_bot_username: str = "workroom_verification_bot"
    telegram_delivery_mode: Literal["webhook", "polling"] = "webhook"
    telegram_webhook_secret: str
    verification_ttl_seconds: int = 300

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()