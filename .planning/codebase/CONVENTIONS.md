## Architecture And Module Layout

- Backend follows a feature-first FastAPI structure under `backend/app/features/*` with per-feature `routes.py` + `services.py` (+ optional `schemas.py` / runtime helpers).
- App composition is centralized in `backend/app/main.py` via `create_app()` and `app.include_router(...)` calls.
- Database setup is centralized in `backend/app/db/session.py` and SQLAlchemy models live in feature-level model modules (`backend/app/features/auth/models.py`, `backend/app/features/shared/models.py`).
- Frontend uses Next.js App Router under `web/src/app/**` and domain modules under `web/src/modules/**`.
- Shared frontend UI primitives are under `web/src/components/ui/**`, with app shell layout parts under `web/src/components/layout/**`.
- Frontend API access is split between shared API infrastructure (`web/src/lib/api/*`) and module-level API wrappers (`web/src/modules/auth/api/*`).

## Style Patterns

- Python typing is pervasive: `str | None`, `tuple[...]`, `dict[str, str]`, and async return annotations are used throughout (`backend/app/features/auth/routes.py`, `backend/app/features/auth/service.py`).
- Python code uses dataclasses for small auth context carriers (`backend/app/features/auth/routes.py`, `backend/app/features/shared/dependencies.py`).
- SQLAlchemy 2 typed ORM style is used: `Mapped[...]`, `mapped_column(...)`, explicit indexes (`backend/app/features/shared/models.py`).
- Backend imports are grouped stdlib/third-party/local and generally match Ruff import sorting intent (`backend/pyproject.toml`, `backend/app/features/auth/service.py`).
- Frontend TypeScript is strict (`web/tsconfig.json`: `"strict": true`) and uses type-only imports where practical (`web/src/lib/utils.ts`, `web/src/modules/auth/api/auth.ts`).
- Frontend uses alias imports (`@/*`) rather than deep relative imports (`web/tsconfig.json`, many files in `web/src/modules/**`).
- React code style favors function components, hooks, and colocated schemas/types for forms (`web/src/modules/auth/components/steps/step-one-form.tsx`, `web/src/modules/auth/lib/onboarding-schemas.ts`).
- Semicolon usage is inconsistent in frontend: some files are no-semicolon (`web/src/modules/auth/components/steps/step-one-form.tsx`), others include semicolons (`web/src/app/(dashboard)/dashboard/page.tsx`).
- Indentation is inconsistent in backend feature routes/services: tabs appear in some modules (`backend/app/features/employees/routes.py`, `backend/app/features/calendar/routes.py`) while most files use spaces.

## Naming Conventions

- Backend route handler names generally use verb-prefixed, descriptive snake_case (`login`, `refresh_session`, `get_calendar_events`, `invite_employee`).
- Backend DI factory functions follow `get_<feature>_service` (`backend/app/features/auth/routes.py`, `backend/app/features/employees/routes.py`, `backend/app/features/calendar/routes.py`).
- Backend DTO classes use PascalCase with Request/Response suffixes (`RegisterWorkspaceRequest`, `CalendarEventsResponse`, `InviteEmployeeResponse`).
- Backend literals capture constrained business values (`TeamSize`, `TimeOffType`, `DurationType`) in `backend/app/features/auth/schemas.py` and `backend/app/features/shared/schemas.py`.
- Frontend hooks and state selectors follow `useX` naming (`useSessionQuery`, `useInitTelegramVerificationMutation`, `useOnboardingStore`).
- Frontend files/components use kebab-case filenames and PascalCase exports (`web/src/modules/auth/components/steps/step-one-form.tsx` exports `StepOneForm`).
- Query keys are centralized and named by domain (`web/src/lib/query-keys.ts` usage in `web/src/modules/auth/api/auth.ts`).

## Error Handling Conventions

- Backend uses `HTTPException` for domain/API errors with explicit status codes and user-facing `detail` messages (`backend/app/features/auth/service.py`, `backend/app/features/telegram/routes.py`, `backend/app/features/shared/domain_support.py`).
- Auth/session path consistently maps invalid/missing auth to `401` (`backend/app/features/auth/routes.py`, `backend/app/features/shared/dependencies.py`).
- Not-found resources map to `404` from shared domain helpers (`backend/app/features/shared/domain_support.py`).
- Conflict checks map to `409` for duplicate email/phone (`backend/app/features/auth/service.py`).
- A broad exception catch exists around JWT decode in auth context resolution (`backend/app/features/auth/routes.py`), which prioritizes stable `401` responses but may hide token parse nuances.
- Frontend normalizes server error payloads with `getApiErrorMessage(...)` and fallback text (`web/src/lib/api/errors.ts`; consumed in `web/src/modules/auth/components/steps/step-one-form.tsx`).
- Frontend API client includes a single-flight refresh retry interceptor for `401` responses, with protected endpoint exclusions (`web/src/lib/api/client.ts`).

## Validation Conventions

- Backend env/config validation uses Pydantic settings validators (`backend/app/config/settings.py`).
- Backend request validation combines declarative field constraints (`Field(min_length=..., max_length=...)`) with model-level invariants via `@model_validator(mode="after")` (`backend/app/features/shared/schemas.py`).
- Backend query parameter validation uses FastAPI `Query` constraints (pagination bounds, year/month ranges) (`backend/app/features/vacations/routes.py`, `backend/app/features/employees/routes.py`).
- Backend normalizes identity input before persistence checks (`email.lower()`, `normalize_phone(...)`) (`backend/app/features/auth/service.py`).
- Frontend form validation uses Zod schemas with custom messages and refinements (`web/src/modules/auth/lib/onboarding-schemas.ts`).
- Frontend form runtime uses `react-hook-form` + `zodResolver` for typed validation pipeline (`web/src/modules/auth/components/steps/step-one-form.tsx`).
- Frontend onboarding state updates are typed and partial-safe with Zustand (`web/src/modules/auth/store/onboarding-store.ts`).

## Organization Patterns (How Code Is Structured Today)

- Backend route files are thin adapters that delegate business logic to service classes (`backend/app/features/*/routes.py` -> `services.py`).
- Reusable cross-feature logic is extracted into `DomainSupport` and auth dependencies (`backend/app/features/shared/domain_support.py`, `backend/app/features/shared/dependencies.py`).
- Backend response mapping from ORM objects to DTOs is explicit and service-owned (`_build_auth_response`, `_employee_summary`, `_calendar_event`).
- Frontend modules keep API, types, lib helpers, and components grouped by domain (`web/src/modules/auth/{api,components,lib,store,types}`).
- Frontend route files in `web/src/app/**/page.tsx` are mostly composition wrappers over module views/components (`web/src/app/(dashboard)/dashboard/page.tsx`).

## Convention Gaps And Drift

- Formatting drift exists in backend due to mixed indentation style (tabs in some feature files, spaces elsewhere).
- Frontend statement termination style (semicolon/no-semicolon) is mixed and currently not standardized by visible formatter config.
- Some backend exception handling is broad (`except Exception`) and could be narrowed for better observability while preserving API behavior.
- No explicit repository-level documented style guide is present; conventions are inferred from implementation patterns.
