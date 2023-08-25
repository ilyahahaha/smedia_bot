from loguru import logger
from pyrogram import Client, filters
from pyrogram.types import Message

from src.common.database import async_session
from src.models.user import User


@Client.on_message(~filters.me & filters.private)
async def any_message(_, message: Message) -> None:
    logger.info(f"Got message from user (UserID: {message.from_user.id})")

    async with async_session() as session:
        user = await User.find_by_user_id(session, str(message.from_user.id))

        if user is None:
            logger.info(
                f"User not found. Creating db entity... (UserID: {message.from_user.id})"
            )

            user = User(
                user_id=str(message.from_user.id),
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
            )

            try:
                await user.save(session)
            except Exception as ex:
                logger.exception(f"{ex} (UserID: {message.from_user.id})")

            logger.info(f"New user created! (UserID: {message.from_user.id})")

    logger.info(f"User found. (UserID: {message.from_user.id})")

    await message.reply_text(user.user_id)
