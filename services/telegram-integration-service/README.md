# Telegram Integration Service

Dedicated Python microservice for CRM Workroom Telegram workflows. The first implemented capability is onboarding phone verification, while the service boundary is intentionally broad enough for future notifications and bot-driven interactions.

## Responsibilities

* Create short-lived verification intents for the Auth service.
* Expose a Telegram webhook endpoint.
* Ask users to share their own Telegram contact.
* Validate the shared contact against the onboarding phone number.
* Generate a 6-digit verification code and return validation status to Auth.
* Provide a natural expansion point for future Telegram notifications.

## Stack

* FastAPI
* aiogram 3
* Redis
* Pydantic Settings

## Local Run

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -e .
```

3. Copy `.env.example` to `.env` and fill in real values. Keep the real bot token only in `.env`.
4. Run the app:

```bash
uvicorn app.main:app --reload --port 8081
```

## Docker Run

From the repository root:

```bash
docker compose up --build telegram-integration-service
```

This starts the service on port `8081` together with Redis.
It reads secrets from `services/telegram-integration-service/.env`.

## Docker Dev Run

For local development with hot reload:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build telegram-integration-service
```

This uses `Dockerfile.dev`, mounts `services/telegram-integration-service` into the container, and runs `uvicorn --reload` without reinstalling Python dependencies on each start.

## Internal Endpoints

* `GET /health`
* `POST /internal/verifications/intents`
* `POST /internal/verifications/check`
* `POST /webhooks/telegram/{secret}`