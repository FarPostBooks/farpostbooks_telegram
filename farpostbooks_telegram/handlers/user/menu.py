import logging
from datetime import datetime
from typing import Any

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, Back, Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from tortoise.query_utils import Prefetch

from farpostbooks_telegram.misc.states import SearchBook
from farpostbooks_telegram.models.users import BookModel, UserBookModel


async def search(_: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        SearchBook.isbn,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )


async def my_book(message: Message, dialog_manager: DialogManager):
    book = await UserBookModel.get_or_none(
        user_id=message.from_user.id,
        back_timestamp__isnull=True
    )
    if book is None:
        await message.answer(
            '<b>📚 У вас еще нет книги, вы можете взять её в боте или на сайте.</b>'
        )
        return

    await dialog_manager.start(
        SearchBook.book,
        data={'isbn': book.book_id},
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )


def rating_button_creator():
    buttons = []
    for index in range(1, 6):
        buttons.append(
            Button(
                Const(str(f'{index} ⭐️')),
                id=str(index),
                on_click=on_rating_selected
            )
        )
    return buttons


def generate_book_info(book: BookModel, on_shelf: bool):
    return (
        f'<b>#️⃣ ISBN:</b> <code>{book.id}</code>\n'
        f'<b>📔 Название:</b> <code>{book.name}</code>\n'
        f'<b>📔 Описание:</b> <code>{book.description[:200]}...</code>\n'
        f'<b>👤 Авторство:</b> <code>{book.author}</code>\n'
        f'<b>📆 Дата публикации:</b> <code>{book.publish}</code>\n\n'
        f'<b>🗄 Книга на полке?</b> <code>{"Да" if on_shelf else "Нет"}</code>'
    )


async def get_data(dialog_manager: DialogManager, **_):
    book = await BookModel.filter(
        id=dialog_manager.dialog_data.get('isbn', dialog_manager.start_data.get('isbn'))
    ).first().prefetch_related(
        Prefetch('user_books', UserBookModel.filter(back_timestamp__isnull=True))
    )
    on_shelf = not book.user_books
    return {
        'dialog_data': 'isbn' in dialog_manager.dialog_data,
        'path': f'images/{book.image}',
        'message': generate_book_info(book, on_shelf),
        'on_shelf': on_shelf
    }


async def send_book(message: Message, _: MessageInput, manager: DialogManager):
    try:
        isbn = int(message.text)
    except ValueError:
        manager.dialog_data['isbn_error'] = (
            '<b>😥 Похоже вы ошиблись при указании ISBN книги.\nПопробуйте снова.</b>',
        )
        return

    book = await BookModel.filter(id=isbn).first().prefetch_related(
        Prefetch('user_books', UserBookModel.filter(back_timestamp__isnull=True))
    )

    if book is None:
        manager.dialog_data['isbn_error'] = (
            '<b>😥 Не удалось найти книгу по заданному ISBN.\nПопробуйте снова.</b>',
        )
        return

    if 'isbn_error' in manager.dialog_data:
        del manager.dialog_data['isbn_error']

    manager.dialog_data['isbn'] = isbn
    await manager.next()


async def take_book(query: CallbackQuery, _: Any, manager: DialogManager):
    isbn: int = manager.dialog_data.get('isbn', manager.start_data.get('isbn'))

    if await UserBookModel.get_or_none(
        user_id=query.from_user.id,
        back_timestamp__isnull=True,
    ) is not None:
        await query.answer('📔 У вас уже есть книга!')
        return

    if await UserBookModel.get_or_none(
        book_id=isbn,
        back_timestamp__isnull=True,
    ) is not None:
        await query.answer('📔 Кто-то уже взял эту книгу!')
        return

    await UserBookModel.create(
        user_id=query.from_user.id,
        book_id=isbn,
    )


async def return_book(query: CallbackQuery, _: Any, manager: DialogManager):
    isbn: int = manager.dialog_data.get('isbn', manager.start_data.get('isbn'))

    book = await UserBookModel.get_or_none(
        user_id=query.from_user.id,
        book_id=isbn,
        back_timestamp__isnull=True,
    )
    if book is None:
        await query.answer('📔 Эта книга принадлежит не вам.')
        return
    await manager.switch_to(SearchBook.rating)


async def on_rating_selected(
    query: CallbackQuery,
    widget: Any,
    manager: DialogManager,
):
    await UserBookModel.filter(
        user_id=query.from_user.id,
        book_id=manager.dialog_data.get('isbn', manager.start_data.get('isbn')),
    ).update(
        back_timestamp=datetime.utcnow(),
        rating=int(query.data),
    )
    await manager.switch_to(SearchBook.book)


book_dialog = Dialog(
    Window(
        Const(
            '<b>🌐 Если вы знаете ISBN книги <i>(обычно он находится на задней '
            'стороне книги)</i> введите его и я найду для вас книгу.</b>',
            when=~F['isbn_error']
        ),
        Format('{message}', when=F['isbn_error']),
        MessageInput(send_book),
        Cancel(Const('🚪 Выйти')),
        state=SearchBook.isbn,
    ),
    Window(
        StaticMedia(
            path=Format('{path}'),
        ),
        Format("{message}"),
        Button(
            Const('📗 Взять книгу'),
            id='take_book',
            on_click=take_book,
            when=F['on_shelf']
        ),
        Button(
            Const('📕 Вернуть книгу'),
            id='return_book',
            on_click=return_book,
            when=~F['on_shelf']
        ),
        Row(
            Back(Const('🔙 Назад'), when=F['dialog_data']),
            Cancel(Const('🚪 Выйти')),
        ),
        getter=get_data,
        state=SearchBook.book,
    ),
    Window(
        Const('<b>🌟 Перед тем, как положить книгу на место, поставьте ей оценку '
              'от <code>1 до 5</code>, нажав на одну из кнопок снизу.</b>'),
        Row(
            *rating_button_creator(),
        ),
        Row(
            Back(Const('🔙 Назад')),
            Cancel(Const('🚪 Выйти')),
        ),
        state=SearchBook.rating
    ),
)
