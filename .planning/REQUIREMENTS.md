# Requirements: DevFlow CRM

**Defined:** 2026-03-17
**Core Value:** Delivery teams get one real-time operational picture of project execution, team workload, and time tracking to reduce coordination friction and ship faster.

## v1 Requirements

### Authentication

- [ ] **AUTH-01**: User can sign up and log in with email/password in a workspace context.
- [ ] **AUTH-02**: User can keep authenticated session via refresh flow across browser refresh.
- [ ] **AUTH-03**: Workspace Admin/Owner can invite users into workspace.
- [ ] **AUTH-04**: Role-based policies are enforced for Admin/Owner, PM/Team Lead, Employee, and HR.

### Projects and Tasks

- [ ] **PROJ-01**: User can create, view, update, and archive projects.
- [ ] **PROJ-02**: User can view project details including status and progress snapshot.
- [ ] **TASK-01**: User can create, update, assign, reprioritize, and change status of tasks.
- [ ] **TASK-02**: User can manage tasks in a Kanban board with drag-and-drop status changes.
- [ ] **PROJ-03**: User can view basic project timeline.
- [ ] **PROJ-04**: PM/Team Lead can view project health indicators (progress, risks, in-review/bottlenecks).
- [ ] **PROJ-05**: User can start projects from predefined templates.

### Time and Workload

- [ ] **TIME-01**: User can log time against tasks/projects.
- [ ] **WORK-01**: PM/Team Lead can see basic team workload view based on assignments and time logs.
- [ ] **WORK-02**: PM/Team Lead can view employee activity summary related to project execution.

### Calendar and Vacations

- [ ] **VAC-01**: User can create and track vacation requests.
- [ ] **CAL-01**: User can view merged team calendar with project events and vacations.
- [ ] **CAL-02**: PM/Team Lead can view availability planning signal for sprint/team planning.

### Freemium and Plans

- [ ] **PLAN-01**: System enforces free-tier limits for members, projects, and tasks.
- [ ] **PLAN-02**: System shows clear upgrade prompts when workspace approaches or exceeds limits.
- [ ] **PLAN-03**: Messenger/chat capabilities are paid-only in initial v1.

### Design Conformance

- [ ] **UX-01**: Implemented UI/UX flows must conform to `design/crm.pen` screens and interaction intent.

## v2 Requirements

### Collaboration and Expansion

- **MSG-01**: Full-featured messenger (channels, mentions, advanced search, files, editing/thread depth).
- **PORT-01**: Advanced info portal workflows (richer ACL/sharing/versioning).
- **INT-01**: Broad external integrations marketplace.
- **MOB-01**: Mobile native applications.

### Billing Depth

- **BILL-01**: Advanced billing automation (multi-currency, tax logic, deeper invoicing flows).

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full Slack/Teams replacement in v1 | Distracts from project-first delivery value and timeline constraints |
| Mobile native apps in v1 | Web-first strategy for 2-3 month execution window |
| Broad third-party integrations in v1 | High integration overhead before core value is validated |
| Advanced billing/tax stack in v1 | Not required to validate freemium adoption and conversion |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase TBD | Pending |
| AUTH-02 | Phase TBD | Pending |
| AUTH-03 | Phase TBD | Pending |
| AUTH-04 | Phase TBD | Pending |
| PROJ-01 | Phase TBD | Pending |
| PROJ-02 | Phase TBD | Pending |
| TASK-01 | Phase TBD | Pending |
| TASK-02 | Phase TBD | Pending |
| PROJ-03 | Phase TBD | Pending |
| PROJ-04 | Phase TBD | Pending |
| PROJ-05 | Phase TBD | Pending |
| TIME-01 | Phase TBD | Pending |
| WORK-01 | Phase TBD | Pending |
| WORK-02 | Phase TBD | Pending |
| VAC-01 | Phase TBD | Pending |
| CAL-01 | Phase TBD | Pending |
| CAL-02 | Phase TBD | Pending |
| PLAN-01 | Phase TBD | Pending |
| PLAN-02 | Phase TBD | Pending |
| PLAN-03 | Phase TBD | Pending |
| UX-01 | Phase TBD | Pending |

**Coverage:**
- v1 requirements: 21 total
- Mapped to phases: 0
- Unmapped: 21 ⚠️

---
*Requirements defined: 2026-03-17*
*Last updated: 2026-03-17 after initial definition*
