# Structure

## Repository Layout
- Root orchestration and docs:
  - `docker-compose.yml`
  - `docker-compose.dev.yml`
  - `README.md`
  - `pytest.ini`
- Service code in `services/`.
- Frontend app in `web/`.
- Design assets in `design/`.

## Backend Service Layout
- `services/api-gateway/`
  - `nginx.conf` route/auth/rate-limit policy.
  - `Dockerfile` image definition.
- `services/auth-service/`
  - `app/` runtime source (`main.py`, `routers/`, `service.py`, `security.py`, `models.py`, `schemas.py`).
  - `migrations/` Alembic env and versions.
  - `tests/` smoke tests.
- `services/people-service/`
  - `app/routers/people/` domain routers.
  - `app/services/` domain service layer.
  - `migrations/` and `tests/`.
- `services/telegram-integration-service/`
  - `app/main.py`, `bot.py`, `service.py`, `storage.py`.
  - `tests/` smoke tests.

## Frontend Layout
- `web/src/app/` route tree and layouts.
- `web/src/components/` shared UI/layout/provider components.
- `web/src/modules/` feature modules (`auth`, `dashboard`, `people`).
- `web/src/lib/` shared API and utility code.
- `web/public/` static assets.

## Data and Migration Layout
- Per-service Alembic setup:
  - `services/auth-service/alembic.ini`
  - `services/people-service/alembic.ini`
- Migration versions under each service `migrations/versions/`.

## Naming and Organization Patterns
- Backend:
  - `routers/` for HTTP boundary.
  - `schemas.py` for DTOs.
  - `service.py` or `services/*` for business logic.
  - `models.py` for persistence entities.
- Frontend:
  - Feature-first organization under `src/modules`.
  - Shared abstractions under `src/lib` and `src/components`.

## Test Location Patterns
- Backend tests are colocated per service under `services/*/tests/`.
- No dedicated frontend test directory currently detected in `web/`.
