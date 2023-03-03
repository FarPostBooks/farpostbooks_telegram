from aiogram.utils.keyboard import ReplyKeyboardBuilder

menu = ReplyKeyboardBuilder()
menu.button(text='🔍 Поиск по ISBN')
menu.button(text='📖 Моя книга')
menu.button(text='🎲 Рандомная книга')
menu.adjust(2, 1)
