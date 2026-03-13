import os
import sys
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


def test_healthcheck_returns_ok() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_employees_requires_auth_context() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/v1/people/employees")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing auth context"}
