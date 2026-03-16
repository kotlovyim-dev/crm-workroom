# Conventions

## Backend Conventions (Python/FastAPI)
- FastAPI application factory pattern in each service `app/main.py`.
- Router registration with prefixes and tags (for example `services/auth-service/app/main.py`).
- Dependency injection with `Depends(...)` in routers (`services/auth-service/app/routers/auth.py`, `services/people-service/app/routers/people/employees.py`).
- Typed async handlers throughout router layers.

## Layering Pattern
- `models.py`: persistence model definitions.
- `schemas.py`: request/response models.
- `service.py` or `services/`: business logic.
- `routers/`: transport/HTTP boundary.
- `database.py`: DB session factory and dependency.

## Auth and Header Context Pattern
- Auth service exposes `/validate-token` and returns identity headers (`services/auth-service/app/routers/auth.py`).
- Gateway maps upstream identity headers to downstream request headers (`services/api-gateway/nginx.conf`).
- People service accepts identity/workspace context via dependency layer (`services/people-service/app/routers/people/employees.py`).

## Style and Tooling Conventions
- Ruff is configured with `line-length = 100` and rule sets `E,F,I,B,UP` in backend `pyproject.toml` files.
- Python target version is 3.12 in backend `pyproject.toml`.
- Frontend linting uses Next.js ESLint config (`web/eslint.config.mjs`).

## Frontend Conventions
- Client API singleton in `web/src/lib/api/client.ts`.
- Cookie-based auth with Axios `withCredentials`.
- 401 interceptor with retry/refresh guard for auth endpoints.
- Feature modules under `web/src/modules/*` with shared utilities in `web/src/lib`.

## API and Route Naming
- Backend API namespaces use `/api/v1/...` prefixes in both gateway and service routers.
- Health endpoints are simple `/health` and `/health/ready` routes in service apps.

## Runtime and Environment Conventions
- Compose files define production-like and dev variants.
- Services run migrations at startup with `alembic upgrade head` commands.
- Frontend API endpoint configured through `NEXT_PUBLIC_API_BASE_URL`.
