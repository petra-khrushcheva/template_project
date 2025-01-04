from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from bot.helpers import extract_media_from_message
from services import media_group_service


class MediaGroupMiddleware(BaseMiddleware):
    """
    Middleware для обработки всех сообщений с media_group_id.
    Сохраняет информацию о медиафайлах из медиагрупп в базу данных.
    """

    async def __call__(self, handler, event: Update, data: dict):
        if (
            event.message
            and isinstance(event.message, Message)
            and event.message.media_group_id
        ):
            message = event.message
            chat_id = message.chat.id
            media_group_id = message.media_group_id

            media = extract_media_from_message(message)

            db_session = data.get("db_session")
            await media_group_service.create(
                session=db_session,
                chat_id=chat_id,
                media_group_id=media_group_id,
                file_id=media["file_id"],
                media_type=media["media_type"],
            )
        return await handler(event, data)
