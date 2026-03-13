from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import AuthContext
from app.models import EmployeeProfile, NotificationSettings as NotificationSettingsModel
from app.schemas import (
    NotificationSettings,
    NotificationSettingsResponse,
    UpdateUserProfileRequest,
    UserProfileResponse,
)
from app.services.common import PeopleDomainSupport


class ProfileSettingsService(PeopleDomainSupport):
    async def get_my_profile(self, session: AsyncSession, auth: AuthContext) -> UserProfileResponse:
        employee = await self._get_employee_by_user(session, auth)
        profile = await session.scalar(
            select(EmployeeProfile).where(EmployeeProfile.employee_id == employee.id)
        )
        return UserProfileResponse(profile=self._build_user_profile(employee, profile))

    async def update_my_profile(
        self,
        session: AsyncSession,
        auth: AuthContext,
        payload: UpdateUserProfileRequest,
    ) -> UserProfileResponse:
        employee = await self._get_employee_by_user(session, auth)
        profile = await session.scalar(
            select(EmployeeProfile).where(EmployeeProfile.employee_id == employee.id)
        )

        employee.first_name = payload.first_name.strip()
        employee.last_name = payload.last_name.strip()
        employee.position = payload.position.strip()

        if profile is None:
            profile = EmployeeProfile(employee_id=employee.id)
            session.add(profile)

        profile.company = payload.company
        profile.location = payload.location
        profile.birthday = payload.birthday
        profile.mobile_number = payload.mobile_number
        profile.skype = payload.skype

        await session.commit()
        await session.refresh(employee)
        await session.refresh(profile)

        return UserProfileResponse(profile=self._build_user_profile(employee, profile))

    async def get_notification_settings(
        self,
        session: AsyncSession,
        auth: AuthContext,
    ) -> NotificationSettingsResponse:
        employee = await self._get_employee_by_user(session, auth)
        settings = await session.scalar(
            select(NotificationSettingsModel).where(NotificationSettingsModel.employee_id == employee.id)
        )
        if settings is None:
            settings = NotificationSettingsModel(employee_id=employee.id)
            session.add(settings)
            await session.commit()
            await session.refresh(settings)

        return NotificationSettingsResponse(
            settings=NotificationSettings(
                issue_activity_email=settings.issue_activity_email,
                tracking_activity_push=settings.tracking_activity_push,
                new_comments_push=settings.new_comments_push,
                silent_hours_enabled=settings.silent_hours_enabled,
                silent_hours_after=settings.silent_hours_after,
            )
        )

    async def update_notification_settings(
        self,
        session: AsyncSession,
        auth: AuthContext,
        payload: NotificationSettings,
    ) -> NotificationSettingsResponse:
        employee = await self._get_employee_by_user(session, auth)
        settings = await session.scalar(
            select(NotificationSettingsModel).where(NotificationSettingsModel.employee_id == employee.id)
        )
        if settings is None:
            settings = NotificationSettingsModel(employee_id=employee.id)
            session.add(settings)

        settings.issue_activity_email = payload.issue_activity_email
        settings.tracking_activity_push = payload.tracking_activity_push
        settings.new_comments_push = payload.new_comments_push
        settings.silent_hours_enabled = payload.silent_hours_enabled
        settings.silent_hours_after = payload.silent_hours_after

        await session.commit()
        await session.refresh(settings)

        return NotificationSettingsResponse(
            settings=NotificationSettings(
                issue_activity_email=settings.issue_activity_email,
                tracking_activity_push=settings.tracking_activity_push,
                new_comments_push=settings.new_comments_push,
                silent_hours_enabled=settings.silent_hours_enabled,
                silent_hours_after=settings.silent_hours_after,
            )
        )
