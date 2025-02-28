from aiogram import BaseMiddleware
from aiogram.types import Chat, Update


class ChatTypeMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        """
        Middleware для определения типа чата.
        Например: "private", "group", "supergroup", "channel".
        """
        update: Update = event

        if update.message:
            chat: Chat = update.message.chat
            data["chat_type"] = chat.type

        return await handler(event, data)
