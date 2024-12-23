from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(
    url=settings.database_url,
    echo=settings.db_echo,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
)

async_session = async_sessionmaker(bind=engine)
