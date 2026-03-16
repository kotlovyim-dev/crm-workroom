# DevFlow CRM v1 Features (Project-First + Freemium)

## Scope Basis

Source inputs used for this research:
- Product direction from `.planning/PROJECT.md` (project-first, medium IT teams, freemium, 2-3 month window)
- Functional areas present in `design/crm.pen`: projects, employees, vacations, calendar, messenger, info portal, auth/onboarding
- Current implementation state: auth/session and people-adjacent APIs exist; full project management slice is still pending

Complexity scale:
- `S`: can be delivered quickly with existing foundations
- `M`: moderate cross-module work
- `L`: multi-domain work with higher product/technical risk

Dependency shorthand:
- `Auth`: login/session/roles/workspace access
- `Projects`: project, task, board, timeline, status models and APIs
- `People`: employees/profile data and assignment links
- `Calendar`: event aggregation and scheduling views
- `Vacations`: leave requests/approvals and policy rules
- `Messaging`: chat channels, mentions, file share, search
- `Portal`: docs/folders/sharing content model
- `Billing`: plan limits, entitlements, upgrade prompts
- `Infra`: notifications, background jobs, search/indexing, file storage

## Table Stakes (Must-Have for v1)

| Area | Feature | Freemium Position | Complexity | Key Dependencies | Notes |
|---|---|---|---|---|---|
| Auth | Signup, login, logout, refresh, workspace session | Free | S | Auth | Already present; keep reliable and frictionless for onboarding. |
| Auth | Role-based access (Admin/Owner, PM/Lead, Employee, HR) | Free | M | Auth | Required to safely expose project and people workflows. |
| Projects | Project list + project details baseline | Free | M | Projects, Auth | Core entry point in design (`Projects - List`, details screens). |
| Projects | Task CRUD with assignee, due date, status | Free | M | Projects, People, Auth | Minimum execution loop for project-first value. |
| Projects | Board view (kanban basics + drag/drop) | Free (limited active projects/tasks) | M | Projects, Auth | In design and critical for daily delivery operations. |
| Projects | Timeline view (read-first, simple dependencies) | Paid trial and above | L | Projects, Calendar, Auth | Keep initial timeline simple to ship in v1 window. |
| Projects | Progress visibility (per-project health and active task counts) | Free | M | Projects, Auth | Supports "single operational picture" promise. |
| Projects | Time tracking on task/project | Free (basic), advanced reports paid | L | Projects, People, Billing | Explicit active requirement in PROJECT.md. |
| Employees | Employee directory list and profile links | Free | S | People, Auth | Needed for assigning tasks and PM visibility. |
| Employees | Employee activity summary (project-related) | Paid | M | Projects, People, Billing | Design includes activity view; monetize richer analytics. |
| Vacations | Vacation request create/view workflow | Free | M | Vacations, People, Auth, Calendar | Enables realistic availability-aware project planning. |
| Calendar | Team calendar with project + vacation events | Free | M | Calendar, Projects, Vacations, Auth | Must aggregate delivery and availability context. |
| Dashboard | Nearest events + project workload snapshot | Free | M | Calendar, Projects, Auth | Existing dashboard shell aligns with this requirement. |
| Freemium | Free-tier limits enforcement (members/projects/tasks) | Free plan control | M | Billing, Auth, Projects, People | Required monetization backbone for v1 launch. |
| Freemium | Upgrade prompts and limit messaging in product | Paid conversion enabler | S | Billing, Auth | Keep non-blocking until hard limits are reached. |

## Differentiators (High-Value, Distinctive, Should Land in v1 if Capacity Allows)

| Area | Feature | Freemium Position | Complexity | Key Dependencies | Why It Differentiates |
|---|---|---|---|---|---|
| Projects + People | Unified workload lens (tasks + capacity + upcoming vacations) | Paid | L | Projects, People, Vacations, Calendar, Billing | Turns scattered signals into one delivery planning view. |
| Projects | Cross-project risk radar (blocked tasks, due soon, in-review bottlenecks) | Paid | L | Projects, Infra, Billing | Gives PMs and leads proactive intervention capability. |
| Projects + Time | Delivery velocity and estimate-vs-actual by project | Paid | L | Projects, People, Infra, Billing | Practical management insight absent in basic task tools. |
| Dashboard | Persona-aware dashboard cards (PM/HR/Employee perspectives) | Free basic, paid advanced cards | M | Auth, Projects, People, Vacations, Billing | Increases relevance without adding separate products. |
| Calendar | "Who is available for this sprint" planning mode | Paid | M | Calendar, Vacations, Projects, People, Billing | Directly supports project-first staffing decisions. |
| Projects UX | Fast project setup templates for IT delivery workflows | Free | M | Projects, Auth | Speeds activation and reduces blank-state churn. |

## Anti-Features for v1 (Explicitly Defer)

| Area | Deferred Feature | Reason for Deferral | Complexity if Included | Dependency Risk |
|---|---|---|---|---|
| Messenger | Full Slack/Teams replacement (channels, rich threading, bots, deep history) | PROJECT.md marks full messenger as out-of-scope for v1; distracts from project-first execution | L | Messaging, Infra, Search, Storage, Realtime |
| Integrations | Broad external marketplace/integration catalog | Explicitly out-of-scope in PROJECT.md; high surface area and support cost | L | Infra, Auth, Partner APIs |
| Mobile | Native iOS/Android apps | Explicitly out-of-scope for v1 timeline; web-first is faster | L | Separate mobile stack, API hardening |
| Portal | Advanced knowledge base (versioning, workflows, ACL matrix, comments) | Not required to prove project-first value in first release | M-L | Portal, Auth, Infra |
| Projects | Complex dependency engine (critical path, auto-scheduling optimization) | High algorithmic/product complexity; timeline can be lightweight first | L | Projects, Calendar, Infra |
| Billing | Multi-currency invoicing/tax/subscription automation depth | Not needed for initial freemium validation | M-L | Billing, Finance integrations |

## v1 Freemium Packaging Suggestion (Project-First)

- Free:
  - Core auth and workspace onboarding
  - Limited projects/tasks/members
  - Project list/details, basic task flow, board, base dashboard, base calendar, vacations request flow
- Paid:
  - Higher limits and team scale
  - Advanced timeline, workload analytics, activity insights, risk radar, velocity/time reporting
  - Messenger and info portal capabilities as add-ons or higher-tier unlocks

## Delivery Dependency Notes

- Foundational sequence for execution:
  1. `Auth + roles + plan entitlements`
  2. `Projects domain baseline (project/task/status)`
  3. `Board + details + basic dashboard metrics`
  4. `Time tracking + reporting primitives`
  5. `Calendar/Vacation aggregation`
  6. `Freemium enforcement and upgrades`
- Critical integration risk:
  - Workload and planning features depend on consistent identity across projects, employees, and vacations (`workspace_id`, user mapping, role permissions).
- Monetization risk:
  - Freemium fails without clean in-product limit visibility and low-friction upgrade paths; this should be treated as product-critical, not just billing backlog.
