# Architecture

## High-Level Architecture
CRM Workroom uses a service-oriented backend and a modular Next.js frontend.

- Public entrypoints:
  - Web UI at port 3000 (`docker-compose.yml`).
  - API Gateway at port 8000 (`docker-compose.yml`).
- Internal services:
  - Auth Service on 8080.
  - People Service on 8082.
  - Telegram Integration Service on 8081.

## Backend Request Flow
1. Browser calls gateway (`web` uses `NEXT_PUBLIC_API_BASE_URL`).
2. Gateway routes auth endpoints directly to auth service (`services/api-gateway/nginx.conf`).
3. Gateway protects people endpoints with `auth_request /_validate_jwt` (`services/api-gateway/nginx.conf`).
4. Auth service validates cookies and returns identity headers via `/api/v1/auth/validate-token` (`services/auth-service/app/routers/auth.py`).
5. Gateway forwards `X-User-Id` and `X-Workspace-Id` to people service (`services/api-gateway/nginx.conf`).

## Service Responsibilities
- Auth Service:
  - Login, registration, refresh, logout, session validation in `services/auth-service/app/routers/auth.py`.
  - JWT and cookie session orchestration via router/service/security modules.
- People Service:
  - Domain endpoints for employees/profile/vacations/calendar under `services/people-service/app/routers/people/`.
  - Multi-tenant request context via auth headers and dependencies.
- Telegram Integration Service:
  - Verification intent and code check endpoints in `services/telegram-integration-service/app/main.py`.
  - Bot runtime and delivery mode (polling/webhook) in same module.

## Frontend Architecture
- Next.js App Router layout under `web/src/app/` with grouped routes (dashboard/login/signup).
- Domain-oriented module structure under `web/src/modules/` (`auth`, `dashboard`, `people`).
- Shared UI and layout components under `web/src/components/`.
- API client and query helpers under `web/src/lib/`.

## Data and State Boundaries
- Auth/session state lives in secure cookies managed by auth service and consumed by frontend Axios (`web/src/lib/api/client.ts`).
- People domain data persisted in Postgres (`people-postgres` compose service).
- Telegram verification state is ephemeral in Redis (`telegram-integration-redis` compose service).

## Cross-Cutting Concerns
- CORS is configured per backend service in each `app/main.py`.
- Migrations run on service startup with `alembic upgrade head` in compose commands.
- Gateway enforces request rate limiting (`limit_req_zone`) and custom error mapping in `services/api-gateway/nginx.conf`.
