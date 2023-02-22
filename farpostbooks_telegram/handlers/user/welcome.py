from aiogram.types import Message

from farpostbooks_telegram.keyboards import reply


async def start(message: Message):
    await message.answer(
        '<b>👁 Добро пожаловать в корпоративную библиотеку FarPost.</b>',
        reply_markup=reply.menu.as_markup(resize_keyboard=True)
    )
