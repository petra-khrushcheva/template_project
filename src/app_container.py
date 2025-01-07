import asyncio
import signal

from admin import AdminManager
from api import ApiManager
from api_client import ApiClientManager
from bot import BotManager
from config import Settings
from core import BaseModuleManager
from database import DatabaseManager
from scheduled_jobs import SchedulerManager
from server import ServerManager


class AppContainer:
    def __init__(self, settings: Settings):

        self.settings = settings

        self.database_manager: DatabaseManager | None = None
        self.api_client_manager: ApiClientManager | None = None
        self.admin_manager: AdminManager | None = None
        self.bot_manager: BotManager | None = None
        self.api_manager: ApiManager | None = None
        self.scheduler_manager: SchedulerManager | None = None
        self.server_manager: ServerManager | None = None

        self.modules: list[BaseModuleManager] = []

        self.stop_event = (
            asyncio.Event()
        )  # Событие для обработки сигналов SIGTERM и SIGINT

    async def setup_module(
        self, module_class: BaseModuleManager, *args, **kwargs
    ):
        """
        Создаёт экземпляр модуля, вызывает его configure,
        добавляет в список modules, и возвращает экземпляр.

        :param module_class: Класс модуля, который нужно зарегистрировать.
        :param args: Позиционные аргументы для инициализации класса.
        :param kwargs: Именованные аргументы для инициализации класса.
        :return: Инициализированный экземпляр модуля.
        """
        module: BaseModuleManager = module_class(*args, **kwargs)
        await module.configure()
        self.modules.append(module)
        return module

    async def configure(self) -> None:
        """
        Конфигурирует все модули приложения.
        """

        self.database_manager = await self.setup_module(
            DatabaseManager, self.settings.database_config
        )

        self.api_client_manager = await self.setup_module(
            ApiClientManager, self.settings.api_client_config
        )

        self.bot_manager = await self.setup_module(
            BotManager,
            bot_config=self.settings.bot_config,
            redis_config=self.settings.redis_config,
            async_session=self.database_manager.async_session,
            api_client=self.api_client_manager,
        )

        self.admin_manager = await self.setup_module(
            AdminManager,
            engine=self.database_manager.engine,
            admin_config=self.settings.admin_config,
            async_session=self.database_manager.async_session,
        )

        self.api_manager = await self.setup_module(
            ApiManager,
            api_config=self.settings.api_config,
            async_session=self.database_manager.async_session,
            api_client=self.api_client_manager,
            bot=self.bot_manager.bot,
            admin=self.admin_manager.admin,
        )

        self.scheduler_manager = await self.setup_module(
            SchedulerManager,
            bot=self.bot_manager.bot,
            async_session=self.database_manager.async_session,
            api_client=self.api_client_manager,
        )

        self.server_manager = await self.setup_module(
            ServerManager,
            app=self.api_manager.app,
            server_config=self.settings.server_config,
        )
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """
        Настраивает обработчики сигналов SIGTERM и SIGINT
        для корректного завершения приложения.
        """
        loop = asyncio.get_running_loop()

        def handle_signal():
            self.stop_event.set()

        loop.add_signal_handler(signal.SIGTERM, handle_signal)
        loop.add_signal_handler(signal.SIGINT, handle_signal)

    async def start(self) -> None:
        """
        Запускает все модули приложения.
        """
        for module in self.modules:
            await module.start()

        # Ожидаем сигнала завершения
        await self.stop_event.wait()
        await self.shutdown()

    async def shutdown(self) -> None:
        """
        Корректно завершает работу всех модулей приложения.
        """
        for module in reversed(self.modules):
            await module.shutdown()
