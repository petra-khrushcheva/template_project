import asyncio
import logging

from aiogram import Router
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramNetworkError,
    TelegramRetryAfter,
)
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

router = Router()


# Хэндлер для ошибки RetryAfter (слишком частые запросы)
@router.error(ExceptionTypeFilter(TelegramRetryAfter))
async def handle_retry_after(event: ErrorEvent):
    exception: TelegramRetryAfter = event.exception
    retry_after = exception.retry_after
    logging.warning(f"Перегрузка, повторите через {retry_after} секунд.")
    await asyncio.sleep(retry_after)
    return True


# Хэндлер для ошибки NetworkError (проблема с сетью)
@router.error(ExceptionTypeFilter(TelegramNetworkError))
async def handle_network_error(event: ErrorEvent):
    logging.warning("Сетевая ошибка. Переподключение...")
    return True


# Хэндлер для общей ошибки TelegramAPIError
@router.error(ExceptionTypeFilter(TelegramAPIError))
async def handle_telegram_api_error(event: ErrorEvent):
    exception = event.exception
    logging.exception(f"Telegram API Error: {exception}")
    return True


# Хэндлер для любых других непредусмотренных ошибок
@router.error()
async def handle_other_exceptions(event: ErrorEvent):
    exception = event.exception
    logging.exception(f"Необработанная ошибка: {exception}")
    return True


# # Хэндлер для ошибки Unauthorized (бот заблокирован пользователем)
# @router.errors_handler(ExceptionTypeFilter(TelegramForbiddenError))
# async def handle_unauthorized(
#     event: ErrorEvent, message: Message
# ):
#     logging.info(
#         f"Бот заблокирован пользователем {update.message.from_user.id}."
#     )
#     return True
