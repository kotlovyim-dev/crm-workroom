# Phase 1: Access, Roles, and Workspace Trust Boundary (Week 1-2) - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

## Phase Boundary

Phase 1 delivers stable workspace onboarding/auth/session behavior and role-based trust enforcement for protected API/UI actions. Scope is limited to AUTH-01 through AUTH-04: signup/login, refresh-session continuity, invitation flow, role policy enforcement, and cross-workspace trust behavior.

## Implementation Decisions

### Invitation Lifecycle (AUTH-03)
- Who can invite: Admin/Owner and PM/Team Lead can send invites.
- Invite expiry: 7 days.
- Existing email behavior: if email is already in the same workspace, reject duplicate invite; if email belongs to another workspace, invite is allowed.
- Required invitation management in v1: view pending invites, resend invite, cancel/revoke pending invite.
- New-user acceptance: invite link opens signup with workspace prefilled; user creates account in that workspace.
- Existing-user acceptance (different workspace): force account transfer with explicit alert/confirmation.
- Expired invite UX: dedicated "Invite expired" error page with CTA to request a new invite.
- Post-accept destination: invited workspace dashboard.

### Role Assignment Rules (AUTH-04)
- Canonical v1 roles used for authorization: Admin/Owner, PM/Team Lead, Employee, HR.
- Workspace creator default role: Admin/Owner.
- Invite flow role assignment: inviter must select a role from canonical set.
- Role change authority after activation: Admin/Owner only.
- PM/Team Lead cannot change roles.
- Pending invite role can be edited before acceptance.
- No self-role changes in v1.
- UI role copy must use canonical labels only (no workspace-custom role names).

### Session Behavior UX (AUTH-01, AUTH-02)
- Remember-me semantics:
  - unchecked -> browser session cookie only,
  - checked -> persistent refresh session (30 days).
- Multi-device behavior: multiple active sessions are allowed.
- Logout scope: revoke only the current device session.
- Expired-session UX: attempt one silent refresh, then redirect to login with "Session expired" message.

### Unauthorized and Cross-Workspace UX
- Cross-workspace resource access should return 404 to avoid existence leakage.
- Same-workspace but insufficient role should return 403 with standardized forbidden message.
- Forbidden route UX: explicit "Access denied" page with back-to-dashboard CTA.
- Navigation behavior for restricted roles: hide restricted menu items entirely.

### Claude's Discretion
- Exact UI wording for inline validation and toast copy can be finalized during planning/implementation as long as it preserves decisions above.
- Exact interaction styling of invite/forbidden states is flexible if behavior remains unchanged.

## Specific Ideas

- Existing-user invite acceptance should include a clear transfer warning ("Force account transfer with alert").
- Session expiration should feel graceful (single silent refresh attempt before redirect).

## Canonical References

Downstream agents MUST read these before planning or implementing.

### Product and Scope
- `.planning/PROJECT.md` - v1 strategic constraints, role model expectation, and non-negotiable design-source rule.
- `.planning/REQUIREMENTS.md` - AUTH-01..AUTH-04 requirement definitions.
- `.planning/ROADMAP.md` - Phase 1 boundary and observable success criteria.
- `.planning/STATE.md` - current planning state and active sequencing constraints.

### Design Contract
- `design/crm.pen` - mandatory UX/flow conformance source for implemented auth and workspace interactions.

## Existing Code Insights

### Reusable Assets
- `backend/app/features/auth/routes.py` - complete auth route surface already exists (`/login`, `/register-workspace`, `/refresh`, `/logout`, `/me`, `/validate-token`).
- `backend/app/features/auth/service.py` - login, workspace registration, refresh-session rotation, cookie settings, and invitation creation primitives are already implemented.
- `backend/app/features/auth/models.py` - source-of-truth entities for `Workspace`, `User`, `Invitation`, `RefreshSession`.
- `web/src/modules/auth/api/auth.ts` - frontend auth query/mutation layer with session cache wiring.
- `web/src/lib/api/client.ts` - centralized 401 interceptor with single-flight refresh retry logic.
- `web/src/modules/auth/components/session-guard.tsx` and `web/src/modules/auth/components/guest-guard.tsx` - existing route gating primitives.

### Established Patterns
- Tenant context for non-auth feature routes is propagated via `X-User-Id` and `X-Workspace-Id` headers (`backend/app/features/shared/dependencies.py`).
- Domain service pattern scopes reads by `workspace_id` in queries (for example employees/calendar services), which can be reused for new protected endpoints.
- Frontend session state is centrally represented by `/api/v1/auth/me` query and react-query cache updates on login/register/logout.

### Integration Points and Gaps To Address In Planning
- `backend/app/features/auth/schemas.py` currently stores `role_description` as free text; phase planning must align persisted values with canonical role set.
- `backend/app/features/employees/routes.py` and `backend/app/features/employees/services.py` include an invite endpoint, but it is currently a stub response and not tied to invitation lifecycle states/actions.
- `/api/v1/auth/validate-token` currently forwards user and workspace headers only; role propagation/enforcement contract is not yet formalized.
- Current repo has no backend auth integration tests (`backend/tests/` absent), so phase tasks must add explicit end-to-end and negative-path coverage for auth/session/invite/cross-workspace rules.

## Deferred Ideas

- None. Discussion stayed within Phase 1 scope.

*Phase: 01-access-roles-and-workspace-trust-boundary-week-1-2*
*Context gathered: 2026-03-17*