from dataclasses import dataclass

from fastapi import Header, HTTPException, status


@dataclass(frozen=True)
class AuthContext:
    user_id: str
    workspace_id: str


def get_auth_context(
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    x_workspace_id: str | None = Header(default=None, alias="X-Workspace-Id"),
) -> AuthContext:
    if not x_user_id or not x_workspace_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth context")

    return AuthContext(user_id=x_user_id, workspace_id=x_workspace_id)
