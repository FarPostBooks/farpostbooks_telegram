import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry
from tortoise import Tortoise

from farpostbooks_telegram.handlers.guest import guest_router
from farpostbooks_telegram.handlers.user import user_router
from farpostbooks_telegram.handlers.user.menu import book_dialog
from farpostbooks_telegram.models.config import TORTOISE_CONFIG
from farpostbooks_telegram.settings import settings

logger = logging.getLogger(__name__)


async def run_database() -> bool:
    try:
        await Tortoise.init(TORTOISE_CONFIG)
        return True
    except Exception as error:
        logger.error(f'Не удалось запустить базу данных. Ошибка: {error}')
        return False


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] '
               u'- %(name)s - %(message)s',
    )
    logger.info("Запуск бота")

    storage = MemoryStorage()
    bot = Bot(token=settings.bot_token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for router in [
        guest_router,
        user_router,
    ]:
        dp.include_router(router)

    registry = DialogRegistry(dp)
    registry.register(book_dialog)

    dp.message.filter(F.chat.type == 'private')
    if await run_database():
        await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Бот был выключен!')
