from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import AuthContext
from app.models import Employee
from app.schemas import (
    EmployeeActivityListResponse,
    EmployeeActivitySummary,
    EmployeeListResponse,
    EmployeeWithActivity,
    InviteEmployeeRequest,
    InviteEmployeeResponse,
)
from app.services.common import PeopleDomainSupport


class EmployeesService(PeopleDomainSupport):
    async def list_employees(
        self,
        session: AsyncSession,
        auth: AuthContext,
        page: int,
        limit: int,
        search: str | None,
        level: str | None,
        position: str | None,
    ) -> EmployeeListResponse:
        query = select(Employee).where(Employee.workspace_id == auth.workspace_id)
        count_query = select(func.count()).select_from(Employee).where(Employee.workspace_id == auth.workspace_id)

        if search:
            pattern = f"%{search.strip()}%"
            condition = or_(
                Employee.first_name.ilike(pattern),
                Employee.last_name.ilike(pattern),
                Employee.email.ilike(pattern),
                Employee.position.ilike(pattern),
            )
            query = query.where(condition)
            count_query = count_query.where(condition)

        if level:
            query = query.where(Employee.level == level)
            count_query = count_query.where(Employee.level == level)

        if position:
            pattern = f"%{position.strip()}%"
            query = query.where(Employee.position.ilike(pattern))
            count_query = count_query.where(Employee.position.ilike(pattern))

        query = query.order_by(Employee.last_name.asc(), Employee.first_name.asc())
        query = query.offset((page - 1) * limit).limit(limit)

        employees = list(await session.scalars(query))
        total = await session.scalar(count_query) or 0

        return EmployeeListResponse(
            items=[self._employee_summary(item) for item in employees],
            page=page,
            limit=limit,
            total=total,
        )

    async def list_employee_activity(
        self,
        session: AsyncSession,
        auth: AuthContext,
        page: int,
        limit: int,
        search: str | None,
    ) -> EmployeeActivityListResponse:
        employees_page = await self.list_employees(
            session=session,
            auth=auth,
            page=page,
            limit=limit,
            search=search,
            level=None,
            position=None,
        )

        items = [
            EmployeeWithActivity(
                employee=employee,
                activity=EmployeeActivitySummary(
                    employee_id=employee.id,
                    backlog_tasks=0,
                    tasks_in_progress=0,
                    tasks_in_review=0,
                ),
            )
            for employee in employees_page.items
        ]

        return EmployeeActivityListResponse(
            items=items,
            page=employees_page.page,
            limit=employees_page.limit,
            total=employees_page.total,
        )

    async def invite_employee(self, payload: InviteEmployeeRequest) -> InviteEmployeeResponse:
        return InviteEmployeeResponse(status="invited", email=payload.email)
