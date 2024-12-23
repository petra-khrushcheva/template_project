from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin, ModelView

from admin.auth import UsernameAndPasswordProvider
from admin.views import PKModelView

# from database.models import Admin as AdminModel
from database.models import Item, User


def configure_admin(engine: AsyncEngine, secret_key: str) -> Admin:
    """
    Конфигурирует админку приложения.

    :param engine: Движок базы данных
    :param settings: Настройки приложения
    :return: Объект админки
    """
    admin = Admin(
        engine,
        title="Базовый проект",
        base_url="/admin",
        auth_provider=UsernameAndPasswordProvider(),
        middlewares=[Middleware(SessionMiddleware, secret_key=secret_key)],
        i18n_config=I18nConfig(default_locale="ru"),
    )

    # Добавляем представления моделей
    admin.add_view(PKModelView(User, label="Пользователи"))
    admin.add_view(ModelView(Item, label="Штуки"))

    return admin
