from typing import AsyncGenerator

from aiogram import Bot
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from api_client import ApiClientManager


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения асинхронной сессии базы данных.
    """
    async_session = request.state.async_session
    if not async_session:
        raise ValueError("Database session factory is not configured.")

    async with async_session() as session:
        yield session


async def get_api_client(request: Request) -> ApiClientManager:
    """
    Зависимость для получения клиента API.
    """
    api_client = request.state.api_client
    if not api_client:
        raise ValueError("API client is not configured.")
    return api_client


async def get_bot(request: Request) -> Bot:
    """
    Зависимость для получения экземпляра Telegram-бота.
    """
    bot = request.state.bot
    if not bot:
        raise ValueError("Telegram bot is not configured.")
    return bot
