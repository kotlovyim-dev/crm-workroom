# People Service

FastAPI service for workforce data in CRM Workroom.

## Responsibilities

- Employee directory and activity view payloads.
- Self profile read and update.
- Notification preferences.
- Vacation balances and time-off requests.
- Workforce calendar events.

## Local Run

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -e .
```

3. Configure environment in `.env` (see `.env.example`).
4. Apply migrations:

```bash
alembic upgrade head
```

5. Run the app:

```bash
uvicorn app.main:app --reload --port 8082
```
