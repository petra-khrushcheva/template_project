import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories import user_repository
from services.base_service import BaseService


class UserService(BaseService):

    async def get_bobs_for_reminder(
        self, session: AsyncSession, timeout: datetime.datetime
    ):
        """
        Возвращает список пользователей для напоминания.

        :param session: Асинхронная сессия SQLAlchemy.
        :param timeout: Временной предел активности пользователя.
        :return: Список пользователей.
        """
        return await self.repository.get_bobs_for_reminder(
            session=session, timeout=timeout
        )


user_service = UserService(user_repository)
