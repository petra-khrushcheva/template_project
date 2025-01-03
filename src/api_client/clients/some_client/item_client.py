from aiohttp import ClientSession

from api_client.base_client import BaseClient


class ItemClient(BaseClient):
    def __init__(self, base_url: str, session: ClientSession):
        super().__init__(base_url, session, "/items")
