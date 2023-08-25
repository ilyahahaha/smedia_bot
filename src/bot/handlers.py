from loguru import logger
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.private)
async def any_message(_, message: Message) -> None:
    logger.info(f"Got message from user (UserID: {message.from_user.id})")

    await message.reply_text(message.text)
