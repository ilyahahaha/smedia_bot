from loguru import logger
from pyrogram import filters, Client
from pyrogram.types import Message

from src import scheduler, app
from src.bot.messages.welcome import welcome as welcome_message
from src.common.database import async_session
from src.models import User


@Client.on_message(~filters.me & filters.private)
async def entry(_, message: Message) -> None:
    logger.info(f"New message: '{message.text}' (UserID: {message.from_user.id})")

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
                scheduler.add_job(
                    welcome_message,
                    id=f"welcome-{user.user_id}",
                    trigger="interval",
                    minutes=1,
                    kwargs={"message": message},
                )

                logger.success(
                    f"Scheduled welcome job! (UserID: {message.from_user.id})"
                )

                await user.save(session)
            except Exception as ex:
                logger.exception(f"{ex} (UserID: {message.from_user.id})")

            logger.success(f"New user created! (UserID: {message.from_user.id})")

        # Проверка на триггер возобновления (в основном, для теста)
        if user.is_paused:
            if message.text.lower() != "привет!":
                return await app.send_message(
                    chat_id=message.chat.id,
                    text="Воронка закончена...\nДля запуска с первого этапа, напишите: 'Привет!'",
                )

            user.is_paused = False
            await user.save(session)

            scheduler.add_job(
                welcome_message,
                id=f"welcome-{user.user_id}",
                trigger="interval",
                minutes=1,
                kwargs={"message": message},
            )

            logger.success(f"User unpaused! (UserID: {message.from_user.id})")
            logger.success(f"Scheduled welcome job! (UserID: {message.from_user.id})")
