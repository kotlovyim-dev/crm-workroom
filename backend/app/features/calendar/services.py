from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.shared.dependencies import AuthContext
from app.features.shared.domain_support import DomainSupport
from app.features.shared.models import CalendarEvent
from app.features.shared.schemas import (
	CalendarEventResponse,
	CalendarEventsResponse,
	CreateCalendarEventRequest,
	UpdateCalendarEventRequest,
)


class CalendarService(DomainSupport):
	async def list_calendar_events(
		self,
		session: AsyncSession,
		auth: AuthContext,
		start_date: date,
		end_date: date,
		event_type: str | None,
	) -> CalendarEventsResponse:
		query = select(CalendarEvent).where(
			CalendarEvent.workspace_id == auth.workspace_id,
			CalendarEvent.date >= start_date,
			CalendarEvent.date <= end_date,
		)
		if event_type:
			query = query.where(CalendarEvent.type == event_type)

		query = query.order_by(CalendarEvent.date.asc(), CalendarEvent.start_time.asc())
		items = list(await session.scalars(query))
		return CalendarEventsResponse(items=[self._calendar_event(item) for item in items])

	async def create_calendar_event(
		self,
		session: AsyncSession,
		auth: AuthContext,
		payload: CreateCalendarEventRequest,
	) -> CalendarEventResponse:
		event = CalendarEvent(
			workspace_id=auth.workspace_id,
			title=payload.title,
			date=payload.date,
			start_time=payload.start_time,
			end_time=payload.end_time,
			duration_label=payload.duration_label,
			type=payload.type,
			color_accent=payload.color_accent,
			trend=payload.trend,
			created_by=auth.user_id,
			updated_by=auth.user_id,
		)
		session.add(event)
		await session.commit()
		await session.refresh(event)
		return CalendarEventResponse(event=self._calendar_event(event))

	async def update_calendar_event(
		self,
		session: AsyncSession,
		auth: AuthContext,
		event_id: str,
		payload: UpdateCalendarEventRequest,
	) -> CalendarEventResponse:
		event = await self._get_workspace_event(session, auth.workspace_id, event_id)
		event.title = payload.title
		event.date = payload.date
		event.start_time = payload.start_time
		event.end_time = payload.end_time
		event.duration_label = payload.duration_label
		event.type = payload.type
		event.color_accent = payload.color_accent
		event.trend = payload.trend
		event.updated_by = auth.user_id

		await session.commit()
		await session.refresh(event)
		return CalendarEventResponse(event=self._calendar_event(event))

	async def delete_calendar_event(
		self,
		session: AsyncSession,
		auth: AuthContext,
		event_id: str,
	) -> None:
		event = await self._get_workspace_event(session, auth.workspace_id, event_id)
		await session.delete(event)
		await session.commit()


__all__ = ["CalendarService"]
