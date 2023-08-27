from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings import Settings

settings = Settings()

engine = create_async_engine(
    settings.postgres_url.unicode_string(),
    future=True,
    echo=False,
)

async_session = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)
