from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import AuthContext, get_auth_context
from app.schemas import (
    EmployeeActivityListResponse,
    EmployeeListResponse,
    InviteEmployeeRequest,
    InviteEmployeeResponse,
)
from app.services.employees import EmployeesService

router = APIRouter()


def get_employees_service() -> EmployeesService:
    return EmployeesService()


@router.get("/employees", response_model=EmployeeListResponse)
async def get_employees(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    level: str | None = Query(default=None),
    position: str | None = Query(default=None),
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    employees_service: EmployeesService = Depends(get_employees_service),
) -> EmployeeListResponse:
    return await employees_service.list_employees(session, auth, page, limit, search, level, position)


@router.get("/employees/activity", response_model=EmployeeActivityListResponse)
async def get_employees_activity(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    employees_service: EmployeesService = Depends(get_employees_service),
) -> EmployeeActivityListResponse:
    return await employees_service.list_employee_activity(session, auth, page, limit, search)


@router.post("/employees/invite", response_model=InviteEmployeeResponse, status_code=status.HTTP_201_CREATED)
async def invite_employee(
    payload: InviteEmployeeRequest,
    _: AuthContext = Depends(get_auth_context),
    employees_service: EmployeesService = Depends(get_employees_service),
) -> InviteEmployeeResponse:
    return await employees_service.invite_employee(payload)
