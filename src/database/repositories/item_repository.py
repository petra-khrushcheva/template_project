from database.models import Item
from database.repositories.base_repository import BaseRepository


class ItemRepository(BaseRepository):
    pass


item_repository = ItemRepository(Item, primary_key="id")
