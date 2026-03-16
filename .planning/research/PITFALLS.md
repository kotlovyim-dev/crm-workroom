# DevFlow CRM Pitfalls (Project-First, Freemium, Role-Based)

## Purpose

This document lists high-probability pitfalls for DevFlow CRM given the current repo state and strategy in `.planning/PROJECT.md`:

- project-first v1 for IT teams (30-200)
- freemium growth model with expansion path
- role-focused workflows (Admin/Owner, PM/Team Lead, Employee, HR)
- modular monolith delivery in 2-3 months

Each pitfall includes warning signs, prevention actions, and the phases that should absorb the risk.

## Phase Map Used In This Research

- **Phase 0 - Foundation Hardening**: trust boundaries, migrations, baseline tests, observability
- **Phase 1 - Workspace + RBAC Core**: tenant model, role permissions, policy checks
- **Phase 2 - Project Execution Core**: projects, tasks, board/list/timeline coherence
- **Phase 3 - Time + Workload Intelligence**: time logging, capacity, utilization, reporting
- **Phase 4 - Freemium Entitlements + Monetization**: feature gates, limits, upgrades, anti-abuse
- **Phase 5 - Adoption + Collaboration UX**: onboarding, notifications, handoffs, in-app guidance
- **Phase 6 - Scale + Reliability**: performance, SLOs, supportability, analytics loops

## Pitfalls Register

| Risk | Why It Is Likely Here | Warning Signs | Prevention | Phases |
|---|---|---|---|---|
| 1) Building "full CRM" before validating project-first value | Repository scope and nav already advertise many future domains; v1 timeline is short | Roadmap items for messenger/info-portal re-enter sprint plans; project/task core is still partial after multiple iterations | Enforce a project-first scope gate: no new domain work unless it directly improves project execution KPI | Phase 0, Phase 2 |
| 2) Tenant isolation weaknesses create cross-workspace data exposure | Current architecture notes header-derived auth context; this is risky if trust boundary is bypassed | API requests succeed with forged workspace headers in non-gateway paths; incident reports mention wrong workspace data | Require verified auth context at backend edge, add tenant-scoped data guards in service layer and tests | Phase 0, Phase 1 |
| 3) RBAC drift causes permission chaos | Four-role model is defined, but permissions are not yet formalized as a policy matrix | Rapid growth of route-level if/else checks; inconsistent behavior between UI and API for same action | Define a single permission matrix and policy engine early; add deny-by-default checks | Phase 1 |
| 4) Freemium gates are bolted on late | Monetization is active requirement but product core is still being implemented | Hard-coded limits appear in random endpoints; upgrade flow exists but limit checks are inconsistent | Introduce centralized entitlements service/table and middleware-style checks from first gated feature | Phase 4 (design starts in Phase 1) |
| 5) Free tier limits block activation before value is felt | Freemium can fail if limits trigger before first team success moment | High signup but low week-1 project/task completion; support asks for limit overrides immediately | Set limits around scale, not core trial value (allow one complete project flow before cap friction) | Phase 4, Phase 5 |
| 6) "Role-based workflows" become role-specific silos | Different personas need shared project context, not isolated modules | PM updates do not propagate to Employee/HR views; users duplicate status updates in external tools | Build shared project objects with role-shaped views, not separate role-owned data models | Phase 1, Phase 2, Phase 3 |
| 7) Task execution and time tracking diverge | Time/workload is a core promise but commonly shipped as detached module | Time logs cannot be tied to task state transitions; utilization reports conflict with board progress | Bind time entries to project/task entities and transition events; enforce referential rules | Phase 2, Phase 3 |
| 8) Workload metrics are vanity, not planning-grade | Early dashboards can over-index on activity counters | Utilization shown without capacity baseline; teams distrust staffing recommendations | Define workload semantics up front (capacity, allocation, actuals, variance) and expose assumptions in UI | Phase 3 |
| 9) Missing migration discipline causes fragile releases | Codebase concerns already flag incomplete DB migration lifecycle | Fresh environment setup breaks; schema differences across machines; manual DB patching appears | Add Alembic baseline and migration CI checks before expanding domain schema | Phase 0 |
| 10) Thin test coverage accelerates regressions | Current state notes empty backend tests and no frontend test runner | Frequent hotfixes in auth/session, broken guards, endpoint contract regressions | Add minimum test pyramid: auth/session integration, RBAC policy tests, core task/time flows | Phase 0, Phase 1, Phase 2 |
| 11) Dead-end navigation undermines trust early | Sidebar already includes routes not fully implemented | 404s or placeholder pages on first session; users assume product is unstable | Hide or badge not-ready modules with feature flags and clear "coming soon" states | Phase 0, Phase 5 |
| 12) Notification strategy creates noise instead of coordination | Multi-role project workflows require selective, actionable alerts | Users mute all notifications; missed approvals/blockers rise | Event taxonomy with priority tiers, role relevance filters, and digest defaults | Phase 5 |
| 13) Onboarding does not reach team-level activation | Signup exists, but team workflows (invite, assignment, collaboration) are still shallow | Many single-user workspaces; low invite acceptance; no second active user by day 3 | Design onboarding around first project setup, first task assignment, first teammate contribution | Phase 5, Phase 2 |
| 14) Pricing and authorization logic diverge | Freemium and RBAC intersect on who can perform paid operations | Non-admin users can trigger paid-only actions; billing changes do not affect permissions promptly | Connect entitlement checks and role checks in one decision path with auditable outcomes | Phase 1, Phase 4 |
| 15) Performance cliffs appear at target team sizes (30-200) | v1 target includes higher collaboration density and list-heavy views | Slow board/timeline loads, N+1 query symptoms, timeouts on calendar/workload ranges | Add query budgets, pagination contracts, index strategy, and per-feature performance tests | Phase 3, Phase 6 |
| 16) No product operating metrics for freemium conversion learning | Without instrumentation, pricing and onboarding become guesswork | Debates rely on anecdotes; inability to explain conversion drop-offs | Instrument activation funnel, limit-hit events, upgrade intent, and role-specific retention | Phase 4, Phase 6 |
| 17) Security defaults leak from dev to production | Existing concerns mention weak default secrets and cookie settings | Same secret reused across envs; insecure cookie flags in staging/prod | Fail fast on unsafe production config and add startup config validation checks | Phase 0 |
| 18) "Everything urgent" destroys roadmap sequencing | Project breadth + short timeline tends to create reactive reprioritization | Frequent mid-sprint context switching; partial features across many modules | Enforce WIP limits and phase exit criteria tied to user outcomes, not ticket count | Phase 0, Phase 6 |

## Immediate Priority Risks (Top 6)

Focus first on risks that can invalidate the whole strategy if delayed:

1. Tenant isolation weaknesses (Risk 2)
2. Migration discipline gaps (Risk 9)
3. Test coverage deficits (Risk 10)
4. RBAC drift (Risk 3)
5. Freemium gates bolted on late (Risk 4)
6. Task/time model divergence (Risk 7)

## Phase-Level Risk Checklist

- **Phase 0 exit**: trusted auth context boundary, migration pipeline, baseline tests, safe production config checks
- **Phase 1 exit**: permission matrix implemented and enforced in API + UI, audit-ready authorization decisions
- **Phase 2 exit**: project/task flows usable end-to-end without dead routes or role inconsistencies
- **Phase 3 exit**: time/workload data model trustworthy for planning, not just reporting
- **Phase 4 exit**: entitlements are centralized, observable, and aligned with upgrade UX
- **Phase 5 exit**: team onboarding and notification model improve collaboration without alert fatigue
- **Phase 6 exit**: performance and reliability validated for 30-200 person teams with measurable conversion/retention insights