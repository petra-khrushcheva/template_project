from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin, ModelView

from admin.auth import UsernameAndPasswordProvider
from admin.views import PKModelView
from config import settings
from database.db_config import engine

# from database.models import Admin as AdminModel
from database.models import Post, User

admin = Admin(
    engine,
    title="Базовый проект",
    base_url="/admin",
    auth_provider=UsernameAndPasswordProvider(),
    middlewares=[
        Middleware(SessionMiddleware, secret_key=settings.secret_key)
    ],
    i18n_config=I18nConfig(default_locale="ru"),
)


admin.add_view(PKModelView(User, label="Пользователи"))
admin.add_view(ModelView(Post, label="Посты"))
