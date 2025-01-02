from abc import ABC, abstractmethod


class BaseModule(ABC):
    @abstractmethod
    def configure(self):
        """Настройка модуля."""
        pass

    @abstractmethod
    async def start(self):
        """Запуск модуля."""
        pass

    @abstractmethod
    async def stop(self):
        """Остановка модуля."""
        pass
