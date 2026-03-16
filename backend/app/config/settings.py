from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "backend"
    app_env: str = "development"
    database_url: str = ""
    frontend_url: str = "http://localhost:3000"
    telegram_service_url: str = "http://localhost:8000/api/v1/telegram"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "change-me"
    access_token_ttl_seconds: int = 900
    refresh_token_ttl_seconds: int = 2_592_000
    cookie_secure: bool = False
    cookie_domain: str | None = None
    telegram_bot_token: str = ""
    telegram_bot_username: str = "workroom_verification_bot"
    telegram_delivery_mode: Literal["webhook", "polling"] = "webhook"
    telegram_webhook_secret: str = ""
    verification_ttl_seconds: int = 300

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("database_url is required")
        return value

    @field_validator("frontend_url", "telegram_service_url")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()
