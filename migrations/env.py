import asyncio

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.settings import Settings
from src.models.base import Base

target_metadata = Base.metadata

settings = Settings()


def do_run_migrations(connection):
    context.configure(
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(
        settings.postgres_url.unicode_string(), future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


asyncio.run(run_migrations_online())
