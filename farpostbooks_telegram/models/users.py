from tortoise import fields, Model


class BookModel(Model):
    """Модель для таблицы с книгами."""

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=128)  # noqa: WPS432
    description = fields.CharField(max_length=1024)  # noqa: WPS432
    image = fields.CharField(max_length=64)  # noqa: WPS432
    author = fields.CharField(max_length=255)  # noqa: WPS432
    publish = fields.CharField(max_length=16)  # noqa: WPS432
    added_timestamp = fields.DatetimeField(auto_now_add=True)

    user_books: fields.ReverseRelation["UserBookModel"]  # noqa: F821

    def __str__(self) -> str:
        return self.name


class UserModel(Model):
    """Модель для таблицы с юзерами."""

    id = fields.BigIntField(pk=True)
    status = fields.CharField(max_length=16, default="user")  # noqa: WPS432
    name = fields.CharField(max_length=64)  # noqa: WPS432
    position = fields.CharField(max_length=64)  # noqa: WPS432
    about = fields.CharField(max_length=255)  # noqa: WPS432
    timestamp = fields.DatetimeField(auto_now_add=True)

    books: fields.ReverseRelation["UserBookModel"]

    def __str__(self) -> str:
        return self.name


class UserBookModel(Model):
    """Модель для таблицы с книгами, которые были у юзеров."""

    id = fields.BigIntField(pk=True)
    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        model_name="models.UserModel",
        related_name="books",
        on_delete="CASCADE",
    )
    book: fields.ForeignKeyRelation[BookModel] = fields.ForeignKeyField(
        model_name="models.BookModel",
        related_name="user_books",
        on_delete="CASCADE",
    )
    get_timestamp = fields.DatetimeField(auto_now_add=True)
    back_timestamp = fields.DatetimeField(null=True)
    rating = fields.SmallIntField(null=True)

    def __str__(self) -> str:
        return str(self.id)
