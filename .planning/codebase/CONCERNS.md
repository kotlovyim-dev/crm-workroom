# Concerns

## Security Concerns
- Default JWT fallback value exists in compose (`JWT_SECRET_KEY: ${JWT_SECRET_KEY:-change-me}` in `docker-compose.yml`).
- Compose sets `COOKIE_SECURE: "false"` for auth service in `docker-compose.yml`, which is unsafe for HTTPS production deployment.
- Hardcoded Postgres password in compose (`POSTGRES_PASSWORD: postgres` in `docker-compose.yml` and `docker-compose.dev.yml`).
- Broad exception handling around token decode in `services/auth-service/app/routers/auth.py` may hide root causes and reduce observability.

## Reliability Concerns
- Migrations run inline on startup (`alembic upgrade head && uvicorn ...`) for auth and people services in compose files; failed migrations can block service boot.
- Gateway routes include upstream services not present in repo (`projects-service`, `info-portal-service`, `messenger-service`) in `services/api-gateway/nginx.conf`; requests may fail unless external services are provided.
- Single gateway and service container assumptions in compose without explicit redundancy.

## Testing and Quality Concerns
- Backend tests are mostly smoke/contract shape; deeper integration and failure-mode coverage appears limited.
- No visible frontend automated tests in `web/`.
- No explicit repository-level CI pipeline config detected from visible files in current scan.

## Architecture and Evolution Concerns
- Auth and people services are present, but gateway config suggests broader platform scope; architectural drift risk if stubs remain long-term.
- Header-based identity propagation is effective but tightly couples downstream services to gateway conventions (`X-User-Id`, `X-Workspace-Id`).
- API versioning is fixed at `/api/v1`, with no visible deprecation/version transition strategy.

## Operational Concerns
- Environment-specific behavior is spread across two compose files and service `.env` files; configuration drift risk across environments.
- Telegram service can run polling mode in dev and webhook mode in runtime code (`services/telegram-integration-service/app/main.py`), which may create environment-specific behavior differences.

## Suggested Mitigations
- Enforce secret provisioning and fail-fast defaults for JWT and DB credentials.
- Split migrations into controlled deploy step for production rollouts.
- Add integration tests for gateway auth flow and cross-service contracts.
- Add frontend test baseline and a minimal CI check suite.
- Document service ownership for planned but currently missing upstream services.
