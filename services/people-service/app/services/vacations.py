from datetime import date

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import AuthContext
from app.models import Employee, TimeOffRequest
from app.schemas import (
    CreateTimeOffRequest,
    EmployeeBalanceItem,
    TimeOffRequest as TimeOffRequestDTO,
    TimeOffRequestListResponse,
    VacationBalanceListResponse,
    VacationBalanceResponse,
)
from app.services.common import PeopleDomainSupport
from app.services.employees import EmployeesService


class VacationsService(PeopleDomainSupport):
    async def get_my_vacation_balance(
        self,
        session: AsyncSession,
        auth: AuthContext,
        year: int | None,
    ) -> VacationBalanceResponse:
        employee = await self._get_employee_by_user(session, auth)
        target_year = year or self._current_year()
        balance = await self._get_or_create_balance(session, employee.id, target_year)
        return VacationBalanceResponse(balance=self._balance_dto(balance))

    async def list_vacation_balances(
        self,
        session: AsyncSession,
        auth: AuthContext,
        page: int,
        limit: int,
        search: str | None,
        year: int | None,
    ) -> VacationBalanceListResponse:
        target_year = year or self._current_year()
        employees_data = await EmployeesService().list_employees(
            session=session,
            auth=auth,
            page=page,
            limit=limit,
            search=search,
            level=None,
            position=None,
        )

        items: list[EmployeeBalanceItem] = []
        for employee in employees_data.items:
            balance = await self._get_or_create_balance(session, employee.id, target_year)
            items.append(EmployeeBalanceItem(employee=employee, balance=self._balance_dto(balance)))

        await session.commit()

        return VacationBalanceListResponse(
            items=items,
            page=employees_data.page,
            limit=employees_data.limit,
            total=employees_data.total,
        )

    async def list_my_time_off_requests(
        self,
        session: AsyncSession,
        auth: AuthContext,
        page: int,
        limit: int,
        status_filter: str | None,
    ) -> TimeOffRequestListResponse:
        employee = await self._get_employee_by_user(session, auth)
        query = select(TimeOffRequest).where(TimeOffRequest.employee_id == employee.id)
        count_query = select(func.count()).select_from(TimeOffRequest).where(
            TimeOffRequest.employee_id == employee.id
        )

        if status_filter:
            query = query.where(TimeOffRequest.status == status_filter)
            count_query = count_query.where(TimeOffRequest.status == status_filter)

        query = query.order_by(TimeOffRequest.created_at.desc())
        query = query.offset((page - 1) * limit).limit(limit)

        requests = list(await session.scalars(query))
        total = await session.scalar(count_query) or 0

        return TimeOffRequestListResponse(
            items=[self._time_off_dto(item) for item in requests],
            page=page,
            limit=limit,
            total=total,
        )

    async def create_time_off_request(
        self,
        session: AsyncSession,
        auth: AuthContext,
        payload: CreateTimeOffRequest,
    ) -> TimeOffRequestDTO:
        employee = await self._get_employee_by_user(session, auth)

        request = TimeOffRequest(
            workspace_id=auth.workspace_id,
            employee_id=employee.id,
            type=payload.type,
            status="pending",
            duration_type=payload.duration_type,
            start_date=payload.start_date,
            end_date=payload.end_date,
            time_from=payload.time_from,
            time_to=payload.time_to,
            requested_units=self._compute_requested_units(
                payload.duration_type,
                payload.start_date,
                payload.end_date,
                payload.time_from,
                payload.time_to,
            ),
            comment=payload.comment,
            created_by=auth.user_id,
            updated_by=auth.user_id,
        )

        session.add(request)
        await session.commit()
        await session.refresh(request)
        return self._time_off_dto(request)

    async def list_vacation_timeline(
        self,
        session: AsyncSession,
        auth: AuthContext,
        page: int,
        limit: int,
        month: int | None,
        year: int | None,
        search: str | None,
        status_filter: str | None,
        request_type: str | None,
    ) -> TimeOffRequestListResponse:
        query = select(TimeOffRequest, Employee).join(Employee, Employee.id == TimeOffRequest.employee_id)
        query = query.where(TimeOffRequest.workspace_id == auth.workspace_id)

        count_query = (
            select(func.count())
            .select_from(TimeOffRequest)
            .where(TimeOffRequest.workspace_id == auth.workspace_id)
        )

        if month and year:
            month_start = date(year, month, 1)
            month_end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
            interval_filter = and_(
                TimeOffRequest.start_date < month_end,
                TimeOffRequest.end_date >= month_start,
            )
            query = query.where(interval_filter)
            count_query = count_query.where(interval_filter)

        if status_filter:
            query = query.where(TimeOffRequest.status == status_filter)
            count_query = count_query.where(TimeOffRequest.status == status_filter)

        if request_type:
            query = query.where(TimeOffRequest.type == request_type)
            count_query = count_query.where(TimeOffRequest.type == request_type)

        if search:
            pattern = f"%{search.strip()}%"
            search_filter = or_(
                Employee.first_name.ilike(pattern),
                Employee.last_name.ilike(pattern),
                Employee.email.ilike(pattern),
            )
            query = query.where(search_filter)
            count_query = count_query.where(
                select(Employee.id)
                .where(Employee.id == TimeOffRequest.employee_id)
                .where(search_filter)
                .exists()
            )

        query = query.order_by(TimeOffRequest.start_date.asc(), TimeOffRequest.created_at.desc())
        query = query.offset((page - 1) * limit).limit(limit)

        rows = (await session.execute(query)).all()
        total = await session.scalar(count_query) or 0
        items = [self._time_off_dto(row.TimeOffRequest) for row in rows]

        return TimeOffRequestListResponse(items=items, page=page, limit=limit, total=total)
