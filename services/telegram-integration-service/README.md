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

3. Copy `.env.example` to `.env` and fill in real values.
4. Run the app:

```bash
uvicorn app.main:app --reload --port 8081
```

## Internal Endpoints

* `GET /healthz`
* `POST /internal/verifications/intents`
* `POST /internal/verifications/check`
* `POST /webhooks/telegram/{secret}`