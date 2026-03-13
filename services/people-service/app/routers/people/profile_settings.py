from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import AuthContext, get_auth_context
from app.schemas import (
    NotificationSettings,
    NotificationSettingsResponse,
    UpdateUserProfileRequest,
    UserProfileResponse,
)
from app.services.profile_settings import ProfileSettingsService

router = APIRouter()


def get_profile_settings_service() -> ProfileSettingsService:
    return ProfileSettingsService()


@router.get("/profile/me", response_model=UserProfileResponse)
async def get_profile_me(
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    profile_settings_service: ProfileSettingsService = Depends(get_profile_settings_service),
) -> UserProfileResponse:
    return await profile_settings_service.get_my_profile(session, auth)


@router.put("/profile/me", response_model=UserProfileResponse)
async def put_profile_me(
    payload: UpdateUserProfileRequest,
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    profile_settings_service: ProfileSettingsService = Depends(get_profile_settings_service),
) -> UserProfileResponse:
    return await profile_settings_service.update_my_profile(session, auth, payload)


@router.get("/settings/notifications", response_model=NotificationSettingsResponse)
async def get_notifications_settings(
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    profile_settings_service: ProfileSettingsService = Depends(get_profile_settings_service),
) -> NotificationSettingsResponse:
    return await profile_settings_service.get_notification_settings(session, auth)


@router.put("/settings/notifications", response_model=NotificationSettingsResponse)
async def put_notifications_settings(
    payload: NotificationSettings,
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    profile_settings_service: ProfileSettingsService = Depends(get_profile_settings_service),
) -> NotificationSettingsResponse:
    return await profile_settings_service.update_notification_settings(session, auth, payload)
