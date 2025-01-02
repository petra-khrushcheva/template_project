from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from config import DatabaseConfig
from core import BaseModuleManager


class DatabaseManager(BaseModuleManager):
    """
    Менеджер базы данных.

    Отвечает за управление подключением к базе данных, настройку движка,
    создание сессий и завершение работы.
    """

    def __init__(self, database_config: DatabaseConfig):
        """
        Инициализирует движок базы данных и фабрику асинхронных сессий.

        :param database_config: Конфигурация базы данных.
        """
        self.engine: AsyncEngine = create_async_engine(
            url=database_config.database_url,
            echo=database_config.echo,
            pool_size=database_config.pool_size,
            max_overflow=database_config.max_overflow,
        )
        self.async_session: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        )

    async def stop(self):
        """
        Закрывает соединения с базой данных.
        """
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Предоставляет асинхронную сессию для работы с базой данных.

        :yield: Экземпляр асинхронной сессии.
        """
        async with self.async_session() as session:
            yield session

    async def start(self):
        """DatabaseManager не требует операций на этапе старта."""
        pass

    async def configure(self):
        """DatabaseManager не требует конфигурации."""
        pass
