from app.services.calendar import CalendarService
from app.services.employees import EmployeesService
from app.services.profile_settings import ProfileSettingsService
from app.services.vacations import VacationsService


class PeopleService(
    EmployeesService,
    ProfileSettingsService,
    VacationsService,
    CalendarService,
):
    """Backward-compatible facade. Domain logic is split across app/services/*.py."""

    pass
