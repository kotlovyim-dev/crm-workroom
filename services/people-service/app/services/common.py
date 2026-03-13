from datetime import UTC, datetime
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import AuthContext
from app.models import CalendarEvent, Employee, EmployeeProfile, TimeOffRequest, VacationBalance
from app.schemas import (
    CalendarEvent as CalendarEventDTO,
    DurationType,
    EmployeeSummary,
    TimeOffRequest as TimeOffRequestDTO,
    TimeOffStatus,
    TimeOffType,
    UserProfile,
    VacationBalance as VacationBalanceDTO,
)


class PeopleDomainSupport:
    async def _get_employee_by_user(self, session: AsyncSession, auth: AuthContext) -> Employee:
        employee = await session.scalar(
            select(Employee).where(
                Employee.workspace_id == auth.workspace_id,
                Employee.user_id == auth.user_id,
            )
        )
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return employee

    async def _get_or_create_balance(
        self,
        session: AsyncSession,
        employee_id: str,
        year: int,
    ) -> VacationBalance:
        balance = await session.scalar(
            select(VacationBalance).where(
                VacationBalance.employee_id == employee_id,
                VacationBalance.year == year,
            )
        )
        if balance is not None:
            return balance

        balance = VacationBalance(
            employee_id=employee_id,
            year=year,
            vacation_total=16,
            vacation_used=0,
            sick_leave_total=10,
            sick_leave_used=0,
            remote_days_total=20,
            remote_days_used=0,
        )
        session.add(balance)
        await session.flush()
        return balance

    async def _get_workspace_event(
        self,
        session: AsyncSession,
        workspace_id: str,
        event_id: str,
    ) -> CalendarEvent:
        event = await session.scalar(
            select(CalendarEvent).where(
                CalendarEvent.id == event_id,
                CalendarEvent.workspace_id == workspace_id,
            )
        )
        if event is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return event

    def _employee_summary(self, employee: Employee) -> EmployeeSummary:
        return EmployeeSummary(
            id=employee.id,
            workspace_id=employee.workspace_id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            full_name=f"{employee.first_name} {employee.last_name}".strip(),
            email=employee.email,
            avatar_url=employee.avatar_url,
            position=employee.position,
            level=employee.level,
            role_label=employee.role_label,
        )

    def _build_user_profile(
        self,
        employee: Employee,
        profile: EmployeeProfile | None,
    ) -> UserProfile:
        return UserProfile(
            id=employee.id,
            workspace_id=employee.workspace_id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            full_name=f"{employee.first_name} {employee.last_name}".strip(),
            email=employee.email,
            avatar_url=employee.avatar_url,
            position=employee.position,
            company=profile.company if profile else None,
            location=profile.location if profile else None,
            birthday=profile.birthday if profile else None,
            mobile_number=profile.mobile_number if profile else None,
            skype=profile.skype if profile else None,
        )

    def _balance_dto(self, balance: VacationBalance) -> VacationBalanceDTO:
        return VacationBalanceDTO(
            employee_id=balance.employee_id,
            year=balance.year,
            vacation_total=balance.vacation_total,
            vacation_used=balance.vacation_used,
            vacation_available=max(balance.vacation_total - balance.vacation_used, 0),
            sick_leave_total=balance.sick_leave_total,
            sick_leave_used=balance.sick_leave_used,
            sick_leave_available=max(balance.sick_leave_total - balance.sick_leave_used, 0),
            remote_days_total=balance.remote_days_total,
            remote_days_used=balance.remote_days_used,
            remote_days_available=max(balance.remote_days_total - balance.remote_days_used, 0),
        )

    def _time_off_dto(self, item: TimeOffRequest) -> TimeOffRequestDTO:
        return TimeOffRequestDTO(
            id=item.id,
            employee_id=item.employee_id,
            type=cast(TimeOffType, item.type),
            status=cast(TimeOffStatus, item.status),
            duration_type=cast(DurationType, item.duration_type),
            start_date=item.start_date,
            end_date=item.end_date,
            requested_units=item.requested_units,
            comment=item.comment,
            created_at=item.created_at,
            time_from=item.time_from,
            time_to=item.time_to,
        )

    def _calendar_event(self, item: CalendarEvent) -> CalendarEventDTO:
        return CalendarEventDTO(
            id=item.id,
            workspace_id=item.workspace_id,
            title=item.title,
            date=item.date,
            start_time=item.start_time,
            end_time=item.end_time,
            duration_label=item.duration_label,
            type=item.type,
            color_accent=item.color_accent,
            trend=item.trend,
        )

    def _compute_requested_units(self, duration_type: str, start_date, end_date, time_from, time_to) -> int:
        if duration_type == "days":
            return (end_date - start_date).days + 1

        assert time_from is not None
        assert time_to is not None
        minutes = time_to.hour * 60 + time_to.minute
        minutes -= time_from.hour * 60 + time_from.minute
        return max(minutes // 60, 1)

    def _current_year(self) -> int:
        return datetime.now(UTC).year
