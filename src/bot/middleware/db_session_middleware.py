from aiogram import BaseMiddleware


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, async_session):
        """
        Middleware для передачи SQLAlchemy AsyncSession в хэндлеры.
        """
        super().__init__()
        self.async_session = async_session

    async def __call__(self, handler, event, data: dict):
        async with self.async_session() as session:
            data["async_session"] = session
            return await handler(event, data)
