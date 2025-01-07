from contextlib import asynccontextmanager

from aiogram import Bot
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette_admin.contrib.sqla import Admin

from api.routers import router
from api_client import ApiClientManager
from config import ApiConfig
from core import BaseModuleManager


class ApiManager(BaseModuleManager):
    def __init__(
        self,
        api_config: ApiConfig,
        async_session: async_sessionmaker | None = None,
        api_client: ApiClientManager | None = None,
        bot: Bot | None = None,
        admin: Admin | None = None,
    ):
        """
        Конструктор ApiManager.

        :param api_config: Конфигурация API (обязательно).
        :param async_session: Фабрика сессий для работы с БД (опционально).
        :param api_client: Клиент для работы с внешними API (опционально).
        :param bot: Экземпляр Telegram-бота (опционально).
        :param admin: Объект админки (опционально).
        """
        self.api_config = api_config
        self.async_session = async_session
        self.api_client = api_client
        self.bot = bot
        self.admin = admin

        self.app = FastAPI(
            title=self.api_config.project_name,
            version=self.api_config.project_version,
            lifespan=self.lifespan,
        )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """
        Lifecycle FastAPI для инициализации и завершения зависимостей.
        """
        yield {
            "async_session": self.async_session,
            "api_client": self.api_client,
            "bot": self.bot,
        }

    async def configure(self):

        self.app.include_router(router)

        if self.admin:
            self.admin.mount_to(self.app)

    async def start(self):
        # Запуск API (если есть фоновые задачи)
        pass

    async def shutdown(self):
        # Остановка API (если нужно)
        pass
