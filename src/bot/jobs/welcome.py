from loguru import logger
from pyrogram.types import Message


async def welcome(message: Message) -> None:
    logger.info(f"{message.from_user.id}")
