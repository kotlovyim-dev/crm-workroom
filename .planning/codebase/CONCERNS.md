# Technical Concerns

## Executive Risk Summary
- `P0`: Database lifecycle is incomplete. Alembic is declared but no migration/config files are present, and no runtime schema bootstrap exists. A fresh database can fail on first auth/domain queries.
- `P0`: Domain endpoints trust caller-supplied identity headers directly; if backend is reachable directly (not only behind trusted proxy), auth context can be spoofed.
- `P1`: Test and automation coverage is effectively absent (`backend/tests/` empty, no frontend tests, no CI workflow), increasing regression and incident risk.
- `P1`: Security defaults remain development-grade (`jwt_secret_key` fallback and insecure cookie default), making misconfiguration in non-dev environments likely.
- `P2`: Product/docs/app-state drift is growing (README still claims broader running stack, dead frontend nav routes, placeholder invite behavior), which can cause planning and delivery errors.

## Security Concerns

### Header-based trust boundary is weak (`P0`)
- Downstream domain APIs accept identity solely from request headers via `get_auth_context` (`backend/app/features/shared/dependencies.py`).
- Header values (`X-User-Id`, `X-Workspace-Id`) are consumed by employees/profile/vacations/calendar routes (`backend/app/features/employees/routes.py`, `backend/app/features/profile/routes.py`, `backend/app/features/vacations/routes.py`, `backend/app/features/calendar/routes.py`).
- Risk: if requests can bypass a trusted gateway/auth_request layer, callers can impersonate users/workspaces.

### Insecure-by-default auth settings (`P1`)
- JWT secret defaults to weak placeholder (`jwt_secret_key = "change-me"`) in `backend/app/config/settings.py` and `.env` template (`backend/.env.example`).
- Cookies default to insecure transport (`cookie_secure = False`) in `backend/app/config/settings.py` and `.env` template.
- Risk: production-like deployments can accidentally run with weak secret/cookie settings.

### Broad token decode exception handling (`P2`)
- Auth context validation catches generic `Exception` around token decode in `backend/app/features/auth/routes.py`.
- Risk: reduced diagnostics and potentially masking specific token failure modes.

## Data Integrity and Migration Leftovers

### Missing migration runtime (`P0`)
- Alembic dependency exists in `backend/pyproject.toml`.
- No migration files/config are present (no `alembic.ini`, no migration directories), and no `create_all` bootstrap path exists in runtime code (`backend/app/main.py`, `backend/app/db/base.py`).
- Risk: schema drift and failed startup/requests on new environments.

### Relational integrity not enforced at DB level for shared domain models (`P1`)
- Multiple shared tables use string IDs without foreign keys (`backend/app/features/shared/models.py`): `Employee.user_id`, `EmployeeProfile.employee_id`, `NotificationSettings.employee_id`, `TimeOffRequest.employee_id`, `CalendarEvent.workspace_id`, etc.
- Risk: orphan rows and cross-workspace consistency defects under failures/manual data operations.

### Auto-create side effects in read/list flows (`P2`)
- Vacation balances are created lazily during list/read paths and then committed (`backend/app/features/vacations/services.py`, `backend/app/features/shared/domain_support.py`).
- Risk: read endpoints mutate state and can create hidden write load/contention.

## Reliability and Operational Concerns

### Service runtime/docs mismatch (`P1`)
- Root `docker-compose.yml` now provisions only Redis.
- Root README still describes broader local endpoints and backend startup assumptions that imply fuller orchestration (`README.md`).
- Risk: onboarding friction, failed local runs, and deployment playbook confusion.

### Telegram runtime dependency coupling (`P2`)
- Telegram verification service is initialized on app startup and readiness depends on Redis (`backend/app/features/telegram/runtime.py`, `backend/app/features/telegram/routes.py`).
- Risk: partial outages in Redis can degrade auth/signup verification without graceful degradation strategy documented.

## Technical Debt and Product Drift

### Frontend navigation advertises non-existent routes (`P1`)
- Sidebar includes `/projects`, `/messanger`, `/info-portal` (`web/src/config/sidebar-nav.config.ts`).
- Only selected dashboard route files exist; several advertised areas are absent under `web/src/app/(dashboard)/`.
- Risk: broken navigation and user-facing dead ends.

### Naming/contract inconsistencies (`P2`)
- Typo persists as `Messanger` and `/messanger` in navigation config.
- Risk: compounding API/route naming debt and future migration churn.

### Placeholder business operation (`P2`)
- Employee invite returns static `"invited"` response without persistence/workflow (`backend/app/features/employees/services.py`).
- Risk: false-positive UX success and hidden backlog in onboarding/team-management flows.

## Testing and Verification Gaps

### No backend tests in repository (`P0`)
- `backend/tests/` is empty.
- Risk: auth/session, Telegram verification, and domain logic regressions ship undetected.

### No frontend automated tests (`P1`)
- No unit/integration/e2e test files or test scripts in `web/package.json`.
- Risk: route guards, session refresh, and onboarding flow breakages are only caught manually.

### No CI workflow in repo (`P1`)
- No `.github/workflows/*` detected.
- Risk: no enforced lint/test gates before merge/deploy.

## Priority Recommendations

### `Now (P0)`
- Add DB lifecycle support: introduce Alembic config + initial migrations for existing models and documented migration runbook.
- Enforce trusted edge for identity headers: either make backend private behind gateway or cryptographically verify propagated auth context.
- Create minimum regression suite:
	- backend tests for login/register/refresh/logout and one domain endpoint per module,
	- smoke API health/readiness checks,
	- CI job that runs lint + tests.

### `Next (P1)`
- Harden security defaults: remove weak secret defaults, fail fast when secrets are unset in non-dev, require secure cookies outside local dev.
- Align docs/runtime: update root `README.md` to current deploy shape and explicit service startup prerequisites.
- Reconcile frontend nav with implemented routes or provide feature-flag/placeholder handling to avoid dead links.

### `Later (P2)`
- Replace placeholder flows (employee invite) with persisted workflow and delivery/audit trail.
- Add observability around token decode and Telegram verification failure modes.
- Plan naming cleanup (`messanger` -> `messenger`) with route compatibility strategy.
