from fastapi import APIRouter

from api.routers.user_count_router import router as user_count_router
from api.routers.user_router import router as user_router

router = APIRouter(prefix="/api")
router.include_router(user_router)
router.include_router(user_count_router)
