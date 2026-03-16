
## Current Test Setup

- Pytest is configured at repository root with `pytest.ini` containing `addopts = --import-mode=importlib`.
- Python test dependencies are declared in `backend/pyproject.toml` optional `dev` extras: `pytest`, `pytest-asyncio`, `ruff`.
- Backend requires Python 3.12 (`backend/pyproject.toml`), which constrains runtime for tests.
- Frontend `web/package.json` defines scripts for `dev`, `build`, `start`, and `lint`, but no `test` script.
- ESLint is configured for frontend quality checks in `web/eslint.config.mjs`.

## How Tests Are Organized Now

- `backend/tests/` exists but is currently empty (`/home/maksym/projects/crm-workroom/backend/tests`).
- No `test_*.py` or `*_test.py` files were found in repository search.
- No frontend test files (`*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.tsx`) were found in repository search.
- No evidence of Playwright/Cypress/Jest/Vitest configuration files in current workspace root snapshot.

## Existing Quality/Verification Mechanisms (Non-Test)

- Backend static quality gate is Ruff config in `backend/pyproject.toml` (`E`, `F`, `I`, `B`, `UP` rulesets).
- Frontend static quality gate is ESLint via Next core-web-vitals + TypeScript configs (`web/eslint.config.mjs`).
- Frontend TypeScript strict mode is enabled (`web/tsconfig.json`), catching many type regressions before runtime.
- Runtime validation is strong on both sides (Pydantic in backend, Zod in frontend), but this does not replace behavior tests.

## Testable Boundaries Present In Code

- Backend service layer has clear unit-test seams: `AuthService` (`backend/app/features/auth/service.py`), `EmployeesService` (`backend/app/features/employees/services.py`), `CalendarService` (`backend/app/features/calendar/services.py`), `VacationsService` (`backend/app/features/vacations/services.py`), `ProfileService` (`backend/app/features/profile/services.py`).
- Backend API layer has integration-test seams through FastAPI routers and DI (`backend/app/features/*/routes.py`, `backend/app/main.py`).
- Backend validation seams are explicit in Pydantic schemas (`backend/app/features/auth/schemas.py`, `backend/app/features/shared/schemas.py`, `backend/app/config/settings.py`).
- Frontend API behavior seams exist in auth API hooks and axios refresh interceptor (`web/src/modules/auth/api/auth.ts`, `web/src/lib/api/client.ts`, `web/src/lib/api/errors.ts`).
- Frontend form/validation seams exist in Zod schemas + RHF forms (`web/src/modules/auth/lib/onboarding-schemas.ts`, `web/src/modules/auth/components/steps/step-one-form.tsx`).
- Frontend state seams exist in Zustand onboarding store (`web/src/modules/auth/store/onboarding-store.ts`).

## Current Gaps

- No executable tests currently exist in either backend or frontend.
- No CI-visible test command is defined at root `package.json` or `web/package.json`.
- No backend test fixtures for DB/session setup (for example, async test database lifecycle) are present.
- No API integration tests covering auth cookie lifecycle (`login`, `refresh`, `logout`, `me`) in `backend/app/features/auth/routes.py`.
- No tests for domain-level invariants in `CreateTimeOffRequest` and `CreateCalendarEventRequest` validators (`backend/app/features/shared/schemas.py`).
- No tests for auth normalization/uniqueness paths (`email.lower()`, `normalize_phone`, conflict outcomes) in `backend/app/features/auth/service.py`.
- No tests for frontend refresh-token retry behavior and request replay in `web/src/lib/api/client.ts`.
- No tests for frontend onboarding validation messages and multi-step flow boundaries.

## Suggested Test Organization (Aligned To Current Structure)

- Backend unit tests:
- `backend/tests/unit/auth/test_service.py` for `AuthService` success/failure paths.
- `backend/tests/unit/shared/test_schemas.py` for Pydantic model validators.
- `backend/tests/unit/employees/test_services.py` for filtering/pagination/query behavior.
- Backend integration tests:
- `backend/tests/integration/auth/test_routes.py` using FastAPI test client and async DB fixtures.
- `backend/tests/integration/calendar/test_routes.py` and `backend/tests/integration/vacations/test_routes.py` for endpoint contracts.
- Frontend unit tests:
- `web/src/modules/auth/lib/onboarding-schemas.test.ts` for schema constraints and custom errors.
- `web/src/lib/api/client.test.ts` for interceptor retry and exclusion rules.
- `web/src/modules/auth/store/onboarding-store.test.ts` for store transitions.
- Frontend component tests:
- `web/src/modules/auth/components/steps/step-one-form.test.tsx` for validation/rendering/submit behavior.

## Minimal Baseline To Add First

- Backend:
- Add `conftest.py` and async DB fixture stack under `backend/tests/`.
- Add smoke tests for `/health/live` and `/health/ready` (`backend/app/features/health/routes.py`).
- Add unit tests for validator edge cases in `backend/app/features/shared/schemas.py`.
- Frontend:
- Add a test runner (`vitest` + `@testing-library/react` or equivalent) and `test` script in `web/package.json`.
- Add schema and API-client behavior tests before component tests.

## Execution Commands That Exist Today

- Backend lint/static checks: Ruff via environment configured from `backend/pyproject.toml`.
- Backend tests command is implied (`pytest`) but currently executes zero tests due empty suite.
- Frontend lint: `npm run lint` in `web/`.
- Frontend tests command: not currently defined.
