import asyncio

import uvicorn

from config import ServerConfig


class ServerManager:
    def __init__(self, app, server_config: ServerConfig):
        """
        Менеджер для управления жизненным циклом Uvicorn сервера.

        :param app: FastAPI-приложение или любой ASGI-совместимый объект.
        """
        self.app = app
        self.server_config = server_config
        self.server = uvicorn.Server(
            uvicorn.Config(
                app=self.app,
                host=self.server_config.host,
                port=self.server_config.port,
                forwarded_allow_ips=self.server_config.forwarded_allow_ips,
                handle_signals=False,
            )
        )
        self.server_task: asyncio.Task | None = None

    async def configure(self):
        """
        Настройка сервера (в данном случае ничего не требуется).
        """
        pass

    async def start(self):
        """
        Запуск Uvicorn сервера.
        """
        self.server_task = asyncio.create_task(self.server.serve())

    async def shutdown(self):
        """
        Корректное завершение работы Uvicorn сервера.
        """
        if self.server_task:
            self.server.should_exit = True
            await self.server_task
            self.server_task = None
