"""initial auth schema

Revision ID: 0001_initial_auth_schema
Revises:
Create Date: 2026-03-11 00:00:00

"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_auth_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "workspaces",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("business_direction", sa.String(length=255), nullable=False),
        sa.Column("usage_purpose", sa.String(length=255), nullable=False),
        sa.Column("team_size", sa.String(length=32), nullable=False),
        sa.Column("has_team", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.Text(), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("role_description", sa.String(length=255), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("phone_number", name="uq_users_phone_number"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_phone_number", "users", ["phone_number"], unique=True)

    op.create_table(
        "invitations",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("invited_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["invited_by_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_invitations_email", "invitations", ["email"], unique=False)

    op.create_table(
        "refresh_sessions",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("rotation_counter", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("token_hash", name="uq_refresh_sessions_token_hash"),
    )
    op.create_index("ix_refresh_sessions_user_id", "refresh_sessions", ["user_id"], unique=False)
    op.create_index("ix_refresh_sessions_token_hash", "refresh_sessions", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_refresh_sessions_token_hash", table_name="refresh_sessions")
    op.drop_index("ix_refresh_sessions_user_id", table_name="refresh_sessions")
    op.drop_table("refresh_sessions")

    op.drop_index("ix_invitations_email", table_name="invitations")
    op.drop_table("invitations")

    op.drop_index("ix_users_phone_number", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    op.drop_table("workspaces")