from datetime import date

from pyrogram import filters, Client
from pyrogram.types import Message
from sqlalchemy import select

from src.common.database import async_session
from src.models.user import User


@Client.on_message(filters.me & filters.command("users_today"))
async def users_today_command(_, message: Message) -> None:
    async with async_session() as session:
        stmt = select(User).where(User.created_at == date.today())
        result = await session.execute(stmt)

        users = result.scalars().all()

    await message.reply_text(
        f"ℹ️ Сегодня зарегистрировано: {str(len(users))} человек.", quote=True
    )
