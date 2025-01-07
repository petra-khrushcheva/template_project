class RepositoryError(Exception):
    """Базовое исключение для ошибок в репозиториях."""


class ServiceError(Exception):
    """Базовое исключение для ошибок на уровне сервиса."""


class NotFoundError(ServiceError):
    """Выбрасывается, если объект не найден."""
