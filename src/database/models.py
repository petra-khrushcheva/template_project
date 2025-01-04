import enum

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.basemodels import Base
from database.mixins import (
    BigIntPrimaryKeyMixin,
    IntPrimaryKeyMixin,
    LastActiveMixin,
)


class User(BigIntPrimaryKeyMixin, LastActiveMixin, Base):
    """
    Пользователи, взаимодействующие с функционалом бота
    в личных сообщениях или в группах.

    Поля класса:
    - `id`: Уникальный идентификатор юзера.
    - `last_active` дата последней активности.
    - `is_active`используется для soft delete.
    - `items` список штук, которые принадлежат пользователю.

    """

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    some_bool_val: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="FALSE"
    )

    items: Mapped[list["Item"]] = relationship(back_populates="user")


class ItemType(str, enum.Enum):

    option_1 = "option_1"
    option_2 = "option_2"


class Item(IntPrimaryKeyMixin, Base):
    """
    Штуки.

    Поля класса:
    - `id`: Уникальный идентификатор штуки.
    - `title`: Название штуки.
    - `type`: Тип штуки.
    - `user_id`: ID пользователя, которому принадлежит штука.
    - `is_active`используется для soft delete.
    """

    __tablename__ = "items"

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    item_type: Mapped[ItemType] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="items")


class Admin(IntPrimaryKeyMixin, Base):
    """
    Таблица для хранения администраторов, имеющих доступ к админ-панели.
    """

    __tablename__ = "admins"

    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str]
