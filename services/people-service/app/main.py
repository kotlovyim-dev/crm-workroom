from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import health, people


def create_app() -> FastAPI:
    app = FastAPI(title="People Service", version="0.1.0")
    settings = get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(people.router, prefix="/api/v1/people", tags=["people"])
    return app


app = create_app()
