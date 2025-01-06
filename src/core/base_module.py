from abc import ABC, abstractmethod


class BaseModuleManager(ABC):
    @abstractmethod
    async def configure(self):
        """Настройка модуля."""
        pass

    @abstractmethod
    async def start(self):
        """Запуск модуля."""
        pass

    @abstractmethod
    async def shutdown(self):
        """Остановка модуля."""
        pass
