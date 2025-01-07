import asyncio
import datetime
import logging
import random

from aiogram import Bot
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from services import user_service

# ограничение ТГ 30 сообщений в секунду
# + оставляем запас для текущей работы бота
MESSAGES_PER_SECOND = 25
# Задержка между сообщениями
DELAY_BETWEEN_MESSAGES = 1 / MESSAGES_PER_SECOND


async def remind_users(bot: Bot, async_session: AsyncSession):
    """
    Отправляет напоминания пользователям, которые не были активны 3 дня.

    :param bot: Экземпляр Telegram-бота.
    :param db_session: Асинхронная сессия базы данных.
    """
    timeout = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(days=3)

    async with async_session() as session:
        users = await user_service.get_bobs_for_reminder(
            session=session, timeout=timeout
        )

        if not users:
            return

        reminded_users_ids = []
        blocked_users_ids = []

        # Функция для повторной отправки сообщения
        async def send_with_retry(user_id, message):
            retry_attempts = 3
            for attempt in range(retry_attempts):
                try:
                    await bot.send_message(user_id, message)
                    return True
                except TelegramForbiddenError:
                    return False
                except TelegramBadRequest as e:
                    if "chat not found" in str(e):
                        return False
                except TelegramNetworkError:
                    # Ждем случайное время и пробуем снова
                    wait_time = random.uniform(
                        2, 5
                    )  # случайное время от 2 до 5 секунд
                    await asyncio.sleep(wait_time)
                    logging.exception(
                        "TelegramNetworkError while notification: "
                    )
                    continue
                except Exception:
                    logging.exception("Unexpected error while notification: ")
                    return False
            return False  # если все попытки не удались

        for user in users:
            success = await send_with_retry(user.tg_id, "Where are you?")
            if success:
                reminded_users_ids.append(user.tg_id)
            else:
                blocked_users_ids.append(user.tg_id)
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)

        if reminded_users_ids:
            await user_service.bulk_update(
                session=session, obj_ids=reminded_users_ids, is_reminded=True
            )

        if blocked_users_ids:
            await user_service.bulk_update(
                session=session, obj_ids=blocked_users_ids, is_active=False
            )
