import asyncio
import html
import io
import logging
import os

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile
from config import LogConfig


class TelegramHandler(logging.Handler):
    def __init__(self, log_bot_token: str, maintainers_user_ids: list[int]):
        logging.Handler.__init__(self)
        self.bot = Bot(
            token=log_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.maintainers_user_ids = maintainers_user_ids

    async def send_to_all(self, message: str):
        max_length = 4096
        for user_id in self.maintainers_user_ids:
            try:
                if len(message) > max_length:
                    file = io.BytesIO(message.encode("utf-8"))
                    input_file = BufferedInputFile(
                        file.getvalue(), "log_message.txt"
                    )

                    await self.bot.send_document(
                        chat_id=user_id,
                        document=input_file,
                    )
                    file.close()
                else:
                    await self.bot.send_message(chat_id=user_id, text=message)
            except Exception:
                # здесь нужно в случае, когда юзер (мейнтейнер) удалился делать pass
                logging.exception(
                    f"Failed to send log message to user {user_id}"
                )

    def emit(self, record):
        message = html.escape(self.format(record))
        asyncio.create_task(self.send_to_all(message))


def configure_logging(log_config: LogConfig):
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(module)-20s] [LINE:%(lineno)-3d] #%(levelname)-7s %(message)s"  # noqa
    )

    # Обработчик для записи в файл
    file_handler = logging.FileHandler(filename="logs/my_app.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Обработчик для Telegram (с уровнем WARNING)
    tg_handler = TelegramHandler(
        log_bot_token=log_config.log_bot_token.get_secret_value(),
        maintainers_user_ids=log_config.maintainers_user_ids,
    )
    tg_handler.setLevel(logging.WARNING)
    tg_handler.setFormatter(formatter)

    # (Опционально) Обработчик для вывода в консоль
    # stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.INFO)
    # stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(tg_handler)
    # logger.addHandler(stream_handler)
