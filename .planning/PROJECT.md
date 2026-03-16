# DevFlow CRM

## What This Is

DevFlow CRM is a SaaS platform for IT companies that unifies delivery operations, HR-adjacent team workflows, and internal coordination in one product. Instead of splitting work across Jira, Slack, HR systems, and spreadsheets, teams use one workspace to plan and execute projects with shared delivery context. The first release targets medium IT teams (30-200 people) with a project-first product strategy.

## Core Value

Delivery teams get one real-time operational picture of project execution, team workload, and time tracking to reduce coordination friction and ship faster.

## Requirements

### Validated

- ✓ Workspace onboarding and authentication flow exists (signup/login/refresh/logout/session) with cookie-based sessions and Telegram verification support — existing
- ✓ Backend modular monolith is running with domain APIs for employees, profiles, vacations, and calendar — existing
- ✓ Frontend has implemented onboarding and dashboard shell with nearest-events view and route structure for key domains — existing
- ✓ Local runtime path is established (backend + frontend locally, Redis in Docker only) — existing

### Active

- [ ] Deliver project-first v1 focused on cross-team visibility and faster delivery cycles
- [ ] Implement full project management slice (tasks, boards, timeline, and project progress visibility)
- [ ] Provide time tracking and workload visibility integrated into project execution flows
- [ ] Establish freemium model with practical free-tier limits (members/projects/tasks) and paid expansion path
- [ ] Keep v1 role model focused on Admin/Owner, PM/Team Lead, Employee, and HR

### Out of Scope

- Full-featured messenger in v1 — chat starts as paid/limited capability and can expand later
- Mobile native applications — web-first delivery for v1 focus and speed
- Broad marketplace-style integrations in v1 — avoid scope explosion until core value is proven

## Context

The repository already moved from microservices to a modular monolith backend (`backend/app/`) with feature boundaries (`auth`, `telegram`, `employees`, `profile`, `vacations`, `calendar`). The design source (`design/crm.pen`) captures broader product scope including dashboard, projects, calendar, employees, vacations, messenger, info portal, and onboarding flows. Current strategic direction is to prioritize project execution and cross-team delivery visibility, then layer additional modules. Monetization direction is freemium with soft free limits and feature expansion through paid plans.

## Constraints

- **Tech stack**: Keep current stack (FastAPI + Next.js + PostgreSQL + Redis) — preserves momentum and reduces migration risk
- **Timeline**: v1 target is 2-3 months — requires strict scope control around project-first workflows
- **Product scope**: Prioritize delivery workflows before broad communication/collaboration scope — protects time-to-value
- **Architecture**: Maintain modular monolith boundaries — supports solo/small-team execution speed while preserving future extraction paths

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use modular monolith over distributed microservices | Solo/small-team execution speed and lower ops overhead | ✓ Good |
| v1 is project-first for medium IT teams (30-200) | Fastest path to measurable delivery impact | — Pending |
| Freemium with soft free limits and paid expansion | Lower adoption friction plus monetization path | — Pending |
| Roles in v1: Admin/Owner, PM/Team Lead, Employee, HR | Covers core planning, execution, and workforce context needs | — Pending |

---
*Last updated: 2026-03-17 after initialization*
