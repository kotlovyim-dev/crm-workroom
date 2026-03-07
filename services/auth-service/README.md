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