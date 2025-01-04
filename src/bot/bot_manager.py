import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import Redis, RedisStorage
from sqlalchemy.ext.asyncio import AsyncSession

from api_client import ApiClientManager
from bot.bot_utils import set_default_commands
from bot.middleware import (  # MediaGroupMiddleware,
    ApiClientMiddleware,
    DBSessionMiddleware,
    IsAdminMiddleware,
)
from bot.routers import router
from config import BotConfig, RedisConfig
from core import BaseModuleManager


class BotManager(BaseModuleManager):
    def __init__(
        self,
        bot_config: BotConfig,
        redis_config: RedisConfig,
        async_session: AsyncSession,
        api_client: ApiClientManager,
    ):
        self.bot_config = bot_config
        self.redis_config = redis_config
        self.async_session = async_session
        self.api_client = api_client
        self.redis: Redis | None = None

        self.bot: Bot = Bot(
            token=self.bot_config.bot_token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.dispatcher: Dispatcher = Dispatcher()
        self._polling_task: asyncio.Task | None = None

    async def configure(self):
        """
        Настройка бота и диспетчера.
        """

        await set_default_commands(bot=self.bot)

        self.redis = Redis(
            host=self.redis_config.redis_host,
            port=self.redis_config.redis_port,
            db=self.redis_config.redis_db,
        )
        storage = RedisStorage(
            redis=self.redis,
            state_ttl=self.redis_config.state_ttl,
            data_ttl=self.redis_config.data_ttl,
        )

        self.dispatcher.storage = storage
        self.dispatcher.include_router(router)

        await self.configure_middleware()

    async def configure_middleware(self):
        """
        Настройка Middleware.
        """
        self.dispatcher.update.middleware(
            DBSessionMiddleware(self.async_session)
        )
        self.dispatcher.update.middleware(ApiClientMiddleware(self.api_client))
        self.dispatcher.update.middleware(IsAdminMiddleware())
        # self.dispatcher.update.middleware(MediaGroupMiddleware())

    async def start(self):
        """
        Запуск бота.
        """
        if self.dispatcher:
            self._polling_task = await self.dispatcher.start_polling(self.bot)

    async def stop(self):
        """
        Остановка бота и диспетчера.
        """
        if self._polling_task:
            self._polling_task.cancel()
            try:
                await self._polling_task
            except asyncio.CancelledError:
                pass

        if self.bot:
            await self.bot.session.close()

        if self.redis:
            await self.redis.close()
