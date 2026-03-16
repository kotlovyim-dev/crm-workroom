# Integrations

## Integration Topology
The system exposes backend APIs through Nginx and composes multiple internal services over HTTP and shared infrastructure services.

## Internal Service Integrations
- API Gateway to Auth Service:
  - Route `/api/v1/auth/` proxies to `auth-service:8080` (`services/api-gateway/nginx.conf`).
- API Gateway to People Service:
  - Route `/api/v1/people/` proxies to `people-service:8082` (`services/api-gateway/nginx.conf`).
- Gateway auth validation hook:
  - Internal location `/_validate_jwt` calls `auth-service:8080/api/v1/auth/validate-token` (`services/api-gateway/nginx.conf`).
- Auth Service to Telegram Integration Service:
  - `TELEGRAM_SERVICE_URL=http://telegram-integration-service:8081` in `docker-compose.yml`.

## Infrastructure Integrations
- People Service to PostgreSQL:
  - `DATABASE_URL=postgresql+asyncpg://...@people-postgres:5432/crm_people` in `docker-compose.yml` and `docker-compose.dev.yml`.
- Telegram Integration Service to Redis:
  - `REDIS_URL=redis://telegram-integration-redis:6379/...` in compose files.

## External Platform Integrations
- Telegram Bot API integration via `aiogram` and bot runtime lifecycle in `services/telegram-integration-service/app/main.py`.
- Webhook endpoint for Telegram updates at `/webhooks/telegram/{secret}` in `services/telegram-integration-service/app/main.py`.

## Auth and Session Integration Contract
- Browser authenticates against Auth Service endpoints under `/api/v1/auth/*` (`services/auth-service/app/routers/auth.py`).
- Auth endpoints set `access_token` and `refresh_token` cookies (`services/auth-service/app/routers/auth.py`).
- Gateway injects `X-User-Id` and `X-Workspace-Id` headers after validation (`services/api-gateway/nginx.conf`).
- People Service depends on auth headers through dependency layer (`services/people-service/app/routers/people/employees.py`).

## Frontend Integration Patterns
- Frontend Axios client uses `withCredentials: true` for cookie-based auth in `web/src/lib/api/client.ts`.
- Frontend auto-refresh behavior calls `/api/v1/auth/refresh` on 401 errors in `web/src/lib/api/client.ts`.
- Base API URL comes from `NEXT_PUBLIC_API_BASE_URL` (`web/src/lib/api/client.ts`, compose files).

## Health and Operational Integrations
- Gateway exposes per-service health proxy routes (`/health/auth`, `/health/people`, `/health/telegram`) in `services/api-gateway/nginx.conf`.
- Compose healthchecks validate readiness for startup dependencies in `docker-compose.yml`.

## Planned or Stubbed Integrations
- Gateway includes routes for `projects-service`, `info-portal-service`, and `messenger-service` in `services/api-gateway/nginx.conf`, indicating planned services not present in this repo.
