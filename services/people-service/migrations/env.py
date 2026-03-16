from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import inspect, pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app import models  # noqa: F401
from app.config import get_settings
from app.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata
VERSION_TABLE = "alembic_version_people"
INITIAL_REVISION = "0001_initial_people_schema"


def _bootstrap_existing_schema_revision(connection: Connection) -> None:
    """Stamp initial revision when schema already exists in a reused database."""
    inspector = inspect(connection)
    tables = set(inspector.get_table_names())

    if "employees" not in tables:
        return

    if VERSION_TABLE not in tables:
        connection.execute(
            text(
                f"CREATE TABLE {VERSION_TABLE} (version_num VARCHAR(32) NOT NULL PRIMARY KEY)"
            )
        )
        connection.execute(
            text(f"INSERT INTO {VERSION_TABLE} (version_num) VALUES (:revision)"),
            {"revision": INITIAL_REVISION},
        )
        return

    current_revision = connection.execute(
        text(f"SELECT version_num FROM {VERSION_TABLE} LIMIT 1")
    ).scalar_one_or_none()
    if current_revision is None:
        connection.execute(
            text(f"INSERT INTO {VERSION_TABLE} (version_num) VALUES (:revision)"),
            {"revision": INITIAL_REVISION},
        )


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        version_table=VERSION_TABLE,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    _bootstrap_existing_schema_revision(connection)

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table=VERSION_TABLE,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
