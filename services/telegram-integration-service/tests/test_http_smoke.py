from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient

from app.config import get_settings
from app.domain import CheckVerificationCodeResponse, CreateVerificationIntentResponse
from app.main import create_app


class FakeRedis:
    async def ping(self) -> bool:
        return True


class FakeVerificationService:
    async def create_intent(self, payload):
        return CreateVerificationIntentResponse(
            intent_id=uuid4(),
            short_token="short-token",
            bot_url="https://t.me/workroom_verification_bot?start=short-token",
            expires_at=datetime.now(UTC) + timedelta(minutes=5),
        )

    async def validate_code(self, phone_number: str, code: str) -> CheckVerificationCodeResponse:
        return CheckVerificationCodeResponse(
            verified=phone_number == "+380991112233" and code == "123456",
            status="verified" if phone_number == "+380991112233" and code == "123456" else "mismatch",
            expires_at=datetime.now(UTC) + timedelta(minutes=5),
        )


@dataclass
class FakeSettings:
    telegram_webhook_secret: str = "expected-secret"


def build_test_client() -> TestClient:
    app = create_app(enable_runtime=False)
    app.state.redis = FakeRedis()
    app.state.verification_service = FakeVerificationService()
    app.state.bot = SimpleNamespace()
    app.state.dispatcher = SimpleNamespace()
    app.dependency_overrides[get_settings] = lambda: FakeSettings()
    return TestClient(app)


def test_healthcheck_returns_ok() -> None:
    with build_test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_returns_ready() -> None:
    with build_test_client() as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_verification_intent_returns_contract_shape() -> None:
    with build_test_client() as client:
        response = client.post(
            "/internal/verifications/intents",
            json={"phone_number": "+380991112233"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["short_token"] == "short-token"
    assert payload["bot_url"].startswith("https://t.me/")


def test_check_verification_code_returns_verification_result() -> None:
    with build_test_client() as client:
        response = client.post(
            "/internal/verifications/check",
            json={"phone_number": "+380991112233", "code": "123456"},
        )

    assert response.status_code == 200
    assert response.json()["verified"] is True


def test_webhook_rejects_wrong_secret() -> None:
    with build_test_client() as client:
        response = client.post("/webhooks/telegram/wrong-secret", json={})

    assert response.status_code == 404
    assert response.json() == {"detail": "Webhook not found"}