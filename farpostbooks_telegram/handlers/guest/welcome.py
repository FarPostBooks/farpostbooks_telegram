from aiogram.types import Message


async def start(message: Message):
    await message.answer(
        '<b>👁 Добро пожаловать в корпоративную библиотеку FarPost.</b>\n'
        'Чтобы взаимодействовать с ботом требуется зарегистрироваться на сайте.',
    )
