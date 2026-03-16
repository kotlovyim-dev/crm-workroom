from datetime import date, datetime, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


EmployeeLevel = Literal["junior", "mid", "senior", "lead"]
TimeOffType = Literal["vacation", "sick_leave", "remote"]
TimeOffStatus = Literal["pending", "approved", "rejected", "cancelled"]
DurationType = Literal["days", "hours"]
EventType = Literal["meeting", "holiday", "birthday", "reminder", "other"]


class EmployeeSummary(BaseModel):
    id: str
    workspace_id: str
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    avatar_url: str | None = None
    position: str
    level: str
    role_label: str


class EmployeeActivitySummary(BaseModel):
    employee_id: str
    backlog_tasks: int
    tasks_in_progress: int
    tasks_in_review: int


class EmployeeWithActivity(BaseModel):
    employee: EmployeeSummary
    activity: EmployeeActivitySummary


class EmployeeListResponse(BaseModel):
    items: list[EmployeeSummary]
    page: int
    limit: int
    total: int


class EmployeeActivityListResponse(BaseModel):
    items: list[EmployeeWithActivity]
    page: int
    limit: int
    total: int


class InviteEmployeeRequest(BaseModel):
    email: EmailStr


class InviteEmployeeResponse(BaseModel):
    status: Literal["invited"]
    email: EmailStr


class UserProfile(BaseModel):
    id: str
    workspace_id: str
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    avatar_url: str | None = None
    position: str
    company: str | None = None
    location: str | None = None
    birthday: date | None = None
    mobile_number: str | None = None
    skype: str | None = None


class UserProfileResponse(BaseModel):
    profile: UserProfile


class UpdateUserProfileRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    position: str = Field(min_length=1, max_length=160)
    company: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    birthday: date | None = None
    mobile_number: str | None = Field(default=None, max_length=32)
    skype: str | None = Field(default=None, max_length=120)


class NotificationSettings(BaseModel):
    issue_activity_email: bool
    tracking_activity_push: bool
    new_comments_push: bool
    silent_hours_enabled: bool
    silent_hours_after: time | None = None


class NotificationSettingsResponse(BaseModel):
    settings: NotificationSettings


class VacationBalance(BaseModel):
    employee_id: str
    year: int
    vacation_total: int
    vacation_used: int
    vacation_available: int
    sick_leave_total: int
    sick_leave_used: int
    sick_leave_available: int
    remote_days_total: int
    remote_days_used: int
    remote_days_available: int


class VacationBalanceResponse(BaseModel):
    balance: VacationBalance


class EmployeeBalanceItem(BaseModel):
    employee: EmployeeSummary
    balance: VacationBalance


class VacationBalanceListResponse(BaseModel):
    items: list[EmployeeBalanceItem]
    page: int
    limit: int
    total: int


class TimeOffRequest(BaseModel):
    id: str
    employee_id: str
    type: TimeOffType
    status: TimeOffStatus
    duration_type: DurationType
    start_date: date
    end_date: date
    requested_units: int
    comment: str | None = None
    created_at: datetime
    time_from: time | None = None
    time_to: time | None = None


class TimeOffRequestListResponse(BaseModel):
    items: list[TimeOffRequest]
    page: int
    limit: int
    total: int


class CreateTimeOffRequest(BaseModel):
    type: TimeOffType
    duration_type: DurationType
    start_date: date
    end_date: date
    time_from: time | None = None
    time_to: time | None = None
    comment: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def validate_duration_specific_fields(self) -> "CreateTimeOffRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be greater than or equal to start_date")

        if self.duration_type == "days":
            if self.time_from is not None or self.time_to is not None:
                raise ValueError("time_from and time_to are only allowed for hours duration_type")
            return self

        if self.start_date != self.end_date:
            raise ValueError("hours duration_type requires start_date and end_date to match")
        if self.time_from is None or self.time_to is None:
            raise ValueError("time_from and time_to are required for hours duration_type")
        if self.time_to <= self.time_from:
            raise ValueError("time_to must be later than time_from")
        return self


class CalendarEvent(BaseModel):
    id: str
    workspace_id: str
    title: str
    date: date
    start_time: time
    end_time: time
    duration_label: str | None = None
    type: EventType | str
    color_accent: str | None = None
    trend: str | None = None


class CalendarEventsResponse(BaseModel):
    items: list[CalendarEvent]


class CreateCalendarEventRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    date: date
    start_time: time
    end_time: time
    duration_label: str | None = Field(default=None, max_length=32)
    type: EventType | str
    color_accent: str | None = Field(default=None, max_length=32)
    trend: str | None = Field(default=None, max_length=32)

    @model_validator(mode="after")
    def validate_time_range(self) -> "CreateCalendarEventRequest":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self


class UpdateCalendarEventRequest(CreateCalendarEventRequest):
    pass


class CalendarEventResponse(BaseModel):
    event: CalendarEvent


class CalendarDeleteResponse(BaseModel):
    status: Literal["deleted"]


class QueryPagination(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
