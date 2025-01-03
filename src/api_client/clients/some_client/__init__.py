from aiohttp import ClientSession

from api_client.clients.some_client.item_client import ItemClient
from api_client.clients.some_client.user_client import UserClient


class SomeClient:
    def __init__(self, base_url: str, session: ClientSession):
        self.user_client = UserClient(base_url, session)
        self.item_client = ItemClient(base_url, session)
