# CRM Workroom Structure

## Repository Root

Top-level layout in `/home/maksym/projects/crm-workroom`:

- `backend/` - FastAPI modular monolith and domain logic.
- `web/` - Next.js frontend app.
- `design/` - Pencil design sources (`.pen`).
- `docs/` - additional documentation artifacts.
- `docker-compose.yml` - local infra (currently Redis service).
- `README.md` - product and implementation overview.
- `.planning/codebase/` - planning and codebase analysis docs.

## Backend Structure (`backend/`)

## Entrypoints and Configuration

- `backend/app/main.py` - FastAPI app construction, middleware, startup/shutdown hooks, router registration.
- `backend/app/config/settings.py` - environment-backed settings (`database_url`, `redis_url`, `frontend_url`, Telegram settings).
- `backend/pyproject.toml` - backend dependencies and tool config.

## Database Layer

- `backend/app/db/base.py` - SQLAlchemy declarative base.
- `backend/app/db/session.py` - async engine and session dependency (`get_db_session`).

## Feature Modules

### `backend/app/features/auth/`

- `models.py` - `Workspace`, `User`, `Invitation`, `RefreshSession` tables.
- `schemas.py` - request/response contracts.
- `routes.py` - auth HTTP API (`/login`, `/register-workspace`, `/refresh`, `/logout`, `/me`, `/validate-token`).
- `service.py` - login/register/session lifecycle and cookie/session logic.
- `security.py` - JWT/password/hash utilities.
- `telegram_client.py` - HTTP adapter from auth domain to telegram verification endpoints.

### `backend/app/features/telegram/`

- `routes.py` - health/readiness, internal verification intent/check, webhook ingestion.
- `runtime.py` - app startup/shutdown wiring for Redis + bot dispatcher lifecycle.
- `service.py` - verification intent/code domain operations.
- `storage.py` - Redis-backed verification state abstraction.
- `bot.py` - aiogram dispatcher/update handling.
- `domain.py` - telegram verification DTOs.

### `backend/app/features/employees/`

- `routes.py` - employees list/activity/invite endpoints.
- `services.py` - employees business logic and persistence interactions.

### `backend/app/features/profile/`

- `routes.py` - profile read/update and notification settings endpoints.
- `services.py` - profile and notification domain behavior.

### `backend/app/features/vacations/`

- `routes.py` - balances, requests, and timeline endpoints.
- `services.py` - vacation business rules.

### `backend/app/features/calendar/`

- `routes.py` - calendar event query/create/update/delete endpoints.
- `services.py` - calendar event domain logic.

### `backend/app/features/shared/`

- `dependencies.py` - shared auth context extraction (`X-User-Id`, `X-Workspace-Id`).
- `models.py` - shared domain tables (`Employee`, `EmployeeProfile`, `NotificationSettings`, `VacationBalance`, `TimeOffRequest`, `CalendarEvent`).
- `schemas.py` - shared API schemas used by multiple features.
- `domain_support.py` - common domain helper utilities.

### `backend/app/features/health/`

- `routes.py` - service health and DB readiness endpoints.

## Backend Flow Topology

- HTTP ingress: `backend/app/main.py` -> feature routers.
- Auth guard for non-auth domains: `backend/app/features/shared/dependencies.py`.
- Service layer execution: feature `services.py`.
- Persistence access: `backend/app/db/session.py` + SQLAlchemy models in `auth/models.py` and `shared/models.py`.
- External state integration: Redis + Telegram runtime via `backend/app/features/telegram/`.

## Frontend Structure (`web/`)

## Entrypoints and App Shell

- `web/src/app/layout.tsx` - root HTML/body layout and React Query provider.
- `web/src/app/page.tsx` - root redirect to `/login`.
- `web/src/components/providers/query-provider.tsx` - QueryClient setup.

## Route Groups (`web/src/app/`)

Auth and public routes:

- `web/src/app/login/page.tsx`
- `web/src/app/signup/page.tsx`
- `web/src/app/signup/[step]/page.tsx`
- `web/src/app/signup/success/page.tsx`

Dashboard route group:

- `web/src/app/(dashboard)/layout.tsx` - authenticated shell (`SessionGuard`, `Sidebar`, `Topbar`).
- `web/src/app/(dashboard)/dashboard/page.tsx`
- `web/src/app/(dashboard)/dashboard/nearest-events/page.tsx`

Placeholder dashboard domains currently empty:

- `web/src/app/(dashboard)/calendar/`
- `web/src/app/(dashboard)/employees/`
- `web/src/app/(dashboard)/profile/`
- `web/src/app/(dashboard)/vacations/`

## Frontend Domain Modules

### `web/src/modules/auth/`

- `api/auth.ts` - auth queries/mutations and API request functions.
- `api/client.ts` - auth API client re-export.
- `components/session-guard.tsx` - redirects unauthenticated users.
- `components/guest-guard.tsx` - prevents authenticated users from entering guest flows.
- `components/steps/*.tsx` - onboarding step forms.
- `store/onboarding-store.ts` - client onboarding state.
- `lib/onboarding.ts`, `lib/onboarding-schemas.ts` - onboarding mapping and validation.

### `web/src/modules/dashboard/`

- `components/views/dashboard-view.tsx` - main dashboard composition.
- `components/views/nearest-events-view.tsx` - nearest-events screen composition.
- `components/ui/*.tsx` - dashboard-specific cards, sections, widgets.
- `types/events.ts` - dashboard event types.

### Shared Frontend Foundations

- `web/src/components/layout/` - shared shell components (`sidebar.tsx`, `topbar.tsx`).
- `web/src/components/ui/` - reusable UI primitives.
- `web/src/lib/api/client.ts` - base Axios client and 401 refresh retry interceptor.
- `web/src/lib/api/errors.ts` - API error parsing.
- `web/src/lib/query-keys.ts` - centralized React Query keys.
- `web/src/config/sidebar-nav.config.ts` - sidebar information architecture.

## Cross-Boundary Request Shape

Frontend to backend calls use cookie-based auth and Axios `withCredentials`:

- API base and interceptors: `web/src/lib/api/client.ts`.
- Auth endpoints consumed from frontend: `/api/v1/auth/*` in `web/src/modules/auth/api/auth.ts`.

Backend issues/validates cookies in `backend/app/features/auth/routes.py` and `backend/app/features/auth/service.py`, then domain APIs rely on header-derived auth context (`backend/app/features/shared/dependencies.py`).

## Non-Code Assets and Planning

- `design/crm.pen` and `design/profile.pen` store source design artifacts.
- `.planning/codebase/STACK.md` holds stack-specific planning context.
- `.planning/codebase/ARCHITECTURE.md` and `.planning/codebase/STRUCTURE.md` capture architecture and structure analysis.
