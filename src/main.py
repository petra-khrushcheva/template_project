import asyncio
import logging

from app_container import AppContainer
from config import settings
from core import configure_logging


async def main():
    configure_logging(settings.log_config)
    app_container = AppContainer(settings)
    try:
        await app_container.configure()
        await app_container.start()
    finally:
        await app_container.shutdown()
        logging.info("App successfully shut down.")


if __name__ == "__main__":
    asyncio.run(main())
