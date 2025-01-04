from aiogram import BaseMiddleware


class ApiClientMiddleware(BaseMiddleware):
    def __init__(self, api_client):
        self.api_client = api_client

    async def __call__(self, handler, event, data):
        data["api_client"] = self.api_client
        return await handler(event, data)
