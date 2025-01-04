from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.base_repository import BaseRepository
from utils import NotFoundError, handle_service_errors


class BaseService:
    def __init__(self, repository: BaseRepository):
        """
        Базовый сервис для работы с репозиториями.
        :param repository: Экземпляр репозитория для работы с данными.
        """
        self.repository = repository

    @handle_service_errors("creating item")
    async def create(self, session: AsyncSession, **fields):
        """
        Создание нового объекта.
        :param session: Асинхронная сессия SQLAlchemy.
        :param fields: Поля для создания нового объекта.
        :return: Созданный объект.
        """
        return await self.repository.create(session, **fields)

    @handle_service_errors("listing items")
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
        return await self.repository.list(
            session, include_inactive=include_inactive, **fields
        )

    @handle_service_errors("retrieving item")
    async def get(
        self, session: AsyncSession, include_inactive: bool = False, **fields
    ):
        """
        Получение одного объекта по заданным критериям.
        :param session: Асинхронная сессия SQLAlchemy.
        :param include_inactive: Включать ли неактивные объекты.
        :param fields: Поля для фильтрации (например, id=1, name="example").
        :return: Объект, соответствующий критериям.
        :raises NotFoundError: Если объект не найден.
        """
        result = await self.repository.get(
            session, include_inactive=include_inactive, **fields
        )
        if not result:
            raise NotFoundError("Item not found")
        return result

    @handle_service_errors("retrieving item or returning None")
    async def get_or_none(
        self, session: AsyncSession, include_inactive: bool = False, **fields
    ):
        """
        Получение одного объекта по заданным критериям или None,
        если объект не найден.
        :param session: Асинхронная сессия SQLAlchemy.
        :param include_inactive: Включать ли неактивные объекты.
        :param fields: Поля для фильтрации (например, id=1, name="example").
        :return: Объект, соответствующий критериям, или None.
        """
        try:
            return await self.get(
                session=session, include_inactive=include_inactive, **fields
            )
        except NotFoundError:
            return None

    @handle_service_errors("retrieving item by ID")
    async def get_by_id(
        self,
        session: AsyncSession,
        obj_id: int,
        include_inactive: bool = False,
    ):
        """
        Получение объекта по его ID.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        :param include_inactive: Включать ли неактивные объекты.
        :return: Найденный объект.
        :raises NotFoundError: Если объект с указанным ID не найден.
        """
        result = await self.repository.get_by_id(
            session, obj_id, include_inactive=include_inactive
        )
        if not result:
            raise NotFoundError("Item not found")
        return result

    @handle_service_errors("updating item")
    async def update(
        self,
        session: AsyncSession,
        obj_id,
        include_inactive: bool = False,
        **fields,
    ):
        """
        Обновление объекта по его ID.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        :param fields: Поля для обновления объекта.
        :raises NotFoundError: Если объект с указанным ID не найден.
        """
        obj = await self.repository.get_by_id(
            session, obj_id, include_inactive=include_inactive
        )
        if not obj:
            raise NotFoundError("Object not found")
        await self.repository.update(session, obj_id, **fields)

    @handle_service_errors("deleting item")
    async def delete(self, session: AsyncSession, obj_id):
        """
        Удаление объекта по его ID.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        :raises NotFoundError: Если объект не найден или уже удален.
        """
        obj = await self.repository.get_by_id(
            session, obj_id, include_inactive=True
        )
        if not obj:
            raise NotFoundError("Object not found or already deleted")
        await self.repository.delete(session, obj_id)

    @handle_service_errors("getting or creating item")
    async def get_or_create(self, session: AsyncSession, **fields):
        """
        Получение объекта по заданным критериям или его создание.
        :param session: Асинхронная сессия SQLAlchemy.
        :param fields: Поля для поиска объекта.
         Если объект не найден, он будет создан с этими полями.
        :return: Найденный или созданный объект.
        """
        return await self.repository.get_or_create(session, **fields)

    @handle_service_errors("bulk creating items")
    async def bulk_create(self, session: AsyncSession, items_data: List[dict]):
        """
        Массовое создание объектов.
        :param session: Асинхронная сессия SQLAlchemy.
        :param items_data: Список словарей с данными для создания объектов.
        :return: None
        """
        return await self.repository.bulk_create(session, items_data)

    @handle_service_errors("deactivating item")
    async def soft_delete(self, session: AsyncSession, obj_id: int):
        """
        Деактивация объекта (soft delete) по его ID.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        :raises NotFoundError: Если объект не найден или уже деактивирован.
        """
        obj = await self.repository.get_by_id(
            session, obj_id, include_inactive=True
        )
        if not obj or not obj.is_active:
            raise NotFoundError("Object not found or already deleted")
        await self.repository.soft_delete(session, obj_id)

    @handle_service_errors("bulk updating items")
    async def bulk_update(
        self, session: AsyncSession, obj_ids: List, **fields
    ):
        """
        Массовое обновление объектов по списку идентификаторов.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_ids: Список ID объектов, которые нужно обновить.
        :param fields: Поля для обновления.
        :raises ValueError: Если список идентификаторов пуст.
        """
        if not obj_ids:
            raise ValueError("List of IDs for bulk update cannot be empty")
        await self.repository.bulk_update(session, obj_ids, **fields)

    @handle_service_errors("creating or updating item by ID")
    async def create_or_update_by_id(
        self, session: AsyncSession, obj_id: int, **fields
    ):
        """
        Создание или обновление объекта по ID.
        :param session: Асинхронная сессия SQLAlchemy.
        :param obj_id: Идентификатор объекта.
        :param fields: Поля для создания или обновления объекта.
        :return: Экземпляр объекта.
        """
        try:
            await self.get_by_id(
                session=session,
                obj_id=obj_id,
                include_inactive=True,
            )
            return await self.repository.update(session, obj_id, **fields)
        except NotFoundError:
            fields[self.repository.primary_key] = obj_id
            return await self.repository.create(session, **fields)

    @handle_service_errors("counting objects")
    async def count(
        self, session: AsyncSession, include_inactive: bool = False, **filters
    ):
        """
        Подсчет количества объектов в базе данных через репозиторий.
        :param session: Асинхронная сессия SQLAlchemy.
        :param include_inactive: Включать ли неактивные объекты в подсчет.
        :param filters: Поля для фильтрации.
        :return: Количество объектов, соответствующих фильтрам.
        """
        return await self.repository.count(
            session, include_inactive, **filters
        )
