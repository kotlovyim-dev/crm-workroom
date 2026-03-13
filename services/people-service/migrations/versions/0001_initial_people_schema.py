"""initial people schema

Revision ID: 0001_initial_people_schema
Revises:
Create Date: 2026-03-13 00:00:00

"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_people_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("avatar_url", sa.String(length=1024), nullable=True),
        sa.Column("position", sa.String(length=160), nullable=False),
        sa.Column("level", sa.String(length=32), nullable=False, server_default="mid"),
        sa.Column("role_label", sa.String(length=120), nullable=False, server_default="Member"),
        sa.Column("employment_type", sa.String(length=32), nullable=False, server_default="full_time"),
        sa.Column("hire_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_employees_user_id"),
    )
    op.create_index("ix_employees_workspace_id", "employees", ["workspace_id"], unique=False)
    op.create_index("ix_employees_user_id", "employees", ["user_id"], unique=True)
    op.create_index("ix_employees_email", "employees", ["email"], unique=False)
    op.create_index(
        "ix_employees_workspace_search",
        "employees",
        ["workspace_id", "last_name", "first_name", "email"],
        unique=False,
    )

    op.create_table(
        "employee_profiles",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("employee_id", sa.String(length=36), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("birthday", sa.Date(), nullable=True),
        sa.Column("mobile_number", sa.String(length=32), nullable=True),
        sa.Column("skype", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("employee_id", name="uq_employee_profiles_employee_id"),
    )
    op.create_index("ix_employee_profiles_employee_id", "employee_profiles", ["employee_id"], unique=True)

    op.create_table(
        "notification_settings",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("employee_id", sa.String(length=36), nullable=False),
        sa.Column("issue_activity_email", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("tracking_activity_push", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("new_comments_push", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("silent_hours_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("silent_hours_after", sa.Time(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("employee_id", name="uq_notification_settings_employee_id"),
    )
    op.create_index(
        "ix_notification_settings_employee_id",
        "notification_settings",
        ["employee_id"],
        unique=True,
    )

    op.create_table(
        "vacation_balances",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("employee_id", sa.String(length=36), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("vacation_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("vacation_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sick_leave_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sick_leave_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("remote_days_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("remote_days_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_vacation_balances_employee_id", "vacation_balances", ["employee_id"], unique=False)
    op.create_index("ix_vacation_balances_year", "vacation_balances", ["year"], unique=False)
    op.create_index(
        "ix_vacation_balances_employee_year",
        "vacation_balances",
        ["employee_id", "year"],
        unique=True,
    )

    op.create_table(
        "time_off_requests",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("employee_id", sa.String(length=36), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("duration_type", sa.String(length=16), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("time_from", sa.Time(), nullable=True),
        sa.Column("time_to", sa.Time(), nullable=True),
        sa.Column("requested_units", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("updated_by", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_time_off_requests_workspace_id", "time_off_requests", ["workspace_id"], unique=False)
    op.create_index("ix_time_off_requests_employee_id", "time_off_requests", ["employee_id"], unique=False)
    op.create_index("ix_time_off_requests_type", "time_off_requests", ["type"], unique=False)
    op.create_index("ix_time_off_requests_status", "time_off_requests", ["status"], unique=False)
    op.create_index(
        "ix_time_off_requests_workspace_timeline",
        "time_off_requests",
        ["workspace_id", "start_date", "end_date", "status", "type"],
        unique=False,
    )

    op.create_table(
        "calendar_events",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("duration_label", sa.String(length=32), nullable=True),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("color_accent", sa.String(length=32), nullable=True),
        sa.Column("trend", sa.String(length=32), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("updated_by", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_calendar_events_workspace_id", "calendar_events", ["workspace_id"], unique=False)
    op.create_index("ix_calendar_events_date", "calendar_events", ["date"], unique=False)
    op.create_index("ix_calendar_events_type", "calendar_events", ["type"], unique=False)
    op.create_index(
        "ix_calendar_events_workspace_date_range",
        "calendar_events",
        ["workspace_id", "date", "type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_calendar_events_workspace_date_range", table_name="calendar_events")
    op.drop_index("ix_calendar_events_type", table_name="calendar_events")
    op.drop_index("ix_calendar_events_date", table_name="calendar_events")
    op.drop_index("ix_calendar_events_workspace_id", table_name="calendar_events")
    op.drop_table("calendar_events")

    op.drop_index("ix_time_off_requests_workspace_timeline", table_name="time_off_requests")
    op.drop_index("ix_time_off_requests_status", table_name="time_off_requests")
    op.drop_index("ix_time_off_requests_type", table_name="time_off_requests")
    op.drop_index("ix_time_off_requests_employee_id", table_name="time_off_requests")
    op.drop_index("ix_time_off_requests_workspace_id", table_name="time_off_requests")
    op.drop_table("time_off_requests")

    op.drop_index("ix_vacation_balances_employee_year", table_name="vacation_balances")
    op.drop_index("ix_vacation_balances_year", table_name="vacation_balances")
    op.drop_index("ix_vacation_balances_employee_id", table_name="vacation_balances")
    op.drop_table("vacation_balances")

    op.drop_index("ix_notification_settings_employee_id", table_name="notification_settings")
    op.drop_table("notification_settings")

    op.drop_index("ix_employee_profiles_employee_id", table_name="employee_profiles")
    op.drop_table("employee_profiles")

    op.drop_index("ix_employees_workspace_search", table_name="employees")
    op.drop_index("ix_employees_email", table_name="employees")
    op.drop_index("ix_employees_user_id", table_name="employees")
    op.drop_index("ix_employees_workspace_id", table_name="employees")
    op.drop_table("employees")
