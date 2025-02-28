import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, Integer, text
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """
    Миксин для добавления временных меток:
    - created_at: время создания записи (UTC).
    - updated_at: время последнего обновления записи (UTC).
    """

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        server_onupdate=text("TIMEZONE('utc', now())"),
    )


class IsActiveMixin:
    """Добавляет флаг is_active для soft delete."""

    is_active: Mapped[bool] = mapped_column(
        default=True, server_default="TRUE", index=True
    )


class IntPrimaryKeyMixin(TimestampMixin, IsActiveMixin):
    """Добавляет первичный ключ с типом Integer."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class BigIntPrimaryKeyMixin(TimestampMixin, IsActiveMixin):
    """Добавляет первичный ключ с типом BigInteger."""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class UUIDPrimaryKeyMixin(TimestampMixin, IsActiveMixin):
    """Добавляет первичный ключ с типом UUID."""

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
