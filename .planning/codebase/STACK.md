# STACK

## Monolith Shape (Current)

- Backend is a modular monolith in `backend/app/` with feature slices:
  - `backend/app/features/auth/`
  - `backend/app/features/telegram/`
  - `backend/app/features/employees/`
  - `backend/app/features/profile/`
  - `backend/app/features/vacations/`
  - `backend/app/features/calendar/`
- Single FastAPI entrypoint and router composition in `backend/app/main.py`.
- Telegram verification is no longer a standalone service folder; it runs inside the backend process (`backend/app/features/telegram/runtime.py`).

## Runtime Stack

### Backend Runtime

- Python `>=3.12` from `backend/pyproject.toml`.
- ASGI app: FastAPI + Uvicorn (`backend/app/main.py`, `backend/pyproject.toml`).
- HTTP client: `httpx` used by auth module for telegram verification calls (`backend/app/features/auth/telegram_client.py`).
- ORM and DB driver:
  - SQLAlchemy async (`backend/app/db/session.py`)
  - `asyncpg` driver (`backend/pyproject.toml`)
- Settings/config: Pydantic Settings (`backend/app/config/settings.py`).
- Auth/tokening:
  - PyJWT (`backend/app/features/auth/security.py`)
  - password hashing via `hashlib.pbkdf2_hmac` (`backend/app/features/auth/security.py`)
- Redis client: `redis` asyncio API (`backend/app/features/telegram/runtime.py`, `backend/app/features/telegram/storage.py`).
- Telegram bot runtime: `aiogram` (`backend/app/features/telegram/bot.py`, `backend/app/features/telegram/runtime.py`).

### Frontend Runtime

- Next.js `16.1.6`, React `19.2.3`, TypeScript `^5` (`web/package.json`).
- Axios client with cookies enabled (`web/src/lib/api/client.ts`).
- TanStack Query, React Hook Form, Zod, Zustand (`web/package.json`).
- Tailwind CSS v4 toolchain (`web/package.json`, `web/postcss.config.mjs`).

### Local Infra Runtime

- Docker Compose currently defines Redis only (`docker-compose.yml`).
- Redis image: `redis:7-alpine` with `6379:6379` port mapping (`docker-compose.yml`).
- Backend README confirms Docker is now used only for Redis (`backend/README.md`).

## API Surface and Composition

- Backend app includes routers in `backend/app/main.py`:
  - `/health`
  - `/api/v1/auth`
  - `/api/v1/telegram`
  - `/api/v1` for employees/profile/vacations/calendar
- CORS origin is driven by `frontend_url` setting (`backend/app/main.py`, `backend/app/config/settings.py`).
- Frontend API base URL comes from `NEXT_PUBLIC_API_BASE_URL` with fallback `http://localhost:8000` (`web/src/lib/api/client.ts`).

## Data and State Stack

- Primary persistent store: PostgreSQL via `DATABASE_URL` (`backend/app/config/settings.py`, `backend/app/db/session.py`, `backend/.env.example`).
- Ephemeral verification/session store: Redis via `REDIS_URL` (`backend/app/config/settings.py`, `backend/app/features/telegram/runtime.py`).
- JWT access token is stateless; refresh tokens are persisted hashed in DB (`backend/app/features/auth/security.py`, `backend/app/features/auth/service.py`).

## Dependency Manifests

- Root package metadata: `package.json` (minimal top-level JS deps only).
- Backend dependency source of truth: `backend/pyproject.toml`.
- Frontend dependency source of truth: `web/package.json`.

## Operations and Run Entry Points

- Backend dev run command documented in `backend/README.md`:
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Frontend scripts in `web/package.json`:
  - `dev`, `build`, `start`, `lint`
- Frontend env documentation in `web/README.md` (`NEXT_PUBLIC_API_BASE_URL`).

## Testing and Quality Tooling

- Backend test tooling in `backend/pyproject.toml` optional deps:
  - `pytest`, `pytest-asyncio`
  - `ruff`
- Pytest configuration exists at repo root: `pytest.ini`.
