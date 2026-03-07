# Auth Service

FastAPI microservice for CRM Workroom authentication and workspace onboarding.

## Responsibilities

* Login with email and password.
* Workspace registration with Telegram phone verification.
* JWT access token issuance via httpOnly cookies.
* Refresh token rotation and logout.
* Owner user and pending invitation persistence.

## Local Run

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -e .
```

3. Run the app:

```bash
uvicorn app.main:app --reload --port 8080
```

The default database is SQLite for local development. Set `DATABASE_URL` to a PostgreSQL URL when infrastructure is ready.

## Docker Run

From the repository root:

```bash
docker compose up --build web auth-service telegram-integration-service
```

This starts:

* `web` on `http://localhost:3000`
* `auth-service` on `http://localhost:8080`
* `telegram-integration-service` on `http://localhost:8081`
* PostgreSQL for Auth on `localhost:5432`
* Redis for Telegram verification on `localhost:6379`

The Compose stack wires Auth to PostgreSQL and the Telegram service automatically.

## Docker Dev Run

For hot reload across frontend and Python services:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```