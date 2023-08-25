from loguru import logger
from pyrogram import Client

from src.common.settings import Settings

settings = Settings()

app = Client(name="smedia_bot", api_id=settings.api_id, api_hash=settings.api_hash, plugins=dict(root="bot"))

if __name__ == "__main__":
    logger.success("Bot started!")
    app.run()
