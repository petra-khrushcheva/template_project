import logging
from functools import wraps

from utils.exceptions import NotFoundError, RepositoryError, ServiceError


def handle_service_errors(action: str):
    """
    Декоратор для обработки ошибок в сервисах.
    :param action: описание действия (например, "creating item").
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except NotFoundError:
                raise
            except RepositoryError as e:
                logging.exception(f"Repository error during {action}")
                raise ServiceError(f"An error occurred during {action}") from e
            except Exception as e:
                logging.exception(f"Unexpected error during {action}")
                raise ServiceError(
                    f"An unexpected error occurred during {action}"
                ) from e

        return wrapper

    return decorator
