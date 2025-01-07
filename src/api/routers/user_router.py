import logging

from aiogram import Bot
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_api_client, get_bot, get_session
from api_client import ApiClientManager
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/example/{user_id}")
async def example_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    api_client: ApiClientManager = Depends(get_api_client),
    bot: Bot = Depends(get_bot),
):
    try:
        # Используем сессию базы данных
        user = await user_service.get_by_id(session=session, obj_id=user_id)

        # Используем API-клиент
        external_user_data = (
            await api_client.some_client.user_client.get_by_id(
                item_id=user.some_api_id
            )
        )

        # Используем Telegram-бота
        await bot.send_message(chat_id=user.tg_id, text="Hello, world!")

        return {"message": "Success", "user_data": external_user_data}
    except Exception:
        logging.exception("Exception in 'example_endpoint': ")
