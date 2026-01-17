
from fastapi import APIRouter
from app.services.telemetry_service import get_latest, get_last_n, get_status_payload, get_thresholds_payload

router = APIRouter()

@router.get("/telemetry/latest")
async def latest():
    return await get_latest()

@router.get("/telemetry/last/{n}")
async def last_n(n: int):
    return await get_last_n(n)


@router.get("/telemetry/status")
async def telemetry_status():
    return await get_status_payload()

@router.get("/telemetry/thresholds")
def telemetry_thresholds():
    return get_thresholds_payload()
