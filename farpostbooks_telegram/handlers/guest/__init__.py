from aiogram import Router
from aiogram.filters import Command

from farpostbooks_telegram.filters.guest import GuestFilter
from farpostbooks_telegram.handlers.guest.welcome import start

guest_router = Router()
guest_router.message.filter(GuestFilter())

guest_router.message.register(start, Command(commands=['start']))


