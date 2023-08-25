from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.common.settings import Settings

settings = Settings()

engine = create_async_engine(
    settings.postgres_url.unicode_string(),
    future=True,
    echo=True,
)

async_session = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)
