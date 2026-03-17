from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


TeamSize = Literal[
    "Only me",
    "2 - 5",
    "6 - 10",
    "11 - 20",
    "21 - 40",
    "41 - 50",
    "51 - 100",
    "101 - 500",
]


class RoleDescription(StrEnum):
    ADMIN_OWNER = "Admin/Owner"
    PM_TEAM_LEAD = "PM/Team Lead"
    TEAM_MEMBER = "Team Member"


INVITER_ROLES: set[RoleDescription] = {RoleDescription.ADMIN_OWNER, RoleDescription.PM_TEAM_LEAD}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    remember_me: bool = False


class InitTelegramVerificationRequest(BaseModel):
    phone_number: str = Field(min_length=7, max_length=20)


class InitTelegramVerificationResponse(BaseModel):
    bot_url: str
    expires_at: datetime


class VerifyTelegramCodeRequest(BaseModel):
    phone_number: str = Field(min_length=7, max_length=20)
    code: str = Field(min_length=6, max_length=6)


class VerifyTelegramCodeResponse(BaseModel):
    verified: bool
    status: str
    expires_at: datetime | None = None


class RegisterWorkspaceRequest(BaseModel):
    phone_number: str = Field(min_length=7, max_length=20)
    telegram_code: str = Field(min_length=6, max_length=6)
    email: EmailStr
    password: str = Field(min_length=8)
    usage_purpose: str = Field(min_length=1, max_length=255)
    role_description: RoleDescription = RoleDescription.ADMIN_OWNER
    additional_boolean_question: bool
    company_name: str = Field(min_length=2, max_length=255)
    team_size: TeamSize
    business_direction: str = Field(min_length=1, max_length=255)
    invited_members: list[EmailStr] = Field(default_factory=list)


class WorkspaceResponse(BaseModel):
    id: str
    company_name: str
    business_direction: str
    usage_purpose: str
    team_size: str
    has_team: bool


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    phone_number: str
    role_description: RoleDescription
    is_verified: bool
    workspace_id: str


class AuthResponse(BaseModel):
    user: UserResponse
    workspace: WorkspaceResponse


class SessionResponse(BaseModel):
    authenticated: bool
    user: UserResponse | None = None
    workspace: WorkspaceResponse | None = None


class TelegramIntentRequest(BaseModel):
    phone_number: str
    workspace_id: str | None = None
    correlation_id: str | None = None


class TelegramIntentResponse(BaseModel):
    intent_id: str
    short_token: str
    bot_url: str
    expires_at: datetime


class TelegramCheckRequest(BaseModel):
    phone_number: str
    code: str


class TelegramCheckResponse(BaseModel):
    verified: bool
    status: str
    expires_at: datetime | None = None


class InvitationCreateRequest(BaseModel):
    email: EmailStr
    role_description: RoleDescription


class InvitationUpdateRoleRequest(BaseModel):
    role_description: RoleDescription


class InvitationAcceptRequest(BaseModel):
    token: str = Field(min_length=16)
    transfer_confirmed: bool = False


class InvitationResponse(BaseModel):
    id: str
    workspace_id: str
    email: EmailStr
    invited_by_user_id: str
    role_description: RoleDescription
    status: str
    expires_at: datetime
    accepted_at: datetime | None
    revoked_at: datetime | None
    created_at: datetime


class InvitationTokenResponse(BaseModel):
    invitation: InvitationResponse
    token: str


class InvitationListResponse(BaseModel):
    items: list[InvitationResponse]