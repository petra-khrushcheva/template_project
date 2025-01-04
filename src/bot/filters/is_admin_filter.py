from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdminFilter(BaseFilter):
    """
    Фильтр для проверки, является ли пользователь администратором.

    Параметры:
    - is_admin (bool): Флаг, передаваемый middleware, указывает статус
      пользователя в системе.

    Возвращает:
        True, если пользователь является администратором, иначе False.

    Пример:
        @router.message(IsAdminFilter())
        async def admin_handler(message: Message):
            await message.reply("Добро пожаловать, администратор!")
    """

    async def __call__(self, message: Message, is_admin: bool):
        return is_admin
