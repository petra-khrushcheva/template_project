import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from services import user_service

router = Router()


@router.message(Command("start"))
async def start_command_handler(
    message: Message, is_admin: bool, async_session: AsyncSession
):
    """
    Обрабатывает команду /start.
    """
    try:
        await user_service.get_by_id(
            session=async_session, obj_id=message.from_user.id
        )
        # some logic
        await message.answer("Привет, чувак(есса)!")
    except Exception:
        logging.exception("Exception in start command handler: ")
