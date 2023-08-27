from random import randint

from loguru import logger
from pyrogram.types import Message

from src import scheduler, app
from src.bot.messages.idle import idle as idle_message


async def material(message: Message) -> None:
    logger.info(f"Starting material job. (UserID: {message.from_user.id})")

    """
    Присутствует задержка при отправке, т.к при каждом вызове используем randint,
    чтобы телеграм не кэшировал изображение и мы получали новое.
    Дополнительно задержка при получении изображения.
    """

    await app.send_photo(
        chat_id=message.chat.id,
        photo=f"https://loremflickr.com/640/480?{randint(1, 999999)}",
        caption="Подготовила для вас материал",
    )
    logger.success(f"Material sent! (UserID: {message.from_user.id})")

    scheduler.remove_job(f"material-{message.from_user.id}")
    scheduler.add_job(
        idle_message,
        id=f"idle-{message.from_user.id}",
        trigger="interval",
        minutes=120,
        kwargs={"message": message},
    )

    logger.success(f"Established next job! (UserID: {message.from_user.id})")
