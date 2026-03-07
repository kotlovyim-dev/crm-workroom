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
docker compose up --build web auth-service telegram-integration-service
```

This starts the full local stack, including the Telegram service on port `8081` together with Redis, Auth, PostgreSQL, and the Next.js frontend.
Telegram-related secrets can be passed as shell environment variables before `docker compose up`.

## Docker Dev Run

For local development with hot reload:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

This uses `Dockerfile.dev`, mounts the service source into the container, and runs `uvicorn --reload` without reinstalling Python dependencies on each start.
In dev mode the bot runs through Telegram long polling, so it can answer directly in chat without a public webhook URL.

## Internal Endpoints

* `GET /health`
* `POST /internal/verifications/intents`
* `POST /internal/verifications/check`
* `POST /webhooks/telegram/{secret}`