from fastapi import APIRouter

from app.routers.people import calendar, employees, profile_settings, vacations
from app.routers.people.calendar import get_calendar_service
from app.routers.people.employees import get_employees_service
from app.routers.people.profile_settings import get_profile_settings_service
from app.routers.people.vacations import get_vacations_service

router = APIRouter()
router.include_router(employees.router)
router.include_router(profile_settings.router)
router.include_router(vacations.router)
router.include_router(calendar.router)

__all__ = [
	"get_calendar_service",
	"get_employees_service",
	"get_profile_settings_service",
	"get_vacations_service",
	"router",
]
