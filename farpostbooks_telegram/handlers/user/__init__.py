from aiogram import Router, F
from aiogram.filters import Command

from farpostbooks_telegram.filters.guest import GuestFilter
from farpostbooks_telegram.handlers.user.menu import (
    search,
    send_book,
    take_book,
    my_book,
)
from farpostbooks_telegram.handlers.user.welcome import start

user_router = Router()
user_router.message.filter(~GuestFilter())

user_router.message.register(start, Command(commands=['start']))
user_router.message.register(search, F.text == '🔍 Поиск по ISBN')
user_router.message.register(my_book, F.text == '📖 Моя книга')
