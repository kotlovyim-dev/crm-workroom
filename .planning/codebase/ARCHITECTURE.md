# CRM Workroom Architecture

## Architecture Style

The repository currently implements a **modular monolith** backend with feature-scoped modules under `backend/app/features/` and a single FastAPI app entrypoint in `backend/app/main.py`.

- Runtime process model: one Python service process hosting all backend feature routers.
- Feature isolation model: per-feature `routes.py`, `services.py`, and domain schemas/models.
- Shared cross-feature contracts: `backend/app/features/shared/`.

This gives microservice-like code boundaries inside one deployable service.

## Runtime Boundaries

## Frontend Boundary

The frontend is a separate Next.js App Router application in `web/`.

- Root layout and global providers: `web/src/app/layout.tsx`.
- Browser API access uses Axios with credentials in `web/src/lib/api/client.ts`.
- Auth-specific API layer lives in `web/src/modules/auth/api/auth.ts`.

The frontend boundary ends at HTTP calls to backend endpoints such as `/api/v1/auth/*`.

## Backend Boundary

The backend boundary starts at FastAPI router registration in `backend/app/main.py`.

Registered route groups:

- Health: `backend/app/features/health/routes.py` -> `/health`.
- Auth: `backend/app/features/auth/routes.py` -> `/api/v1/auth/*`.
- Telegram: `backend/app/features/telegram/routes.py` -> `/api/v1/telegram/*`.
- Employees/Profile/Vacations/Calendar: feature routes under `/api/v1/*`.

Persistent dependencies:

- PostgreSQL via SQLAlchemy async session factory in `backend/app/db/session.py`.
- Redis for Telegram verification runtime/session state via `backend/app/features/telegram/runtime.py` and `backend/app/features/telegram/storage.py`.

## Infrastructure Boundary

Current local orchestration in `docker-compose.yml` defines Redis explicitly. PostgreSQL is expected through `database_url` from environment (`backend/app/config/settings.py`).

## Feature Layout

Backend features are organized as vertical slices:

- `backend/app/features/auth/`: login, registration, session/refresh cookies, token validation.
- `backend/app/features/telegram/`: verification intents, code checks, webhook/polling runtime.
- `backend/app/features/employees/`: employee list/activity/invite endpoints.
- `backend/app/features/profile/`: profile and notification settings endpoints.
- `backend/app/features/vacations/`: balances, requests, timeline.
- `backend/app/features/calendar/`: event CRUD and range queries.
- `backend/app/features/shared/`: auth header dependency, shared SQL models, shared response/request schemas.

Frontend features are grouped by business domain:

- `web/src/modules/auth/`: auth UI, onboarding flow, session guards, auth API hooks.
- `web/src/modules/dashboard/`: dashboard views/components and event types.
- `web/src/modules/people/`: present as domain container (minimal implementation currently).
- `web/src/components/layout/`: shell-level `Sidebar` and `Topbar`.
- `web/src/components/ui/`: reusable UI primitives.

## Entrypoints

Primary app entrypoints:

- Backend ASGI app: `backend/app/main.py` (`app = create_app()`).
- Backend settings source: `backend/app/config/settings.py`.
- Frontend root route redirect: `web/src/app/page.tsx` (`/` -> `/login`).
- Frontend dashboard shell: `web/src/app/(dashboard)/layout.tsx`.

User-facing route entrypoints currently wired:

- `web/src/app/login/page.tsx`.
- `web/src/app/signup/page.tsx`.
- `web/src/app/signup/[step]/page.tsx`.
- `web/src/app/signup/success/page.tsx`.
- `web/src/app/(dashboard)/dashboard/page.tsx`.
- `web/src/app/(dashboard)/dashboard/nearest-events/page.tsx`.

Placeholder route directories exist but are currently empty:

- `web/src/app/(dashboard)/calendar/`
- `web/src/app/(dashboard)/employees/`
- `web/src/app/(dashboard)/profile/`
- `web/src/app/(dashboard)/vacations/`

## Request and Data Flow

## Auth Session Flow

1. Browser requests login/signup through UI in `web/src/modules/auth/components/`.
2. Frontend mutation calls in `web/src/modules/auth/api/auth.ts` hit backend `/api/v1/auth/*`.
3. Backend auth router (`backend/app/features/auth/routes.py`) delegates to `AuthService` in `backend/app/features/auth/service.py`.
4. `AuthService` reads/writes `User`, `Workspace`, `RefreshSession` in `backend/app/features/auth/models.py` via `AsyncSession` from `backend/app/db/session.py`.
5. Backend sets `access_token` and `refresh_token` cookies in auth routes.
6. Frontend Axios interceptor in `web/src/lib/api/client.ts` auto-calls `/api/v1/auth/refresh` on 401 and retries original request.
7. Protected frontend layout uses `SessionGuard` (`web/src/modules/auth/components/session-guard.tsx`) which calls `/api/v1/auth/me`.

## Telegram Verification Flow

1. Frontend calls `/api/v1/auth/init-telegram-verification` and `/api/v1/auth/verify-telegram-code`.
2. `AuthService` uses HTTP client adapter `backend/app/features/auth/telegram_client.py`.
3. Telegram feature endpoints in `backend/app/features/telegram/routes.py` create/check intents.
4. Verification state is stored in Redis through `backend/app/features/telegram/storage.py` and `backend/app/features/telegram/service.py`.
5. Bot runtime is initialized at app startup by `setup_telegram_runtime` in `backend/app/features/telegram/runtime.py`.

## Domain API Flow (Employees/Profile/Vacations/Calendar)

1. Request enters feature router in `backend/app/features/*/routes.py`.
2. Auth context is derived from forwarded headers (`X-User-Id`, `X-Workspace-Id`) by `backend/app/features/shared/dependencies.py`.
3. Router delegates to feature service in `services.py`.
4. Services read/write shared domain tables from `backend/app/features/shared/models.py`.
5. Responses are serialized with shared/domain schemas in `backend/app/features/shared/schemas.py`.

## Persistence Model

- Authentication and workspace identity tables: `backend/app/features/auth/models.py`.
- People/profile/vacation/calendar tables: `backend/app/features/shared/models.py`.
- SQLAlchemy base metadata root: `backend/app/db/base.py`.

## Operational Notes

- CORS origin is constrained to configured frontend URL in `backend/app/main.py`.
- Telegram runtime can be disabled if `telegram_bot_token` is empty (`backend/app/features/telegram/runtime.py`).
- Redis is explicitly provisioned in `docker-compose.yml`; DB/other services are externally configured through environment.
