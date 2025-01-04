import logging
from contextlib import asynccontextmanager
from typing import List

from sqlalchemy import delete, func, inspect, select, update
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
    TimeoutError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from utils import RepositoryError


class BaseRepository:
    def __init__(self, table, primary_key: str = None):
        """
        Базовый репозиторий для работы с таблицами через SQLAlchemy.
        :param table: SQLAlchemy модель, представляющая таблицу.
        :param primary_key: Имя первичного ключа таблицы. Если не указано,
         определяется автоматически.
        """
        self.table = table
        if primary_key is None:
            self.primary_key = self._get_primary_key_name()
        else:
            self.primary_key = primary_key

    def _get_primary_key_name(self) -> str:
        """
        Автоматически определяет имя первичного ключа модели.
        :return: Имя первичного ключа.
        """
        mapper = inspect(self.table)
        return mapper.primary_key[0].name

    @asynccontextmanager
    async def _handle_errors(self, action: str):
        """
        Универсальный обработчик ошибок SQLAlchemy.
        :param action: описание действия (например, "создание объекта").
        """
        try:
            yield
        except IntegrityError as e:
            logging.exception(f"Integrity error during {action}")
            raise RepositoryError(
                f"Integrity error during {action}: {e}"
            ) from e
        except OperationalError as e:
            logging.exception(f"Operational error during {action}")
            raise RepositoryError(
                f"Operational error during {action}: {e}"
            ) from e
        except TimeoutError as e:
            logging.exception(f"Timeout error during {action}")
            raise RepositoryError(f"Timeout error during {action}: {e}") from e
        except DataError as e:
            logging.exception(f"Data error during {action}")
            raise RepositoryError(f"Data error during {action}: {e}") from e
        except SQLAlchemyError as e:
            logging.exception(f"Unexpected database error during {action}")
            raise RepositoryError(
                f"Unexpected database error during {action}: {e}"
            ) from e

    async def create(self, session: AsyncSession, **fields):
        """
        Создание нового объекта.
        :param session: Асинхронная сессия SQLAlchemy.
        :param fields: Поля для создания нового объекта.
        :return: Созданный объект.
        """
        async with self._handle_errors("creating an object"):
            new_obj = self.table(**fields)
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
            return new_obj

    async def list(
        self, session: AsyncSession, include_inactive: bool = False, **fields
    ):
        """
        Получение списка объектов.
        :param session: Асинхронная сессия SQLAlchemy.
        :param include_inactive: Включать ли неактивные объекты.
        :param fields: Поля для фильтрации (например, name="example").
        :return: Список объектов, соответствующих критериям.
        """
        async with self._handle_errors("listing objects"):
            query = select(self.table).filter_by(**fields)
            if not include_inactive and hasattr(self.table, "is_active"):
                query = query.filter_by(is_active=True)
            results = await session.execute(query)
            return results.scalars().all()

    async def get(
        self, session: AsyncSession, include_inactive: bool = False, **fields
    ):
        """
        Получение одного объекта по заданным критериям.
        :param session: Асинхронная сессия SQLAlchemy.
        :param include_inactive: Включать ли неактивные объекты.
        :param fields: Поля для фильтрации (например, id=1, name="example").
        :return: Объект или None, если не найден.
        """
        async with self._handle_errors("getting an object"):
            query = select(self.table).filter_by(**fields)
            if not include_inactive and hasattr(self.table, "is_active"):
                query = query.filter_by(is_active=True)
            result = await session.execute(query)
            return result.scalars().first()

    async def get_by_id(
        self, session: AsyncSession, obj_id, include_inactive: bool = False
    ):
        """
        Получение объекта по его ID.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        :param include_inactive: Включать ли неактивные объекты.
        :return: Объект или None, если не найден.
        """

        async with self._handle_errors("getting an object by ID"):
            query = select(self.table).filter_by(id=obj_id)
            if not include_inactive and hasattr(self.table, "is_active"):
                query = query.filter_by(is_active=True)
            results = await session.execute(query)
            return results.scalars().first()

    async def update(self, session: AsyncSession, obj_id, **fields):
        """
        Обновление объекта по его ID.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        :param fields: Поля для обновления.
        """
        async with self._handle_errors("updating an object"):
            await session.execute(
                update(self.table)
                .filter(getattr(self.table, self.primary_key) == obj_id)
                .values(**fields)
            )
            await session.commit()
            return await self.get_by_id(session, obj_id, include_inactive=True)

    async def delete(self, session: AsyncSession, obj_id):
        """
        Удаление объекта по его ID из базы данных.

        Обратите внимание:
        - Этот метод полностью удаляет объект из базы данных.
        - Если вы хотите сохранить объект, но пометить его как "удаленный",
          рассмотрите использование метода `soft_delete`.

        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        """
        async with self._handle_errors("deleting an object"):
            await session.execute(
                delete(self.table).filter_by(**{self.primary_key: obj_id})
            )
            await session.commit()

    async def get_or_create(self, session: AsyncSession, **fields):
        """
        Получение объекта по критериям или его создание, если он не найден.
        :param session: Асинхронная сессия SQLAlchemy.
        :param fields: Поля для поиска и создания объекта.
        :return: Найденный или созданный объект.
        """
        async with self._handle_errors("getting or creating an object"):
            pk_value = fields.get(self.primary_key)
            if pk_value is not None:
                instance = await self.get_by_id(session, pk_value)
                if instance:
                    return instance
            instance = await self.get(session, **fields)
            if instance:
                return instance
            instance = await self.create(session, **fields)
            return instance

    async def bulk_create(self, session: AsyncSession, items_data: List[dict]):
        """
        Массовое создание объектов.
        :param session: Асинхронная сессия SQLAlchemy.
        :param items_data: Список словарей с данными для создания объектов.
        """
        async with self._handle_errors("bulk creating objects"):
            new_objs = [self.table(**data) for data in items_data]
            session.add_all(new_objs)
            await session.commit()

    async def soft_delete(self, session: AsyncSession, obj_id: int):
        """
        Деактивация объекта по его ID (soft delete).
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        """
        async with self._handle_errors("soft deleting an object"):
            await session.execute(
                update(self.table)
                .filter_by(**{self.primary_key: obj_id})
                .values(is_active=False)
            )
            await session.commit()

    async def bulk_update(
        self, session: AsyncSession, obj_ids: List, **fields
    ):
        """
        Массовое обновление объектов по списку идентификаторов.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_ids: Список id объектов, которые нужно обновить.
        :param fields: Поля для обновления (общие для всех объектов).
        """
        async with self._handle_errors("bulk updating objects"):
            await session.execute(
                update(self.table)
                .where(getattr(self.table, self.primary_key).in_(obj_ids))
                .values(**fields)
            )
            await session.commit()

    async def count(
        self, session: AsyncSession, include_inactive: bool = False, **fields
    ) -> int:
        """
        Подсчет количества объектов, соответствующих заданным фильтрам.
        :param session: Асинхронная сессия SQLAlchemy.
        :param include_inactive: Включать ли неактивные объекты в подсчет.
        :param fields: Поля для фильтрации (например, name="example").
        :return: Количество объектов, соответствующих критериям.
        """
        async with self._handle_errors("counting objects"):
            query = select(func.count(self.table.id)).filter_by(**fields)

            if not include_inactive and hasattr(self.table, "is_active"):
                query = query.filter_by(is_active=True)

            result = await session.execute(query)
            return result.scalar()
