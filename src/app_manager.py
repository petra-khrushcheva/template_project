import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Tuple

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette_admin.contrib.sqla import Admin

from admin import configure_admin
from api import router
from bot import configure_bot
from client import ApiClient, configure_client
from config import Settings, settings
from database import configure_db_session
from scheduled_tasks import start_scheduler
from utils import configure_logging


async def initialize_configuration(
    settings: Settings,
) -> Tuple[Admin, ApiClient, Bot, AsyncSession, Dispatcher]:
    """
    Инициализирует основные компоненты приложения.

    - Настраивает логирование.
    - Создает и конфигурирует клиент API.
    - Конфигурирует движок базы данных и возвращает фабрику сессий.
    - Создает и конфигурирует админку.
    - Инициализирует Telegram-бота и его диспетчер.

    :param settings: Настройки приложения.
    :return: Кортеж из:
        - admin: Объект админки.
        - api_client: Клиент для взаимодействия с API.
        - bot: Экземпляр Telegram-бота.
        - db_session: Фабрика сессий для работы с базой данных.
        - dp: Диспетчер для обработки событий Telegram.
    """
    configure_logging(settings.log_bot_token.get_secret_value())
    api_client = await configure_client(settings.base_url)
    engine, db_session = configure_db_session(settings.database_config)
    admin = configure_admin(engine, settings.secret_key)
    bot, dp = await configure_bot(
        settings.bot_token.get_secret_value(),
        settings.redis_config,
        db_session,
        api_client,
    )
    return admin, api_client, bot, db_session, dp


async def start_services(
    api_client: ApiClient, bot: Bot, dp: Dispatcher, db_session: AsyncSession
):
    """Запускает бота и шедулер."""
    scheduler = start_scheduler(bot, db_session, api_client)
    bot_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))
    return bot_task, scheduler


async def shutdown_services(bot_task, scheduler, api_client):
    """Останавливает бот, шедулер и закрывает клиент API."""
    try:
        if not bot_task.done():
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                logging.info("Bot task cancelled.")
    finally:
        scheduler.shutdown()
        logging.info("Scheduler has been shut down.")
        await api_client.close()
        logging.info("API client has been closed.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Настраивает жизненный цикл приложения FastAPI.

    - Инициализирует конфигурацию основных компонентов приложения:
      админку, клиента API, Telegram-бота, базу данных и диспетчер.
    - Запускает службы: Telegram-бота и планировщик задач.
    - Подключает админку к приложению.
    - Корректно завершает службы и
      освобождает ресурсы при остановке приложения.

    :param app: Экземпляр FastAPI-приложения.
    :yield: Управляет жизненным циклом приложения FastAPI.
    """
    try:
        logging.info("Initializing configuration...")
        admin, api_client, bot, db_session, dp = (
            await initialize_configuration(settings=settings)
        )
        bot_task, scheduler = await start_services(
            api_client, bot, dp, db_session
        )
        admin.mount_to(app)
        logging.info("Configuration initialized successfully!")
        yield
    except Exception:
        logging.exception("An error occurred during application startup.")
        raise
    finally:
        logging.info("Shutting down services...")
        await shutdown_services(bot_task, scheduler, api_client)
        logging.info("Services shut down successfully.")


def configure_app() -> FastAPI:
    """
    Конфигурирует и возвращает экземпляр FastAPI-приложения.

    - Устанавливает жизненный цикл приложения.
    - Подключает маршруты.
    - Настраивает заголовки и параметры приложения.

    :return: Настроенный экземпляр FastAPI.
    """
    app = FastAPI(lifespan=lifespan, title=settings.project_name)
    app.include_router(router)
    return app
