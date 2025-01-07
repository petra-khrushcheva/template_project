from datetime import timezone

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import async_sessionmaker

from api_client import ApiClientManager
from scheduled_jobs.jobs import example_scheduler_task, remind_users


class SchedulerManager:
    def __init__(
        self,
        bot: Bot | None = None,
        async_session: async_sessionmaker | None = None,
        api_client: ApiClientManager | None = None,
    ):
        """
        Менеджер для управления жизненным циклом планировщика.

        :param bot: Экземпляр Telegram-бота (опционально).
        :param async_session: Фабрика сессий для работы с БД (опционально).
        :param api_client: Клиент для работы с внешними API (опционально).
        """
        self.bot = bot
        self.async_session = async_session
        self.api_client = api_client
        self.scheduler = AsyncIOScheduler()

    async def configure(self):
        """
        Настройка задач планировщика.
        """

        self.scheduler.add_job(
            remind_users,
            CronTrigger(hour=9, minute=0, timezone=timezone.utc),
            misfire_grace_time=60,
            args=[self.bot, self.async_session],
        )
        self.scheduler.add_job(
            example_scheduler_task,
            CronTrigger(minute="*/5", timezone=timezone.utc),
            misfire_grace_time=60,
            args=[self.api_client, self.async_session],
        )

    async def start(self):
        """
        Запуск планировщика.
        """
        if self.scheduler:
            self.scheduler.start()

    async def shutdown(self):
        """
        Остановка планировщика.
        """
        if self.scheduler:
            self.scheduler.shutdown(wait=False)
