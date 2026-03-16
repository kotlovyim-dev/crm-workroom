# Phase 1 Research: Access, Roles, and Workspace Trust Boundary (Week 1-2)

Phase scope validation (AUTH-01..AUTH-04):
- AUTH-01 (workspace signup/login): covered by recommendations for credential flow hardening, canonical role assignment at registration, and auth route contracts.
- AUTH-02 (refresh session continuity): covered by refresh rotation/revocation semantics, cookie policy, retry/refresh client behavior, and token/session lifecycle checks.
- AUTH-03 (workspace invites): covered by invitation state model, expiry/reissue/revoke flow, and acceptance transfer rules.
- AUTH-04 (RBAC): covered by canonical role enum, policy dependency layer, and cross-workspace 404 + same-workspace 403 enforcement.

## Standard Stack

Recommended implementation stack for this phase (ecosystem mode):
- Backend API/auth: FastAPI dependencies + security utilities, keeping auth checks in dependency/policy functions close to data access.
  - Confidence: High
  - Why: FastAPI security/dependency model is the intended pattern for bearer/cookie auth composition and OpenAPI security declaration.
  - Source: FastAPI Security tutorials (`/tutorial/security/first-steps/`, `/tutorial/security/oauth2-jwt/`)
- Session model: short-lived access token + server-stored rotating refresh sessions in DB (`refresh_sessions`), delivered as HttpOnly cookies.
  - Confidence: High
  - Why: current code already uses this shape (`RefreshSession`, cookie rotation), and OWASP guidance strongly favors strict server-side session lifecycle controls.
  - Source: OWASP Session Management Cheat Sheet; existing code in `backend/app/features/auth/service.py` and `backend/app/features/auth/routes.py`
- JWT profile: signed JWT access token with strict algorithm allowlist and explicit claim validation (`exp`, `sub`, `workspace_id`, plus `iss`/`aud` where possible).
  - Confidence: High
  - Why: RFC 8725 mandates algorithm verification and audience/issuer validation for substitution/confusion resistance.
  - Source: RFC 8725 sections 3.1, 3.8, 3.9, 3.12
- Data access/transactions: SQLAlchemy 2.0 explicit transaction boundaries (`session.begin()`), especially for auth-critical multi-step writes.
  - Confidence: High
  - Why: SQLAlchemy 2.0 semantics are explicit; auth workflows should avoid partial commits across user/session mutation chains.
  - Source: SQLAlchemy 2.0 docs (`orm/session_transaction.html`)
- Frontend auth state: Next.js app-router + TanStack Query with centralized auth query and Axios interceptor for single-flight refresh.
  - Confidence: High
  - Why: current code already has interceptor single-flight and session query; tighten retry semantics to avoid auth loops.
  - Source: Next.js auth guide, TanStack Query retry docs, current code in `web/src/lib/api/client.ts`, `web/src/modules/auth/api/auth.ts`

## Architecture Patterns

1. Auth context and trust-boundary layering
- Pattern:
  - Cookie/token validation in auth boundary dependency.
  - Convert to typed `AuthContext(user_id, workspace_id, role)`.
  - Apply RBAC/capability checks in dedicated policy dependency.
  - Apply workspace scoping in every query (`WHERE workspace_id = auth_context.workspace_id`).
- Prescriptive implementation:
  - Extend `/auth/validate-token` to also emit `X-User-Role` once role is canonicalized.
  - Add reusable dependency: `require_roles(*allowed)` for route-level enforcement.
  - Keep 404 for cross-workspace resource lookups and 403 only for same-workspace insufficient role.
- Confidence: High

2. Canonical role model (AUTH-04)
- Current gap:
  - `role_description` is free text in schemas/models.
- Prescriptive implementation:
  - Introduce canonical enum in backend (`owner_admin`, `pm_team_lead`, `employee`, `hr`) and map to UI labels.
  - Enforce enum at Pydantic schema boundaries and DB check constraint.
  - Add policy matrix module (capability -> allowed roles).
- Confidence: High

3. Session lifecycle and rotation (AUTH-02)
- Pattern:
  - Access token stateless and short TTL.
  - Refresh token opaque, hashed in DB, one-record rotation per use.
  - On logout, revoke only current refresh session (matches current phase decision).
- Prescriptive implementation:
  - Keep single-flight client refresh (`refreshRequest` promise) and reject on refresh failure to avoid hidden loops.
  - Add refresh reuse detection path (if previous token replayed, revoke session family/device as policy choice).
  - Add idle and absolute timeout fields on `RefreshSession` if not already encoded only by `expires_at`.
- Confidence: Medium-High

4. Invitation lifecycle as state machine (AUTH-03)
- Pattern:
  - `pending -> accepted | expired | revoked`.
  - Explicit expiry timestamp and token hash (not raw token storage).
- Prescriptive implementation:
  - Add fields: `role`, `expires_at`, `accepted_at`, `revoked_at`, `invited_email_normalized`.
  - API set:
    - `POST /invitations` (Admin/Owner + PM/Lead allowed to create)
    - `GET /invitations?status=pending`
    - `POST /invitations/{id}/resend`
    - `POST /invitations/{id}/revoke`
    - `POST /invitations/accept` (handles new/existing user transfer semantics)
  - Enforce idempotency and duplicate-email-in-workspace rejection.
- Confidence: High

5. Transaction boundaries for auth workflows
- Current risk:
  - login updates `last_login` and commits before refresh session creation, so partial success is possible.
- Prescriptive implementation:
  - Wrap login/update/refresh-session creation in one transaction per request path where atomicity is required.
  - Use `with session.begin():` style at service boundary for multi-write flows.
- Confidence: Medium-High

6. Next.js and TanStack auth UX safety
- Pattern:
  - Route guards are UX helpers only; secure checks happen at API/data layer.
  - Disable or customize retries for auth-sensitive queries.
- Prescriptive implementation:
  - For `useSessionQuery`, set `retry: false` or retry only non-401 errors.
  - Keep redirect-on-expired behavior but add deterministic expired-message state.
  - Do not rely only on layout-level checks; apply checks at page/data fetch boundaries.
- Confidence: High

## Don't Hand-Roll

- Do not invent custom crypto, token formats, or random generators.
  - Use vetted libraries and strict algorithm allowlists.
  - Confidence: High
  - Source: RFC 8725, FastAPI JWT guidance
- Do not store access/refresh tokens in `localStorage` for this architecture.
  - Keep HttpOnly cookies for session secrets.
  - Confidence: High
  - Source: OWASP Session Management Cheat Sheet
- Do not use permissive session ID acceptance (accepting arbitrary user-provided session identifiers).
  - Enforce strict server-issued token/session IDs only.
  - Confidence: High
  - Source: OWASP Session Management Cheat Sheet
- Do not encode role or workspace policy solely in frontend guards.
  - UI hiding is not authorization.
  - Confidence: High
  - Source: Next.js auth docs (secure checks close to data source)
- Do not let TanStack default retry behavior handle auth errors blindly.
  - Default retries can amplify 401/refresh loops and delay redirects.
  - Confidence: High
  - Source: TanStack Query retry docs

## Common Pitfalls

- Free-text roles lead to policy drift and bypasses.
  - Fix: enum + check constraints + centralized capability map.
  - Confidence: High
- Missing `aud`/`iss` validation enables token substitution across contexts.
  - Fix: include and validate audience/issuer in decode path.
  - Confidence: High
- Split commits in auth flow cause partial state (e.g., last_login updated but session creation failed).
  - Fix: explicit transaction boundaries.
  - Confidence: Medium-High
- Over-broad cookie `Domain` and permissive `Path` increase cross-app leakage risk.
  - Fix: narrow scope; avoid unnecessary domain-wide cookies.
  - Confidence: High
- Returning 403 for cross-workspace object access leaks object existence.
  - Fix: return 404 for cross-workspace misses, 403 only for same-tenant privilege failures.
  - Confidence: High
- Client-side session guard null-render loops can degrade UX and conceal auth faults.
  - Fix: explicit loading/error/expired states and one refresh attempt policy.
  - Confidence: Medium
- Auth query retries + interceptor refresh can double-retry unexpectedly.
  - Fix: auth query `retry: false`; conditional retry function for non-auth data queries.
  - Confidence: High

## Code Examples

### 1) Canonical role enum + policy dependency (FastAPI)

```python
from enum import StrEnum
from fastapi import Depends, HTTPException, status

class WorkspaceRole(StrEnum):
    OWNER_ADMIN = "owner_admin"
    PM_TEAM_LEAD = "pm_team_lead"
    EMPLOYEE = "employee"
    HR = "hr"

class AuthContext(BaseModel):
    user_id: str
    workspace_id: str
    role: WorkspaceRole


def require_roles(*allowed: WorkspaceRole):
    async def dependency(ctx: AuthContext = Depends(get_current_auth_context)) -> AuthContext:
        if ctx.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return ctx
    return dependency
```

### 2) Workspace-safe loader (404 cross-tenant)

```python
from sqlalchemy import select
from fastapi import HTTPException, status

async def get_project_or_404(session: AsyncSession, project_id: str, workspace_id: str) -> Project:
    project = await session.scalar(
        select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id)
    )
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return project
```

### 3) Atomic login + refresh session issue (SQLAlchemy 2.0)

```python
async def login_and_issue_session(session: AsyncSession, payload: LoginRequest, request: Request) -> AuthResponse:
    async with session.begin():
        user = await authenticate_user(session, payload.email, payload.password)
        user.last_login = datetime.now(UTC)
        refresh_token = await create_refresh_session_in_tx(session, user, request, payload.remember_me)

    access_token = build_access_token(user)
    return AuthBundle(auth=build_auth_response(user), access_token=access_token, refresh_token=refresh_token)
```

### 4) JWT validation profile hardening

```python
def decode_access_token_strict(token: str, settings: Settings) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],  # explicit allowlist
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
        options={"require": ["exp", "sub", "workspace_id", "iss", "aud"]},
    )
```

### 5) TanStack Query auth-safe retry config

```ts
export function useSessionQuery(enabled = true) {
  return useQuery({
    queryKey: queryKeys.auth.session(),
    queryFn: getSession,
    enabled,
    retry: false,
    staleTime: 30_000,
  })
}

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error: any) => {
        const status = error?.response?.status
        if (status === 401 || status === 403) return false
        return failureCount < 2
      },
    },
  },
})
```

### 6) Invitation schema shape for AUTH-03

```python
class InvitationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
    REVOKED = "revoked"

class Invitation(Base):
    __tablename__ = "invitations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    email: Mapped[str] = mapped_column(String(320), index=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=InvitationStatus.PENDING.value)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

Critical source anchors used for this research:
- FastAPI security/auth patterns:
  - https://fastapi.tiangolo.com/tutorial/security/first-steps/
  - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- OWASP session guidance:
  - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- JWT best current practice:
  - https://www.rfc-editor.org/rfc/rfc8725
- SQLAlchemy transaction semantics:
  - https://docs.sqlalchemy.org/en/20/orm/session_transaction.html
- Next.js auth UX/authorization placement:
  - https://nextjs.org/docs/app/guides/authentication
- TanStack Query retries:
  - https://tanstack.com/query/latest/docs/framework/react/guides/query-retries
