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
from app.database import get_db_session


class _FakeSession:
    async def execute(self, *_args, **_kwargs) -> None:
        return None


async def _fake_get_db_session():
    yield _FakeSession()


def _build_test_client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_db_session] = _fake_get_db_session
    return TestClient(app)


def test_healthcheck_returns_ok() -> None:
    with _build_test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_returns_ready() -> None:
    with _build_test_client() as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_validate_token_requires_authentication() -> None:
    with _build_test_client() as client:
        response = client.get("/api/v1/auth/validate-token")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}