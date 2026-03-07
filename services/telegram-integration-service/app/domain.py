from datetime import UTC, datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


VerificationStatus = Literal["pending", "verified", "expired", "not_found", "mismatch", "failed"]


class CreateVerificationIntentRequest(BaseModel):
    phone_number: str = Field(min_length=7, max_length=20)
    workspace_id: UUID | None = None
    correlation_id: str | None = None


class CreateVerificationIntentResponse(BaseModel):
    intent_id: UUID
    short_token: str
    bot_url: str
    expires_at: datetime


class CheckVerificationCodeRequest(BaseModel):
    phone_number: str = Field(min_length=7, max_length=20)
    code: str = Field(min_length=6, max_length=6)


class CheckVerificationCodeResponse(BaseModel):
    verified: bool
    status: VerificationStatus
    expires_at: datetime | None = None


class VerificationIntent(BaseModel):
    intent_id: UUID = Field(default_factory=uuid4)
    short_token: str
    phone_number: str
    status: VerificationStatus = "pending"
    code: str | None = None
    telegram_user_id: int | None = None
    workspace_id: UUID | None = None
    correlation_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime