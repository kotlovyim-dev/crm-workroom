# Testing

## Test Frameworks
- Python backend tests use `pytest` and `pytest-asyncio` from service dev dependencies:
  - `services/auth-service/pyproject.toml`
  - `services/people-service/pyproject.toml`
  - `services/telegram-integration-service/pyproject.toml`
- Global pytest config exists at `pytest.ini`.

## Current Test Placement
- `services/auth-service/tests/`:
  - `test_http_smoke.py`
- `services/people-service/tests/`:
  - `test_http_smoke.py`
  - `test_contract_people_api.py`
- `services/telegram-integration-service/tests/`:
  - `test_http_smoke.py`

## Observed Testing Patterns
- Smoke endpoint checks (health/readiness/basic auth failure) in `services/auth-service/tests/test_http_smoke.py`.
- Contract-shape tests with fake service injection in `services/people-service/tests/test_contract_people_api.py`.
- Dependency override approach using FastAPI app overrides for isolation (people contract tests).
- Minimal DB interaction in tests through fakes/mocks rather than full integration DB runs.

## Coverage Characteristics
- API surface health and basic route behavior are covered in smoke tests.
- Domain contract fields for people responses are covered for selected endpoints.
- Limited evidence of deep auth flow, migration, and end-to-end cross-service tests.
- No obvious frontend automated tests under `web/` currently.

## Gaps and Risks
- Missing frontend unit/integration/e2e coverage.
- No explicit CI quality gates for coverage thresholds found in repository root.
- Cross-service integration (gateway + auth + people) appears under-tested from repo-visible tests.
- Token refresh and cookie/session lifecycle are complex but not visibly covered by dedicated tests.

## Recommended Next Test Investments
- Add backend integration tests with ephemeral Postgres/Redis in compose test profile.
- Add focused auth tests for login/refresh/logout and cookie behavior.
- Add gateway contract tests to validate auth header propagation.
- Add frontend tests (component + API hook level) and one e2e happy path.
