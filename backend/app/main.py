from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.settings import get_settings
from .features.auth import router as auth_router
from .features.calendar import router as calendar_router
from .features.employees import router as employees_router
from .features.health.routes import router as health_router
from .features.profile import router as profile_router
from .features.telegram import router as telegram_router
from .features.telegram.runtime import setup_telegram_runtime, shutdown_telegram_runtime
from .features.vacations import router as vacations_router


def create_app() -> FastAPI:
    app = FastAPI(title="CRM Backend", version="0.1.0")
    settings = get_settings()

    @app.on_event("startup")
    async def startup() -> None:
        await setup_telegram_runtime(app, settings)

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await shutdown_telegram_runtime(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(telegram_router, prefix="/api/v1/telegram", tags=["telegram"])
    app.include_router(employees_router, prefix="/api/v1", tags=["employees"])
    app.include_router(profile_router, prefix="/api/v1", tags=["profile"])
    app.include_router(vacations_router, prefix="/api/v1", tags=["vacations"])
    app.include_router(calendar_router, prefix="/api/v1", tags=["calendar"])
    return app


app = create_app()
