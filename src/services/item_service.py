from database.repositories import item_repository
from services.base_service import BaseService


class ItemService(BaseService):
    pass


item_service = ItemService(item_repository)
