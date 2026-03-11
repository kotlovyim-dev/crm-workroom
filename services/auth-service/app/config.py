from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "auth-service"
    app_env: str = "development"
    database_url: str
    frontend_url: str = "http://localhost:3000"
    telegram_service_url: str = "http://localhost:8000"
    jwt_secret_key: str = "change-me"
    access_token_ttl_seconds: int = 900
    refresh_token_ttl_seconds: int = 2_592_000
    cookie_secure: bool = False
    cookie_domain: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("frontend_url", "telegram_service_url")    
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()