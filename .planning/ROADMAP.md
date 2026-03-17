# Roadmap: DevFlow CRM v1

**Defined:** 2026-03-17  
**Strategy:** Project-first v1 for medium IT teams (30-200 people), with freemium monetization and mandatory UX/flow conformance to `design/crm.pen`.  
**Target window:** 2-3 months

## Phase Plan

### Phase 1: Access, Roles, and Workspace Trust Boundary (Week 1-2)
**Goal:** Stabilize workspace onboarding/auth/session and role policy enforcement as the foundation for all project workflows.

**Mapped REQ IDs:** AUTH-01, AUTH-02, AUTH-03, AUTH-04
**Plans:** 3 plans

Plans:
- [ ] 01-01-PLAN.md - Stabilize auth/session core and canonical role contract with integration tests.
- [ ] 01-02-PLAN.md - Implement full invitation lifecycle with role assignment and transfer semantics.
- [ ] 01-03-PLAN.md - Deliver trust-boundary frontend UX (role-hidden nav, forbidden and invite/session edge states).

**Observable success criteria:**
- Signup/login and refresh-session flows pass end-to-end tests for valid and invalid credential paths.
- Workspace invitation flow allows Admin/Owner to invite and activate users in the same workspace.
- Capability checks consistently enforce v1 roles (Admin/Owner, PM/Team Lead, Employee, HR) on protected API/UI actions.
- Cross-workspace access attempts are rejected in integration tests for critical read/write endpoints.

### Phase 2: Project Core Lifecycle (Week 2-3)
**Goal:** Deliver project CRUD and project detail visibility so teams can model delivery work in one system.

**Mapped REQ IDs:** PROJ-01, PROJ-02

**Observable success criteria:**
- Users can create, view, update, and archive projects through API and dashboard UI.
- Project detail page shows status and progress snapshot fields defined by v1 data model.
- Archived projects are excluded from default active views and can be filtered/retrieved explicitly.

### Phase 3: Task Execution and Kanban Flow (Week 3-4)
**Goal:** Implement day-to-day task execution loop with assignment, prioritization, and board-based status movement.

**Mapped REQ IDs:** TASK-01, TASK-02

**Observable success criteria:**
- Users can create, assign, reprioritize, and status-change tasks within authorized projects.
- Kanban board supports drag-and-drop status transitions with persisted ordering/state.
- Task change history includes actor and timestamp for status and assignee changes.

### Phase 4: Timeline and Project Health Signals (Week 4-5)
**Goal:** Provide PM/Lead-level visibility into schedule and risk through timeline and health indicators.

**Mapped REQ IDs:** PROJ-03, PROJ-04

**Observable success criteria:**
- Project timeline view renders key milestones/deadlines from project/task data.
- PM/Team Lead role can access project health indicators (progress, risks, in-review/bottlenecks).
- Non-PM roles are restricted from PM-only health views where required by policy.

### Phase 5: Project Templates (Week 5-6)
**Goal:** Accelerate project kickoff using reusable project templates that seed initial structure.

**Mapped REQ IDs:** PROJ-05

**Observable success criteria:**
- Users can create projects from predefined templates in UI and API.
- Template-generated projects include expected default task/status structure.
- Template creation path reduces time-to-first-project compared to manual setup baseline.

### Phase 6: Time Tracking and Workload Visibility (Week 6-7)
**Goal:** Connect task execution to time logs and delivery analytics for team capacity decisions.

**Mapped REQ IDs:** TIME-01, WORK-01, WORK-02

**Observable success criteria:**
- Users can log time entries against tasks/projects with validation on ownership/workspace context.
- PM/Team Lead workload view shows assignment and logged-time signals by team member.
- Employee activity summary surfaces execution-relevant activity for PM/Lead review.

### Phase 7: Vacations and Unified Planning Calendar (Week 7-8)
**Goal:** Merge people availability and project events into planning-friendly calendar workflows.

**Mapped REQ IDs:** VAC-01, CAL-01, CAL-02

**Observable success criteria:**
- Vacation request lifecycle (submit, track status) works end-to-end.
- Unified calendar combines project events and vacation entries in one view.
- Sprint/team planning view exposes clear availability signals for PM/Team Lead.

### Phase 8: Freemium Entitlements and Upgrade Path (Week 8-9)
**Goal:** Enforce free-tier limits and paid-only capabilities to validate monetization and conversion.

**Mapped REQ IDs:** PLAN-01, PLAN-02, PLAN-03

**Observable success criteria:**
- Server-side limits are enforced for free-tier members/projects/tasks with audit-friendly decisions.
- Workspace usage meters and upgrade prompts appear before and at limit boundaries.
- Messenger/chat features are gated as paid-only in v1 access checks and UI affordances.

### Phase 9: Design Conformance and v1 Release Readiness (Week 9-10)
**Goal:** Ensure implemented IA, screens, and interactions conform to `design/crm.pen` before v1 release.

**Mapped REQ IDs:** UX-01

**Observable success criteria:**
- Implemented navigation/routes align with the corresponding `design/crm.pen` information architecture for v1 scope.
- Key user flows (auth, projects, tasks, time, calendar, freemium upgrade) pass design-conformance review against `design/crm.pen`.
- No critical v1 route leads to a non-functional or dead-end page in production candidate build.

## Delivery Notes

- Sequencing keeps project-first value loop first: projects -> tasks -> timeline/health -> time/workload.
- Freemium implementation is deliberate and early enough to validate paid expansion path before v1 release.
- Design conformance is mandatory throughout and finalized explicitly before go-live.
- Scope remains web-first and excludes v2 domains (full messenger depth, marketplace integrations, native mobile apps).
