from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

from services import admin_service


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        """
        Проверяет, есть ли пользователь в таблице администраторов,
        и добавляет эту информацию в data.
        """
        update: Update = event

        if update.message:
            username = update.message.from_user.username

            if not username:
                data["is_admin"] = False
                return await handler(event, data)

            db_session: AsyncSession = data.get("db_session")

            data["is_admin"] = bool(
                await admin_service.get_or_none(
                    session=db_session, username=username
                )
            )

        return await handler(event, data)
