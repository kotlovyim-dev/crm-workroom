# Stack

## Overview
CRM Workroom is a multi-service web application with a Next.js frontend, Python FastAPI backend services, and Nginx as API gateway.

## Runtimes and Languages
- TypeScript/React frontend in `web/` (`web/package.json`).
- Python 3.12 backend services (`services/auth-service/pyproject.toml`, `services/people-service/pyproject.toml`, `services/telegram-integration-service/pyproject.toml`).
- Nginx gateway config in `services/api-gateway/nginx.conf`.

## Frontend Stack
- Next.js `16.1.6` in `web/package.json`.
- React `19.2.3` and React DOM `19.2.3` in `web/package.json`.
- TypeScript `^5` in `web/package.json`.
- State/data libs: `@tanstack/react-query`, `zustand`, `axios`, `react-hook-form`, `zod` in `web/package.json`.
- Styling libs: `tailwindcss`, `class-variance-authority`, `tailwind-merge` in `web/package.json`.
- UI System: `shadcn`.

## Backend Stack
- FastAPI in all services:
  - `services/auth-service/pyproject.toml`
  - `services/people-service/pyproject.toml`
  - `services/telegram-integration-service/pyproject.toml`
- ASGI server: `uvicorn[standard]` in all three service `pyproject.toml` files.
- ORM and migrations:
  - `sqlalchemy` and `alembic` in auth and people service `pyproject.toml`.
- DB drivers:
  - `asyncpg`, `psycopg2-binary` in auth/people `pyproject.toml`.
- Auth/JWT libs:
  - `PyJWT` in `services/auth-service/pyproject.toml`.
- Telegram integration:
  - `aiogram`, `redis`, `httpx` in `services/telegram-integration-service/pyproject.toml`.

## Data Stores
- PostgreSQL 16 (`people-postgres`) in `docker-compose.yml`.
- Redis 7 (`telegram-integration-redis`) in `docker-compose.yml`.

## Containerization and Local Orchestration
- Docker Compose prod-like setup in `docker-compose.yml`.
- Docker Compose dev setup in `docker-compose.dev.yml`.
- Service images/builds via per-service Dockerfiles:
  - `services/auth-service/Dockerfile`, `services/auth-service/Dockerfile.dev`
  - `services/people-service/Dockerfile`, `services/people-service/Dockerfile.dev`
  - `services/telegram-integration-service/Dockerfile`, `services/telegram-integration-service/Dockerfile.dev`
  - `web/Dockerfile`, `web/Dockerfile.dev`

## Tooling and Quality
- Python lint/format tooling: Ruff configured in each backend `pyproject.toml`.
- Python test framework: pytest configured in root `pytest.ini` and service dev deps.
- Frontend linting: ESLint via `web/package.json` and `web/eslint.config.mjs`.

## Environment and Config Patterns
- Backend service runtime env vars are managed by compose env and `.env` files:
  - `services/auth-service/.env` referenced in `docker-compose.yml`
  - `services/telegram-integration-service/.env` referenced in `docker-compose.yml`
- Frontend API URL is `NEXT_PUBLIC_API_BASE_URL` in both compose files and `web/package.json` scripts.
