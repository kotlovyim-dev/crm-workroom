from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.features.shared.dependencies import AuthContext, get_auth_context
from app.features.shared.schemas import (
	CreateTimeOffRequest,
	TimeOffRequest,
	TimeOffRequestListResponse,
	VacationBalanceListResponse,
	VacationBalanceResponse,
)
from app.features.vacations.services import VacationsService

router = APIRouter()


def get_vacations_service() -> VacationsService:
	return VacationsService()


@router.get("/vacations/balances/me", response_model=VacationBalanceResponse)
async def get_vacation_balance_me(
	year: int | None = Query(default=None, ge=2000, le=2100),
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	vacations_service: VacationsService = Depends(get_vacations_service),
) -> VacationBalanceResponse:
	return await vacations_service.get_my_vacation_balance(session, auth, year)


@router.get("/vacations/balances", response_model=VacationBalanceListResponse)
async def get_vacation_balances(
	page: int = Query(default=1, ge=1),
	limit: int = Query(default=20, ge=1, le=100),
	search: str | None = Query(default=None),
	year: int | None = Query(default=None, ge=2000, le=2100),
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	vacations_service: VacationsService = Depends(get_vacations_service),
) -> VacationBalanceListResponse:
	return await vacations_service.list_vacation_balances(session, auth, page, limit, search, year)


@router.get("/vacations/requests/me", response_model=TimeOffRequestListResponse)
async def get_vacation_requests_me(
	page: int = Query(default=1, ge=1),
	limit: int = Query(default=20, ge=1, le=100),
	status_filter: str | None = Query(default=None, alias="status"),
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	vacations_service: VacationsService = Depends(get_vacations_service),
) -> TimeOffRequestListResponse:
	return await vacations_service.list_my_time_off_requests(session, auth, page, limit, status_filter)


@router.post("/vacations/requests", response_model=TimeOffRequest, status_code=status.HTTP_201_CREATED)
async def post_vacation_request(
	payload: CreateTimeOffRequest,
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	vacations_service: VacationsService = Depends(get_vacations_service),
) -> TimeOffRequest:
	return await vacations_service.create_time_off_request(session, auth, payload)


@router.get("/vacations/timeline", response_model=TimeOffRequestListResponse)
async def get_vacation_timeline(
	page: int = Query(default=1, ge=1),
	limit: int = Query(default=20, ge=1, le=100),
	month: int | None = Query(default=None, ge=1, le=12),
	year: int | None = Query(default=None, ge=2000, le=2100),
	search: str | None = Query(default=None),
	status_filter: str | None = Query(default=None, alias="status"),
	request_type: str | None = Query(default=None, alias="type"),
	auth: AuthContext = Depends(get_auth_context),
	session: AsyncSession = Depends(get_db_session),
	vacations_service: VacationsService = Depends(get_vacations_service),
) -> TimeOffRequestListResponse:
	return await vacations_service.list_vacation_timeline(
		session,
		auth,
		page,
		limit,
		month,
		year,
		search,
		status_filter,
		request_type,
	)


__all__ = ["get_vacations_service", "router"]
