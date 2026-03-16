# STACK Research for DevFlow CRM (2025-2026)

## Scope and Product Fit

DevFlow CRM is a project-first SaaS for medium IT companies (30-200 people), with freemium onboarding and a fast path to team adoption. The stack should optimize for:
- Fast iteration by a small team
- Low operational overhead during v1 and early growth
- Strong tenant isolation and auditability for B2B buyers
- Predictable scaling from first paid customers to mid-market usage

Current repo baseline:
- Backend: FastAPI modular monolith, Python 3.12, SQLAlchemy async, Alembic
- Frontend: Next.js 16 + React 19 + TypeScript + Tailwind v4 + TanStack Query
- Data: PostgreSQL
- Cache/ephemeral state: Redis
- Runtime: local-first, Redis in Docker

## Executive Recommendation

Keep the current monolith-first architecture and modernize around reliability, observability, and controlled scale features rather than replatforming.

Recommended strategic position for 2025-2026:
- Keep FastAPI + Next.js + Postgres + Redis as core
- Add background job processing on Redis (not Kafka yet)
- Add production-grade observability (OpenTelemetry + error tracking)
- Harden tenancy, limits, and billing boundaries in the existing monolith
- Delay microservices and event-platform complexity until clear scale triggers

Overall confidence: High (0.87)

## Stack Choices by Layer

## 1) Frontend (Web App)

Decision: Keep Next.js App Router + React 19 + TypeScript + TanStack Query.

Why this fits this repo:
- Already implemented and working in `web/`
- Good balance of DX and performance for dashboard-heavy SaaS
- Server components plus client-side React Query is a practical hybrid for auth and data-heavy screens

Recommended adjustments:
- Keep `next@16` and `react@19`, but pin minor versions in production branches to reduce upgrade regressions.
- Keep `zod` + `react-hook-form` as form standard.
- Keep `zustand` only for UI/session-local state, not server state.
- Add a typed API contract generation path (OpenAPI -> TS client generation) to reduce drift between FastAPI and frontend modules.

Avoid for now:
- Full frontend rewrite to another framework (no ROI).
- Overusing server actions for all data mutations when current API patterns already center on backend routes.

Confidence: High (0.84)

## 2) Backend API and Domain Runtime

Decision: Keep FastAPI modular monolith as the primary backend architecture through v1-v2 growth.

Why this fits this repo:
- Existing bounded modules (`auth`, `telegram`, `employees`, `profile`, `vacations`, `calendar`)
- Product velocity is more important than distributed-system decomposition
- Current team size and timeline (2-3 months for project-first v1) favors low ops complexity

Recommended adjustments:
- Keep SQLAlchemy 2 async + Alembic as canonical data layer.
- Introduce explicit service-layer interfaces per feature for easier later extraction.
- Standardize idempotency for write endpoints likely to be retried by UI.
- Add strict request/response versioning discipline under `/api/v1` before adding `/api/v2`.

Avoid for now:
- Early split into many services (auth/projects/people/time as separate deployables).
- Premature GraphQL gateway for all domain APIs.

Confidence: High (0.90)

## 3) Data Platform (Primary Store)

Decision: Keep PostgreSQL as source of truth; scale vertically first, then selectively optimize.

Why this fits this repo:
- Relational model strongly matches CRM entities and workspace scoping
- Supports transactional integrity for onboarding, membership, limits, and audit trails

Recommended adjustments:
- Enforce workspace-tenant boundaries at schema and query layers (`workspace_id` everywhere it matters).
- Add partial indexes for high-frequency dashboards (tasks by project/status/assignee/date).
- Use Postgres features before adding new infra:
  - `pg_trgm` for search-like UX in employees/projects/tasks
  - Materialized views (or cached summary tables) for dashboard aggregates
- Add PITR-capable managed Postgres in production environments.

Avoid for now:
- Introducing a second primary DB for analytics in early stage.
- Replacing SQLAlchemy with a new ORM just for trend reasons.

Confidence: High (0.88)

## 4) Cache, Queue, and Async Work

Decision: Keep Redis, expand usage to caching + job queue + rate/limit support.

Why this fits this repo:
- Redis already used for Telegram verification sessions
- Freemium model benefits from fast counters and quota checks

Recommended adjustments:
- Add Redis-backed background jobs (prefer `arq` in Python ecosystem for this stack).
- Move non-request-critical tasks to jobs:
  - Notification fanout
  - Digest generation
  - Usage aggregation for freemium limits
- Define clear TTL policy and key naming conventions by domain.

Avoid for now:
- Kafka/RabbitMQ unless there is sustained queue pressure, multi-consumer event needs, or strict replay requirements.

Confidence: Medium-High (0.79)

## 5) Auth, Sessions, and Tenant Security

Decision: Keep cookie-based sessions and current auth flow, harden for B2B compliance expectations.

Why this fits this repo:
- Existing login/refresh/logout/session implementation is already the strongest vertical slice
- Cookie sessions are good for web SaaS UX and security posture

Recommended adjustments:
- Rotate refresh tokens with reuse-detection and session family invalidation.
- Persist audit events for auth-sensitive actions.
- Add per-workspace policy toggles (session timeout, password policy, invite rules).
- Ensure all domain endpoints consistently resolve `X-Workspace-Id` and `X-User-Id` from trusted auth context.

Avoid for now:
- Replacing current auth flow with external identity complexity unless enterprise demand appears.

Confidence: Medium-High (0.77)

## 6) Observability and Runtime Ops

Decision: Add observability now; it is a scaling multiplier for small teams.

Recommended baseline for 2025-2026:
- OpenTelemetry traces across Next.js -> FastAPI -> Postgres/Redis
- Structured logs with request IDs and workspace IDs
- Error tracking (Sentry or equivalent)
- Basic RED metrics (rate, errors, duration) per endpoint and key jobs

Avoid for now:
- Full platform-engineering stack (service mesh, complex APM topology) before proven need.

Confidence: High (0.86)

## 7) Billing, Freemium Limits, and Plan Enforcement

Decision: Enforce limits in backend domain logic with Redis-accelerated counters and Postgres source-of-truth records.

Recommended shape:
- Postgres tables for plan entitlements and usage ledgers
- Redis for near-real-time soft-limit checks
- Periodic reconciliation job back into Postgres
- Workspace-level hard caps for free tier (members/projects/tasks)

Avoid for now:
- Embedding limit logic only in frontend
- Relying only on cached counters without durable reconciliation

Confidence: Medium-High (0.80)

## What to Keep From Current Stack

Keep as-is (or with small hardening):
- FastAPI modular monolith architecture in `backend/app/features/*`
- SQLAlchemy async + Alembic migrations
- Next.js App Router module layout in `web/src/app` and `web/src/modules`
- TanStack Query + RHF + Zod form/data patterns
- PostgreSQL as main store
- Redis as ephemeral and async support store

Confidence: High (0.91)

## What to Avoid (2025-2026 for This Repo)

Avoid now:
- Microservices split before project/task/time-tracking domain is stable
- Event bus platform (Kafka-class) without clear throughput/replay needs
- Replatforming frontend to chase trends
- New ORM migration that resets backend velocity
- Multi-region complexity before product-market fit and enterprise demand

Confidence: High (0.89)

## Migration Strategy and Risk Analysis

Principle: Evolve in place; do not replatform.

Phase A: Foundation hardening (low risk)
- Add observability and request correlation
- Add tenancy consistency checks and auth context propagation tests
- Introduce typed API client generation for frontend

Risk: Low
- Main risk is implementation overhead and temporary slowdown
- Mitigation: ship incrementally per domain and add smoke tests

Phase B: Product-first expansion (medium risk)
- Implement projects/tasks/time-tracking in existing monolith modules
- Add Redis job queue for side effects and async processing
- Add freemium limit enforcement and usage ledger

Risk: Medium
- Main risk is domain coupling and query performance regressions
- Mitigation: explicit module contracts, targeted DB indexes, endpoint SLO monitoring

Phase C: Scale gates and extraction readiness (medium, conditional)
- Define extraction triggers (e.g., sustained p95 latency, team ownership boundaries, independent deploy need)
- Extract only one high-pressure domain if trigger is met, not all at once

Risk: Medium
- Main risk is introducing distributed failure modes too early
- Mitigation: use a strangler approach with contract tests and shared auth/tenant middleware

Overall migration risk if this strategy is followed: Medium-Low (0.36 estimated risk score)
Confidence in strategy: High (0.85)

## Trigger-Based Reassessment Criteria

Reassess architecture only if at least two are true for 4+ weeks:
- API p95 latency remains above SLO after indexing/caching fixes
- Background jobs saturate Redis queue with operational impact
- Team structure requires independent deploy cadence for specific domains
- Enterprise security/compliance requirements exceed monolith operational model

If triggers are not met, continue monolith-first roadmap.

Confidence: Medium-High (0.78)

## Final Recommendation

For DevFlow CRM, the best 2025-2026 stack decision is to keep and harden the current FastAPI + Next.js monolith architecture with Postgres and Redis, add observability and async job capabilities, and postpone distributed-system complexity until objective scale triggers appear.

This maximizes delivery speed for the project-first v1, aligns with freemium economics, and preserves a clean path for selective extraction later.
