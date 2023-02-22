from aiogram.filters.state import State, StatesGroup


class SearchBook(StatesGroup):
    isbn = State()
    book = State()
    rating = State()
