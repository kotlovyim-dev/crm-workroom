# Backend

Local monolithic backend entrypoint for CRM Workroom.

## Run locally

1. Copy env:

```bash
cp backend/.env.example backend/.env
```

2. Install dependencies in your local Python env:

```bash
pip install -e ./backend
```

3. Start backend (without Docker):

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docker is now used only for Redis in project compose files.

Implemented backend features:
- `app/features/auth/*`
- `app/features/telegram/*`
- `app/features/employees/*`
- `app/features/profile/*`
- `app/features/vacations/*`
- `app/features/calendar/*`
