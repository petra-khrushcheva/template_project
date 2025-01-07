import logging

from sqlalchemy.ext.asyncio import async_sessionmaker

from api_client import ApiClientManager
from services import item_service


async def example_scheduler_task(
    api_client: ApiClientManager, async_session: async_sessionmaker
):
    """
    Пример задачи для планировщика.

    :param api_client: Клиент для работы с внешними API.
    :param async_session: Фабрика асинхронных сессий для работы с базой данных.
    """

    try:
        # Пример работы с базой данных
        async with async_session() as session:
            items = await item_service.list(session=session)

        # Пример работы с API-клиентом
        await api_client.some_client.item_client.bulk_create(items)

    except Exception:
        logging.exception("Exception in example scheduler job: ")
