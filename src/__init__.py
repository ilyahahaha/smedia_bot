from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client

from src.common.settings import Settings

settings = Settings()


app = Client(
    name="smedia_bot",
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    session_string=settings.session_string,
    in_memory=True,
    plugins=dict(root="bot"),
)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler_store = SQLAlchemyJobStore(
    url=settings.postgres_url.unicode_string().replace(
        "postgresql+asyncpg", "postgresql"
    )
)
scheduler.add_jobstore(scheduler_store)
