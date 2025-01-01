from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from config import DatabaseConfig


def configure_db_session(
    config: DatabaseConfig,
) -> tuple[AsyncEngine, async_sessionmaker]:
    """Конфигурирует и возвращает движок базы данных и фабрику сессий."""
    engine = create_async_engine(config.database_url, echo=config.db_echo)

    session = async_sessionmaker(bind=engine)
    return engine, session
