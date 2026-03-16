from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.features.profile.services import ProfileService
from app.features.shared.dependencies import AuthContext, get_auth_context
from app.features.shared.schemas import (
	NotificationSettings,
	NotificationSettingsResponse,
	UpdateUserProfileRequest,
	UserProfileResponse,
)

router = APIRouter()


def get_profile_service() -> ProfileService:
	return ProfileService()


@router.get("/profile/me", response_model=UserProfileResponse)
async def get_profile_me(
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	profile_service: ProfileService = Depends(get_profile_service),
) -> UserProfileResponse:
	return await profile_service.get_my_profile(session, auth)


@router.put("/profile/me", response_model=UserProfileResponse)
async def put_profile_me(
	payload: UpdateUserProfileRequest,
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	profile_service: ProfileService = Depends(get_profile_service),
) -> UserProfileResponse:
	return await profile_service.update_my_profile(session, auth, payload)


@router.get("/settings/notifications", response_model=NotificationSettingsResponse)
async def get_notifications_settings(
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	profile_service: ProfileService = Depends(get_profile_service),
) -> NotificationSettingsResponse:
	return await profile_service.get_notification_settings(session, auth)


@router.put("/settings/notifications", response_model=NotificationSettingsResponse)
async def put_notifications_settings(
	payload: NotificationSettings,
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	profile_service: ProfileService = Depends(get_profile_service),
) -> NotificationSettingsResponse:
	return await profile_service.update_notification_settings(session, auth, payload)


__all__ = ["get_profile_service", "router"]
