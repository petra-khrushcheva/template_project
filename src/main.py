import logging

import uvicorn

from app_manager import configure_app
from config import settings


def main():
    logging.info("App is starting!")
    try:
        app = configure_app()
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            forwarded_allow_ips=settings.forwarded_allow_ips,
        )
    except (KeyboardInterrupt, SystemExit):
        logging.info("App stopped!")
    except Exception:
        logging.exception()


if __name__ == "__main__":
    main()
