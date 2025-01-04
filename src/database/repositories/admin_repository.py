from database.models import Admin
from database.repositories.base_repository import BaseRepository


class AdminRepository(BaseRepository):
    pass


admin_repository = AdminRepository(Admin, primary_key="id")
