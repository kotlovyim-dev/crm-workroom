from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import AuthContext, get_auth_context
from app.schemas import (
    CalendarDeleteResponse,
    CalendarEventResponse,
    CalendarEventsResponse,
    CreateCalendarEventRequest,
    UpdateCalendarEventRequest,
)
from app.services.calendar import CalendarService

router = APIRouter()


def get_calendar_service() -> CalendarService:
    return CalendarService()


@router.get("/calendar/events", response_model=CalendarEventsResponse)
async def get_calendar_events(
    start_date: date = Query(...),
    end_date: date = Query(...),
    event_type: str | None = Query(default=None, alias="type"),
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> CalendarEventsResponse:
    return await calendar_service.list_calendar_events(session, auth, start_date, end_date, event_type)


@router.post("/calendar/events", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
async def post_calendar_event(
    payload: CreateCalendarEventRequest,
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> CalendarEventResponse:
    return await calendar_service.create_calendar_event(session, auth, payload)


@router.put("/calendar/events/{event_id}", response_model=CalendarEventResponse)
async def put_calendar_event(
    event_id: str,
    payload: UpdateCalendarEventRequest,
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> CalendarEventResponse:
    return await calendar_service.update_calendar_event(session, auth, event_id, payload)


@router.delete("/calendar/events/{event_id}", response_model=CalendarDeleteResponse)
async def delete_calendar_event(
    event_id: str,
    auth: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db_session),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> CalendarDeleteResponse:
    await calendar_service.delete_calendar_event(session, auth, event_id)
    return CalendarDeleteResponse(status="deleted")
