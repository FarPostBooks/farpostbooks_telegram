import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message

from farpostbooks_telegram.models.users import UserModel


class GuestFilter(BaseFilter):
    async def __call__(self, obj: Message) -> bool:
        user = await UserModel.get_or_none(id=obj.from_user.id)
        return user is None
