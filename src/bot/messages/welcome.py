from loguru import logger
from pyrogram.types import Message

from src import scheduler, app
from src.bot.messages.material import material as material_message


async def welcome(message: Message) -> None:
    logger.info(f"Starting welcome job. (UserID: {message.from_user.id})")

    await app.send_message(chat_id=message.chat.id, text="Добрый день!")
    logger.success(f"Welcome message sent! (UserID: {message.from_user.id})")

    scheduler.remove_job(f"welcome-{message.from_user.id}")
    scheduler.add_job(
        material_message,
        id=f"material-{message.from_user.id}",
        trigger="interval",
        minutes=1,
        kwargs={"message": message},
    )

    logger.success(f"Established next job! (UserID: {message.from_user.id})")
