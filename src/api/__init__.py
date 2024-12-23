from fastapi import APIRouter

from api.user_count_router import router as user_count_router

router = APIRouter(prefix="/api")
router.include_router(user_count_router)
