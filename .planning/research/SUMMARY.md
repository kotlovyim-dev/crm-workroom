# DevFlow CRM Research Summary

## Key stack recommendation
- Keep and harden the current modular monolith: FastAPI + SQLAlchemy async + Alembic, Next.js App Router + React + TypeScript, PostgreSQL, Redis.
- Prioritize reliability upgrades over replatforming: capability-based RBAC, tenant boundary enforcement, outbox-style internal events, and production observability (structured logs, traces, error tracking).
- Add Redis-backed background jobs for notifications, usage aggregation, and projection updates before considering Kafka/microservices.
- Treat `design/crm.pen` as mandatory product contract for IA, screen priorities, and role workflows; implementation should follow design intent, not redesign it.

## Table stakes for v1
- Project-first core loop for medium IT teams: projects, tasks, board view, assignment, due dates, status transitions, and basic project health.
- Time tracking linked to task/project entities (not standalone) to support delivery transparency.
- Team context essentials: employee directory, vacation requests, unified calendar with project + availability signals.
- Stable auth/session + role enforcement (Owner/Admin, PM/Lead, Employee, HR) across API and UI.
- Freemium baseline: clear free-tier caps (members/projects/tasks), visible usage meters, upgrade prompts at limit boundaries.
- Navigation and modules must match implemented scope in `design/crm.pen` to avoid dead-end routes and trust loss.

## Top pitfalls
- Scope creep into full CRM/messenger/integrations before validating project execution value.
- Tenant isolation gaps from inconsistent workspace context validation.
- RBAC drift via ad hoc role checks instead of centralized capability rules.
- Late, scattered freemium gates that break monetization and create inconsistent UX.
- Weak migration/testing discipline causing fragile releases and regressions.
- Task and time-tracking models drifting apart, producing untrustworthy workload analytics.

## Suggested phase implications
- Phase 0 (hardening): production-safe config checks, migration CI, baseline integration tests, auth context trust boundary.
- Phase 1 (access + entitlements): capability matrix, centralized permission checks, early plan/limit service foundation.
- Phase 2 (project execution): `projects` + `tasks` modules and UI flows mapped directly to `design/crm.pen` priority screens.
- Phase 3 (time + workload): `time_tracking` plus projection-backed `workload/reporting` read models.
- Phase 4 (freemium monetization): durable entitlement ledger + Redis counters + consistent API/UI upgrade semantics.
- Phase 5+ (expansion): collaboration depth (messenger/info portal) only after project-time-workload loop and activation metrics are stable.

## Go/no-go checks
- Go if: one workspace can complete end-to-end project setup -> task execution -> time logging -> calendar visibility without role conflicts.
- Go if: tenant isolation and RBAC tests pass for all write endpoints and critical reads.
- Go if: free-tier limits are consistently enforced server-side with clear upgrade UX and auditability.
- Go if: implemented routes/screens materially match `design/crm.pen` and no key nav item leads to non-functional pages.
- No-go if: migrations are not reproducible in clean environments or auth/session regressions remain unresolved.
- No-go if: roadmap includes major non-project-first domains before v1 activation and conversion signals are instrumented.
