from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
    """
    Фильтр для проверки типа чата, из которого пришло сообщение.

    Параметры:
    - chat_type (str): Ожидаемый тип чата. Возможные значения:
        - "private": Личный чат.
        - "group": Групповой чат.
        - "supergroup": Супергруппа.
        - "channel": Канал.

    Возвращает:
        True, если тип чата совпадает с указанным в фильтре, иначе False.

    Пример использования:
        @router.message(ChatTypeFilter(chat_type="private"))
        async def private_chat_handler(message: Message):
            await message.reply("Это сообщение только для личного чата.")
    """

    def __init__(self, chat_type: str):
        self.chat_type = chat_type

    async def __call__(self, message: Message, chat_type: str):
        return chat_type == self.chat_type
