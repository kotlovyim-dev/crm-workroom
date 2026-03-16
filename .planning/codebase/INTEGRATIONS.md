# INTEGRATIONS

## Integration Topology (Post-Migration)

- Core architecture is backend monolith + frontend client.
- Telegram verification logic is integrated into backend feature modules, not a separate deployable service.
- A retained internal HTTP boundary still exists inside the monolith:
  - auth feature client in `backend/app/features/auth/telegram_client.py`
  - telegram internal endpoints in `backend/app/features/telegram/routes.py`
  - default base URL points back to same backend: `TELEGRAM_SERVICE_URL=http://localhost:8000/api/v1/telegram` (`backend/.env.example`)

## Databases and State Stores

### PostgreSQL (Primary Persistence)

- Used by SQLAlchemy async engine in `backend/app/db/session.py`.
- Configured through `database_url` setting in `backend/app/config/settings.py`.
- Env key: `DATABASE_URL` (`backend/.env.example`).
- Typical entities (auth domain) live in `backend/app/features/auth/models.py`.

### Redis (Ephemeral Verification State)

- Redis client is initialized at startup in `backend/app/features/telegram/runtime.py`.
- Verification storage implementation in `backend/app/features/telegram/storage.py`.
- Key namespaces:
  - `tg_verify:intent:{short_token}`
  - `tg_verify:phone:{phone_number}`
  - `tg_verify:user:{telegram_user_id}`
- TTL is controlled by `verification_ttl_seconds` / `VERIFICATION_TTL_SECONDS`.
- Env key: `REDIS_URL`.
- Local runtime from `docker-compose.yml` service `redis`.

## Telegram Integration

### Telegram Bot API Boundary (External)

- aiogram bot created from `TELEGRAM_BOT_TOKEN` in `backend/app/features/telegram/runtime.py`.
- Runtime modes:
  - `webhook` (default)
  - `polling`
- Mode selection via `TELEGRAM_DELIVERY_MODE` (`backend/app/config/settings.py`, `backend/.env.example`).

### Telegram Webhook Boundary

- Endpoint: `/api/v1/telegram/webhooks/telegram/{secret}` in `backend/app/features/telegram/routes.py`.
- Secret validation against `TELEGRAM_WEBHOOK_SECRET`.
- If bot token is absent, bot runtime remains disabled (`backend/app/features/telegram/runtime.py`).

### Telegram Verification Flow (Internal)

- Auth creates intent via HTTP POST to `/internal/verifications/intents` (`backend/app/features/auth/telegram_client.py`).
- Auth checks code via HTTP POST to `/internal/verifications/check` (`backend/app/features/auth/telegram_client.py`).
- Telegram bot deep-link and contact confirmation handled by:
  - `backend/app/features/telegram/service.py`
  - `backend/app/features/telegram/bot.py`
- Verification code is generated and persisted in Redis-backed intent state.

## Frontend <-> Backend Integration Boundary

- Frontend API client in `web/src/lib/api/client.ts`.
- Base URL env: `NEXT_PUBLIC_API_BASE_URL` (`web/.env.example`).
- Cookies are sent cross-origin with `withCredentials: true`.
- Backend CORS allows configured frontend origin (`frontend_url`) in `backend/app/main.py`.

## Auth, Session, and Cookie Boundary

- Access JWT creation/validation in `backend/app/features/auth/security.py`.
- Refresh session rotation and revocation in `backend/app/features/auth/service.py`.
- Cookie issuance and deletion in `backend/app/features/auth/routes.py`.
- Cookie behavior depends on:
  - `COOKIE_SECURE`
  - `COOKIE_DOMAIN`
  - `ACCESS_TOKEN_TTL_SECONDS`
  - `REFRESH_TOKEN_TTL_SECONDS`

## Environment Variable Contract

Source of truth:
- settings fields: `backend/app/config/settings.py`
- sample values: `backend/.env.example`, `web/.env.example`

### Backend env vars

- `APP_ENV`
- `DATABASE_URL`
- `FRONTEND_URL`
- `TELEGRAM_SERVICE_URL`
- `JWT_SECRET_KEY`
- `ACCESS_TOKEN_TTL_SECONDS`
- `REFRESH_TOKEN_TTL_SECONDS`
- `COOKIE_SECURE`
- `COOKIE_DOMAIN`
- `REDIS_URL`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_BOT_USERNAME`
- `TELEGRAM_DELIVERY_MODE`
- `TELEGRAM_WEBHOOK_SECRET`
- `VERIFICATION_TTL_SECONDS`

### Frontend env vars

- `NEXT_PUBLIC_API_BASE_URL`

## External Service Boundaries Summary

- PostgreSQL: external persistent DB accessed by SQLAlchemy async engine.
- Redis: external in-memory store (containerized locally) for verification state.
- Telegram Bot API: external third-party messaging platform via aiogram bot client.
- Browser client: external caller to backend REST API (`/api/v1/*`) with cookie-based auth.

## Migration Notes (Observed in Current Codebase)

- Monolith backend is canonical runtime path (`backend/app/main.py`).
- Redis remains as separate infrastructure dependency (`docker-compose.yml`).
- Telegram integration service folder has been removed; equivalent behavior is represented by in-process feature modules under `backend/app/features/telegram/`.
- Internal auth-to-telegram HTTP calls remain as a soft boundary and can be collapsed to direct Python service calls in a future cleanup.
