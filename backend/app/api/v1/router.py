
from fastapi import APIRouter
from app.api.v1.endpoints import health, telemetry, telegram

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(telemetry.router, tags=["telemetry"])
router.include_router(telegram.router, tags=["telegram"])
