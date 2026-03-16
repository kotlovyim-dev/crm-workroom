from datetime import UTC, date as dt_date, datetime, time
from uuid import uuid4

from sqlalchemy import Date, DateTime, Index, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(String(36), index=True)
    user_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(320), index=True)
    avatar_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    position: Mapped[str] = mapped_column(String(160))
    level: Mapped[str] = mapped_column(String(32), default="mid")
    role_label: Mapped[str] = mapped_column(String(120), default="Member")
    employment_type: Mapped[str] = mapped_column(String(32), default="full_time")
    hire_date: Mapped[dt_date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_employees_workspace_search", "workspace_id", "last_name", "first_name", "email"),
    )


class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    employee_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    birthday: Mapped[dt_date | None] = mapped_column(Date, nullable=True)
    mobile_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    skype: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    employee_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    issue_activity_email: Mapped[bool] = mapped_column(default=True)
    tracking_activity_push: Mapped[bool] = mapped_column(default=True)
    new_comments_push: Mapped[bool] = mapped_column(default=True)
    silent_hours_enabled: Mapped[bool] = mapped_column(default=False)
    silent_hours_after: Mapped[time | None] = mapped_column(Time, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class VacationBalance(Base):
    __tablename__ = "vacation_balances"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    employee_id: Mapped[str] = mapped_column(String(36), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    vacation_total: Mapped[int] = mapped_column(Integer, default=0)
    vacation_used: Mapped[int] = mapped_column(Integer, default=0)
    sick_leave_total: Mapped[int] = mapped_column(Integer, default=0)
    sick_leave_used: Mapped[int] = mapped_column(Integer, default=0)
    remote_days_total: Mapped[int] = mapped_column(Integer, default=0)
    remote_days_used: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_vacation_balances_employee_year", "employee_id", "year", unique=True),
    )


class TimeOffRequest(Base):
    __tablename__ = "time_off_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(String(36), index=True)
    employee_id: Mapped[str] = mapped_column(String(36), index=True)
    type: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True, default="pending")
    duration_type: Mapped[str] = mapped_column(String(16))
    start_date: Mapped[dt_date] = mapped_column(Date)
    end_date: Mapped[dt_date] = mapped_column(Date)
    time_from: Mapped[time | None] = mapped_column(Time, nullable=True)
    time_to: Mapped[time | None] = mapped_column(Time, nullable=True)
    requested_units: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index(
            "ix_time_off_requests_workspace_timeline",
            "workspace_id",
            "start_date",
            "end_date",
            "status",
            "type",
        ),
    )


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(String(36), index=True)
    title: Mapped[str] = mapped_column(String(255))
    date: Mapped[dt_date] = mapped_column(Date, index=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    duration_label: Mapped[str | None] = mapped_column(String(32), nullable=True)
    type: Mapped[str] = mapped_column(String(32), index=True)
    color_accent: Mapped[str | None] = mapped_column(String(32), nullable=True)
    trend: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_calendar_events_workspace_date_range", "workspace_id", "date", "type"),
    )
