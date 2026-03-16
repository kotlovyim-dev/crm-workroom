# ARCHITECTURE Research - DevFlow CRM

Date: 2026-03-17
Focus: Modular monolith evolution for project-first v1 delivery

## 1) Architectural Direction

DevFlow CRM should continue as a modular monolith with strict in-process module boundaries and explicit contracts between modules. The current structure is already close to the target shape; the next step is to harden boundaries, add missing project execution modules, and standardize read models for cross-team visibility.

Target qualities:
- Fast feature throughput for a small team (single deployable backend + single frontend app)
- Clear domain ownership per module (no shared business logic bleed)
- Extraction-ready seams for future service split only when justified by scale
- Predictable API contracts for frontend modules and phase-by-phase delivery

Non-goal for v1:
- No distributed microservices or event bus infrastructure unless a concrete bottleneck appears

## 2) Recommended Component Boundaries

## 2.1 Backend bounded modules (inside `backend/app/features/`)

Existing modules should remain and be clarified:
- `auth`: identity, session lifecycle, workspace scoping, role claims
- `telegram`: verification intents, bot runtime, Telegram linkage lifecycle
- `employees`: employee directory and team membership views
- `profile`: personal settings and user-level preferences
- `vacations`: balances, requests, approval states, timeline sources
- `calendar`: event CRUD and time-window queries

New project-first modules for v1:
- `projects`: project metadata, status, ownership, membership, milestones
- `tasks`: task lifecycle, assignment, priority, state transitions, board columns
- `time_tracking`: worklog entries, timers (optional), task/project attribution
- `workload`: computed availability and capacity snapshots (read-model module)
- `reporting`: delivery and throughput snapshots (read-model module for dashboard)
- `plans` (or `billing_limits`): freemium limits checks and plan entitlements

Shared kernel guidance:
- Keep `features/shared/` strictly technical and cross-cutting.
- Move any domain-specific model out of shared into an owning module.
- Allowed shared concerns: request context extraction, common error envelopes, pagination primitives, base audit fields, shared enum utilities.

## 2.2 Frontend module boundaries (`web/src/modules/`)

Current module structure should mirror backend ownership one-to-one where possible.

Recommended frontend modules:
- `auth`
- `dashboard`
- `projects`
- `tasks`
- `time`
- `workload`
- `people` (maps to employees/profile where needed)
- `vacations`
- `calendar`
- `billing`

Rules:
- Route segments in `web/src/app/(dashboard)/...` should map to module entrypoints.
- API hooks must stay inside owning module (`modules/<domain>/api/*`).
- Reusable visual primitives remain in `components/ui`, but business components stay in modules.

## 2.3 Data ownership boundaries

Write ownership per aggregate:
- `auth` owns User/Workspace/RefreshSession and role claims
- `projects` owns Project/Milestone/ProjectMember
- `tasks` owns Task/BoardColumn/TaskComment/TaskTransition log
- `time_tracking` owns Worklog/TimerSession
- `vacations` owns VacationBalance/VacationRequest
- `calendar` owns CalendarEvent (or projection of other module events)

Read model ownership:
- `workload` and `reporting` are projection modules; they do not own core business writes from other modules.

Boundary policy:
- Cross-module writes should happen through service-level APIs, not direct table mutation from another module.
- Cross-module reads can be:
  - direct query for simple lookups (v1 pragmatism), or
  - projection/read model for dashboard-heavy queries.

## 3) Data Flow Model

## 3.1 Request flow (command path)

1. Next.js UI route triggers module action (TanStack Query mutation).
2. Module API client calls backend REST endpoint.
3. Backend router validates request and workspace/user context.
4. Owning service executes domain logic and transaction.
5. Service writes aggregate tables and emits internal domain event record (DB-backed outbox table recommended).
6. Response returns canonical DTO; frontend invalidates/query-refreshes relevant caches.

Recommendation:
- Introduce a lightweight in-DB outbox pattern before adding async brokers. This keeps monolith simplicity while enabling reliable projections.

## 3.2 Query flow (read path)

Two query classes:
- Operational queries: module-local reads (tasks list, project detail, profile)
- Analytical queries: cross-module reads (team workload, delivery velocity, project health)

For analytical queries:
- Build projection tables/materialized views updated from domain events/outbox processor.
- Serve dashboard endpoints from `workload`/`reporting` modules to avoid expensive join-heavy ad hoc queries in request time.

## 3.3 Identity and tenancy flow

- Auth remains source of truth for user/workspace identity.
- Every domain command/query enforces workspace boundary at repository/service layer.
- Role checks should be centralized as capability checks (e.g., `can_manage_project`, `can_approve_vacation`) instead of ad hoc role string checks.

## 3.4 Time and calendar unification flow

- `tasks` and `vacations` publish domain events that can project into `calendar` views.
- `calendar` remains user-facing schedule API; it may expose merged views from owned events + projections.
- `time_tracking` links entries to task/project IDs to enable downstream workload/reporting metrics.

## 4) Build Order (Implementation Sequence)

The sequence below minimizes rework and aligns with project-first v1 goals.

Phase A - Foundation hardening
- Standardize module template (`routes.py`, `service.py`, `schemas.py`, `repository.py` where needed)
- Add capability-based authorization helper layer
- Introduce outbox table + internal event publisher abstraction
- Add consistent pagination/filter contract across list endpoints

Phase B - Core project execution domain
- Implement `projects` module (CRUD + membership + project status)
- Implement `tasks` module (board-aware task lifecycle)
- Frontend routes/pages for projects and tasks with shared dashboard navigation

Phase C - Time and workload
- Implement `time_tracking` writes and task attribution
- Implement `workload` projections and APIs for per-user and per-project capacity
- Add dashboard cards/charts for workload and in-flight execution risk

Phase D - Reporting and visibility
- Implement `reporting` projections (velocity, completion trends, overdue rates)
- Add project health views and cross-team delivery snapshots
- Add export-friendly endpoints if needed for PM/lead workflows

Phase E - Freemium enforcement and plan boundaries
- Implement `plans`/`billing_limits` checks at command boundary
- Enforce free-tier limits (members/projects/tasks) with clear API error semantics
- Surface upgrade prompts and usage meters in frontend

Phase F - Collaboration and expansion (post-v1)
- Messenger/info-portal deeper features as paid expansion
- Integrations only after core project-time-workload loop is stable

## 5) Phase Implications for This Repo

## 5.1 Backend implications

- Add new feature directories under `backend/app/features/` for `projects`, `tasks`, `time_tracking`, `workload`, `reporting`, `plans`.
- Keep each module self-contained with migrations scoped by ownership.
- Reduce overgrowth in `features/shared/models.py`; migrate domain-owned tables into owning modules over time.
- Introduce an internal repository pattern only where query complexity warrants it; avoid boilerplate for simple modules.

## 5.2 Frontend implications

- Fill currently empty dashboard route segments (`calendar`, `employees`, `profile`, `vacations`) with module-driven pages.
- Add new segments for `/projects`, `/tasks`, `/time`, `/workload`, and reporting views.
- Keep API/auth concerns in dedicated module clients; avoid leaking Axios calls directly into route files.
- Use query-key domains per module to avoid cache invalidation collisions.

## 5.3 Dev and ops implications

- Keep single backend deployment and single DB for v1.
- Redis remains for Telegram and can optionally support lightweight background workers/caching.
- Add one internal background worker process only if projection lag becomes visible; still same repo and same DB.

## 5.4 Testing implications

Minimum per new module:
- Service-layer unit tests for domain rules and role/capability checks
- Router integration tests for workspace isolation and error contracts
- Cross-module contract tests for projection correctness (tasks/time -> workload/reporting)

Quality gates:
- No module may write another module's tables directly.
- All list endpoints must implement deterministic pagination and filter schema.
- Role/capability checks must be explicit and test-covered.

## 6) Recommended Near-Term Refactors

1. Extract domain tables from `features/shared/models.py` into owning modules where feasible.
2. Introduce a common `domain_events` (outbox) table and processing loop.
3. Add `projects` and `tasks` first, then adapt dashboard to consume those APIs.
4. Normalize API prefixing and endpoint naming by module (`/api/v1/projects/*`, `/api/v1/tasks/*`, etc.).
5. Introduce `capabilities` utility in auth/shared to centralize role policy.

## 7) Risks and Mitigations

Risk: Shared module becomes a de facto dumping ground.
Mitigation: Enforce ownership rules in code review and module README contracts.

Risk: Dashboard queries become slow with cross-module joins.
Mitigation: Build projection tables early (workload/reporting) and serve analytical reads from them.

Risk: Freemium checks get scattered.
Mitigation: Centralize limit enforcement in command services via `plans`/`billing_limits`.

Risk: Over-engineering toward microservices too early.
Mitigation: Keep monolith-first, extraction-ready interfaces, no broker-first architecture.

## 8) Target v1 Module Map (Recommended)

Backend modules (v1):
- auth
- telegram
- employees
- profile
- vacations
- calendar
- projects
- tasks
- time_tracking
- workload
- reporting
- plans

Frontend modules (v1):
- auth
- dashboard
- projects
- tasks
- time
- workload
- people
- vacations
- calendar
- billing

This map keeps the product aligned with project-first delivery while preserving the current modular monolith direction and implementation velocity.
