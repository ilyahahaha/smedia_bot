from loguru import logger
from pyrogram.types import Message

from src import app, scheduler
from src.database import async_session
from src.models import User


async def idle(message: Message) -> None:
    # Костыль для избавления от циклического импорта
    from src.bot.messages.welcome import welcome as welcome_message

    logger.info(f"Starting idle job. (UserID: {message.from_user.id})")
    message_history = [item async for item in app.get_chat_history(message.chat.id)]

    scheduler.remove_job(f"idle-{message.from_user.id}")

    # Проверка на триггер
    async with async_session() as session:
        user = await User.find_by_user_id(session, user_id=str(message.from_user.id))

        if any(
            m.text is not None and m.text.lower() == "хорошего дня"
            for m in message_history
        ):
            user.is_paused = True
            await user.save(session)

            await app.send_message(
                chat_id=message.chat.id,
                text="Воронка закончена...\nДля запуска с первого этапа, напишите: 'Привет!'",
            )

            return logger.info(
                f"User called pause. Ignoring for next jobs... (UserID: {message.from_user.id}"
            )

    await app.send_message(
        chat_id=message.chat.id, text="Скоро вернусь с новым материалом!"
    )

    scheduler.add_job(
        welcome_message,
        id=f"welcome-{message.from_user.id}",
        trigger="interval",
        minutes=1,
        kwargs={"message": message},
    )

    logger.success(
        f"Finished all jobs! Switched to welcome. (UserID: {message.from_user.id})"
    )
