import os
import sys
from datetime import date, datetime, time
from pathlib import Path

from fastapi.testclient import TestClient


def _bootstrap_service_imports() -> None:
    service_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(service_root))

    for module_name in list(sys.modules):
        if module_name == "app" or module_name.startswith("app."):
            del sys.modules[module_name]


_bootstrap_service_imports()

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")

from app.main import create_app
from app.routers import people
from app.schemas import (
    CalendarEvent,
    CalendarEventResponse,
    CalendarEventsResponse,
    EmployeeActivityListResponse,
    EmployeeActivitySummary,
    EmployeeBalanceItem,
    EmployeeListResponse,
    EmployeeSummary,
    EmployeeWithActivity,
    InviteEmployeeResponse,
    NotificationSettings,
    NotificationSettingsResponse,
    TimeOffRequest,
    TimeOffRequestListResponse,
    UserProfile,
    UserProfileResponse,
    VacationBalance,
    VacationBalanceListResponse,
    VacationBalanceResponse,
)


class FakePeopleService:
    async def list_employees(self, *args, **kwargs):
        employee = EmployeeSummary(
            id="emp-1",
            workspace_id="ws-1",
            first_name="Evan",
            last_name="Yates",
            full_name="Evan Yates",
            email="evan@example.com",
            avatar_url=None,
            position="UI/UX Designer",
            level="senior",
            role_label="Team Lead",
        )
        return EmployeeListResponse(items=[employee], page=1, limit=20, total=1)

    async def list_employee_activity(self, *args, **kwargs):
        employee = EmployeeSummary(
            id="emp-1",
            workspace_id="ws-1",
            first_name="Evan",
            last_name="Yates",
            full_name="Evan Yates",
            email="evan@example.com",
            avatar_url=None,
            position="UI/UX Designer",
            level="senior",
            role_label="Team Lead",
        )
        return EmployeeActivityListResponse(
            items=[
                EmployeeWithActivity(
                    employee=employee,
                    activity=EmployeeActivitySummary(
                        employee_id="emp-1",
                        backlog_tasks=3,
                        tasks_in_progress=4,
                        tasks_in_review=1,
                    ),
                )
            ],
            page=1,
            limit=20,
            total=1,
        )

    async def invite_employee(self, *args, **kwargs):
        return InviteEmployeeResponse(status="invited", email="member@example.com")

    async def get_my_profile(self, *args, **kwargs):
        profile = UserProfile(
            id="emp-1",
            workspace_id="ws-1",
            first_name="Evan",
            last_name="Yates",
            full_name="Evan Yates",
            email="evan@example.com",
            avatar_url=None,
            position="UI/UX Designer",
            company="Cadabra",
            location="NYC, USA",
            birthday=date(1995, 4, 12),
            mobile_number="+123456789",
            skype="evan.yates",
        )
        return UserProfileResponse(profile=profile)

    async def update_my_profile(self, *args, **kwargs):
        return await self.get_my_profile()

    async def get_notification_settings(self, *args, **kwargs):
        settings = NotificationSettings(
            issue_activity_email=True,
            tracking_activity_push=True,
            new_comments_push=True,
            silent_hours_enabled=False,
            silent_hours_after=time(21, 0),
        )
        return NotificationSettingsResponse(settings=settings)

    async def update_notification_settings(self, *args, **kwargs):
        return await self.get_notification_settings()

    async def get_my_vacation_balance(self, *args, **kwargs):
        balance = VacationBalance(
            employee_id="emp-1",
            year=2026,
            vacation_total=16,
            vacation_used=4,
            vacation_available=12,
            sick_leave_total=10,
            sick_leave_used=2,
            sick_leave_available=8,
            remote_days_total=20,
            remote_days_used=5,
            remote_days_available=15,
        )
        return VacationBalanceResponse(balance=balance)

    async def list_vacation_balances(self, *args, **kwargs):
        employee = EmployeeSummary(
            id="emp-1",
            workspace_id="ws-1",
            first_name="Evan",
            last_name="Yates",
            full_name="Evan Yates",
            email="evan@example.com",
            avatar_url=None,
            position="UI/UX Designer",
            level="senior",
            role_label="Team Lead",
        )
        balance = VacationBalance(
            employee_id="emp-1",
            year=2026,
            vacation_total=16,
            vacation_used=4,
            vacation_available=12,
            sick_leave_total=10,
            sick_leave_used=2,
            sick_leave_available=8,
            remote_days_total=20,
            remote_days_used=5,
            remote_days_available=15,
        )
        return VacationBalanceListResponse(
            items=[EmployeeBalanceItem(employee=employee, balance=balance)],
            page=1,
            limit=20,
            total=1,
        )

    async def list_my_time_off_requests(self, *args, **kwargs):
        req = TimeOffRequest(
            id="to-1",
            employee_id="emp-1",
            type="vacation",
            status="pending",
            duration_type="days",
            start_date=date(2026, 3, 18),
            end_date=date(2026, 3, 20),
            requested_units=3,
            comment="Family trip",
            created_at=datetime(2026, 3, 10, 10, 30),
            time_from=None,
            time_to=None,
        )
        return TimeOffRequestListResponse(items=[req], page=1, limit=20, total=1)

    async def create_time_off_request(self, *args, **kwargs):
        return (await self.list_my_time_off_requests()).items[0]

    async def list_vacation_timeline(self, *args, **kwargs):
        return await self.list_my_time_off_requests()

    async def list_calendar_events(self, *args, **kwargs):
        return CalendarEventsResponse(
            items=[
                CalendarEvent(
                    id="ev-1",
                    workspace_id="ws-1",
                    title="Presentation of the new department",
                    date=date(2026, 3, 22),
                    start_time=time(17, 0),
                    end_time=time(19, 0),
                    duration_label="2h",
                    type="meeting",
                    color_accent="blue",
                    trend="up",
                )
            ]
        )

    async def create_calendar_event(self, *args, **kwargs):
        return CalendarEventResponse(event=(await self.list_calendar_events()).items[0])

    async def update_calendar_event(self, *args, **kwargs):
        return await self.create_calendar_event()

    async def delete_calendar_event(self, *args, **kwargs):
        return None


def build_test_client() -> TestClient:
    app = create_app()
    app.dependency_overrides[people.get_employees_service] = lambda: FakePeopleService()
    app.dependency_overrides[people.get_profile_settings_service] = lambda: FakePeopleService()
    app.dependency_overrides[people.get_vacations_service] = lambda: FakePeopleService()
    app.dependency_overrides[people.get_calendar_service] = lambda: FakePeopleService()
    return TestClient(app)


def auth_headers() -> dict[str, str]:
    return {"X-User-Id": "user-1", "X-Workspace-Id": "ws-1"}


def test_get_employees_contract_shape() -> None:
    with build_test_client() as client:
        response = client.get("/api/v1/people/employees", headers=auth_headers())

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"][0]["full_name"] == "Evan Yates"
    assert payload["page"] == 1


def test_profile_contract_shape() -> None:
    with build_test_client() as client:
        response = client.get("/api/v1/people/profile/me", headers=auth_headers())

    assert response.status_code == 200
    payload = response.json()
    assert payload["profile"]["email"] == "evan@example.com"


def test_vacation_request_create_contract_shape() -> None:
    with build_test_client() as client:
        response = client.post(
            "/api/v1/people/vacations/requests",
            headers=auth_headers(),
            json={
                "type": "vacation",
                "duration_type": "days",
                "start_date": "2026-03-18",
                "end_date": "2026-03-20",
                "comment": "Family trip",
            },
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["duration_type"] == "days"
    assert payload["requested_units"] == 3


def test_calendar_events_contract_shape() -> None:
    with build_test_client() as client:
        response = client.get(
            "/api/v1/people/calendar/events?start_date=2026-03-01&end_date=2026-03-31",
            headers=auth_headers(),
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"][0]["type"] == "meeting"
