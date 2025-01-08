import asyncio
import logging
from functools import wraps

import typer

from config import settings
from database import DatabaseManager
from services import admin_service
from utils import hash_password

app = typer.Typer()


# декоратор для запуска асинхронных функций бд в синхронном typer
def typer_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


# Данный метод добавляет "запасную" команду в приложение Typer.
# Это связано с особенностями поведения Typer:
# если к приложению привязана только одна команда,
# Typer запускает её автоматически, даже если не была вызвана явно.
# Добавление этой "запасной" команды позволяет избежать автоматического запуска
# и корректно обрабатывать команды, переданные через CLI.
@app.command()
@typer_async
async def other_command():
    pass


@app.command()
@typer_async
async def create_admin(username: str, password: str):
    """
    Создает нового администратора с указанным именем пользователя и паролем.

    :param username: Имя пользователя администратора.
    :param password: Пароль администратора.
    """
    try:
        database_manager = DatabaseManager(
            database_config=settings.database_config
        )
        async_session = database_manager.async_session
        password = hash_password(password=password)
        async with async_session() as session:

            admin = await admin_service.create(
                session=session, username=username, password=password
            )
            print(f"New admin created: {admin.username}")
            logging.info("New admin created: {}".format(admin.username))
    except Exception:
        logging.exception("Exception in create_admin:")
    finally:
        database_manager.engine.dispose()


if __name__ == "__main__":
    app()
