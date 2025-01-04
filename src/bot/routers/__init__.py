from aiogram import Router

from bot.routers.common_commands import router as common_commands_router
from bot.routers.error_router import router as error_router

router = Router()
router.include_router(error_router)
router.include_routers(
    common_commands_router,
)
