import logging

from fastapi import APIRouter, Depends
from schemas import UserCountStatistics
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session
from services import user_service

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/usercount", response_model=UserCountStatistics)
async def get_user_count_statistics(
    session: AsyncSession = Depends(get_session),
):
    """
    Эндпойнт для передачи количества пользователей.
    """
    try:
        user_count = await user_service.count(session=session)
        return UserCountStatistics(user_count=user_count)
    except Exception:
        logging.exception("Exception in 'get_user_count_statistics': ")
