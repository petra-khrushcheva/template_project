import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    async def get_bobs_for_reminder(
        self, session: AsyncSession, timeout: datetime.datetime
    ):
        """
        Возвращает пользователей, которым нужно отправить напоминание.

        :param session: Асинхронная сессия SQLAlchemy.
        :param timeout: Временной предел активности пользователя.
        :return: Список пользователей.
        """
        query = select(User).filter(
            and_(
                User.first_name == "Bob",
                User.last_active < timeout,
            )
        )
        results = await session.execute(query)
        return results.scalars().all()


user_repository = UserRepository(User, primary_key="id")
