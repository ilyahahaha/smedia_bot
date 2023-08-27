from random import randint

from pyrogram.types import Message


async def material(message: Message) -> None:
    """
    Присутствует задержка при отправке, т.к при каждом вызове используем randint,
    чтобы телеграм не кэшировал изображение и мы получали новое.
    Дополнительно задержка при получении изображения.
    """
    await message.reply_photo(
        photo=f"https://loremflickr.com/640/480?{randint(1, 999999)}",
        caption="Подготовила для вас материал",
    )
