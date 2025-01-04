from database.repositories import admin_repository
from services.base_service import BaseService


class AdminService(BaseService):
    pass


admin_service = AdminService(admin_repository)
