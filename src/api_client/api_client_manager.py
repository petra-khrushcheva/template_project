from aiohttp import ClientSession

from api_client.clients import SomeClient, SomeOtherClient
from config import ApiClientConfig
from core import BaseModuleManager


class ApiClientManager(BaseModuleManager):
    def __init__(self, api_client_config: ApiClientConfig):
        self.some_base_url = api_client_config.some_api_url
        self.some_other_base_url = api_client_config.some_other_api_url

        self.some_client: SomeClient | None = None
        self.some_other_client: SomeOtherClient | None = None

        self.session: ClientSession | None = None

    async def configure(self):
        """
        Создаёт общую сессию и инициализирует клиенты.
        """
        self.session = ClientSession()

        self.some_client = SomeClient(self.some_base_url, self.session)
        self.payment_client = SomeOtherClient(
            self.some_other_base_url, self.session
        )

    async def start(self):
        """
        Клиенты не требуют явного запуска.
        """
        pass

    async def shutdown(self):
        """
        Закрывает сессию.
        """
        if self.session:
            await self.session.close()
