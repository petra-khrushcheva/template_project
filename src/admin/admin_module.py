from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin, ModelView

from admin.auth import UsernameAndPasswordProvider
from admin.views import PKModelView
from config import AdminConfig
from core import BaseModule

# from database.models import Admin as AdminModel
from database.models import Item, User


class AdminModule(BaseModule):
    def __init__(
        self,
        engine: AsyncEngine,
        admin_config: AdminConfig,
        async_session: async_sessionmaker,
    ):
        """
        Конструктор принимает базовые зависимости:
        - engine: асинхронный SQLAlchemy движок для работы с базой данных.
        - admin_config: конфигурация админки.
        """
        self.admin_config = admin_config
        self.async_session = async_session
        self.admin = Admin(engine)

    async def configure(self):
        """
        Инициализация админки:
        - Настройка базовых параметров (название, URL).
        - Подключение аутентификации.
        - Настройка middleware.
        - Регистрация моделей (User, Item).
        """

        self.admin.title = self.admin_config.project_name
        self.admin.base_url = "/admin"
        self.admin.auth_provider = UsernameAndPasswordProvider(
            self.async_session
        )

        self.admin.middlewares = [
            Middleware(
                SessionMiddleware, secret_key=self.admin_config.secret_key
            )
        ]
        self.admin.i18n_config = I18nConfig(default_locale="ru")

        self.setup_views()

    def setup_views(self):
        self.admin.add_view(PKModelView(User, label="Пользователи"))
        self.admin.add_view(ModelView(Item, label="Штуки"))

    async def start(self):
        """Админка не требует запуска."""
        pass

    async def stop(self):
        """Админка не требует остановки."""
        pass
