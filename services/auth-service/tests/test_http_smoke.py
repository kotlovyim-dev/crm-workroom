from fastapi.testclient import TestClient

from app.main import create_app


def test_healthcheck_returns_ok() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_returns_ready() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_validate_token_requires_authentication() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/v1/auth/validate-token")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}