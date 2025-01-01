from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin, ModelView

from admin.auth import UsernameAndPasswordProvider
from admin.views import PKModelView
from config import Settings

# from database.models import Admin as AdminModel
from database.models import Item, User


class AdminManager:
    def __init__(
        self,
        engine: AsyncEngine,
        async_session: async_sessionmaker,
        settings: Settings,
    ):
        """
        Конструктор принимает базовые зависимости:
        - engine: асинхронный SQLAlchemy движок для работы с базой данных.
        - secret_key: секретный ключ для сессий.
        """
        self.settings = settings
        self.engine = engine
        self.async_session = async_session
        self.admin = None

    async def initialize(self):
        """
        Инициализация админки:
        - Настройка базовых параметров (название, URL).
        - Подключение аутентификации.
        - Настройка middleware.
        - Регистрация моделей (User, Item).
        """
        self.admin = Admin(
            engine=self.engine,
            title=self.settings.project_name,
            base_url="/admin",
            auth_provider=UsernameAndPasswordProvider(self.async_session),
            middlewares=[
                Middleware(
                    SessionMiddleware, secret_key=self.settings.secret_key
                )
            ],
            i18n_config=I18nConfig(default_locale="ru"),
        )

        await self.setup_views()

    async def setup_views(self):
        self.admin.add_view(PKModelView(User, label="Пользователи"))
        self.admin.add_view(ModelView(Item, label="Штуки"))
