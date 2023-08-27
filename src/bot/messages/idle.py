from pyrogram.types import Message


async def idle(message: Message) -> None:
    await message.reply_text("Добрый день!")
