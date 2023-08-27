from pyrogram.types import Message


async def welcome(message: Message) -> None:
    await message.reply_text("Добрый день!")
