from aiohttp import ClientSession

from api_client.base_client import BaseClient


class SomeOtherClient(BaseClient):
    def __init__(self, base_url: str, session: ClientSession):
        super().__init__(base_url, session, "/some_route")

    async def specific_request(self, some_data: dict):
        return await self.request("POST", "/specific_endpoint", json=some_data)
