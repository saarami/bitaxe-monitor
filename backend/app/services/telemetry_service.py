
from __future__ import annotations
#from datetime import datetime, timezone
import datetime as dt
from typing import Any
import httpx
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models.telemetry import Telemetry
from app.db.repositories.telemetry_repository import TelemetryRepository
from app.services.bitaxe_client import fetch_system_info


def _now() -> dt.datetime:
    return dt.datetime.now((dt.timezone.utc))


_repo = TelemetryRepository()


async def collect_and_store() -> dict[str, Any]:
    """Fetch telemetry from Bitaxe, normalize, store, and return a normalized dict."""
    with SessionLocal() as session:
        try:
            try:
                data = await fetch_system_info()
                online = data.get("wifiStatus") == "Connected!"
                raw_json = data
            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError, httpx.HTTPError) as e:
                online = False
                raw_json = {
                    "error": "bitaxe_unreachable",
                    "exception": e.__class__.__name__,
                    "message": str(e),
                    "url": f"{settings.BITAXE_BASE_URL}/api/system/info",
                }
                data = {}

            t = Telemetry(
                timestamp=_now(),
                online=online,
                temp_core_c=data.get("temp"),
                temp_vr_c=data.get("vrTemp"),
                power_w=data.get("power"),
                fan_rpm=data.get("fanrpm"),
                frequency_mhz=data.get("frequency"),
                core_voltage_mv=data.get("coreVoltage"),
                wifi_rssi_dbm=data.get("wifiRSSI"),
                uptime_seconds=data.get("uptimeSeconds"),
                hash_rate_ghs=data.get("hashRate"),
                best_difficulty=data.get("bestDiff"),
                response_time_ms=data.get("_response_time_ms"),
                shares_accepted=data.get("sharesAccepted"),
                shares_rejected=data.get("sharesRejected"),
                raw_json=raw_json,
            )

            _repo.create(session, t)
            session.commit()

            return {
                "timestamp": t.timestamp.isoformat(),
                "online": t.online,
                "temp_core_c": t.temp_core_c,
                "temp_vr_c": t.temp_vr_c,
                "power_w": t.power_w,
                "fan_rpm": t.fan_rpm,
                "frequency_mhz": t.frequency_mhz,
                "core_voltage_mv": t.core_voltage_mv,
                "wifi_rssi_dbm": t.wifi_rssi_dbm,
                "uptime_seconds": t.uptime_seconds,
                "hash_rate_ghs": t.hash_rate_ghs,
                "best_difficulty": t.best_difficulty,
                "response_time_ms": t.response_time_ms,
                "shares_accepted": t.shares_accepted,
                "shares_rejected": t.shares_rejected,
                "raw_json": raw_json,
            }
        finally:
            session.close()


async def get_latest() -> dict:
    with SessionLocal() as session:
        row = _repo.get_latest(session)
        if row is None:
            return {"message": "No telemetry yet"}
        d = {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
        if d.get("timestamp") is not None:
            d["timestamp"] = d["timestamp"].isoformat()
        return d


async def get_last_n(n: int) -> list[dict]:
    with SessionLocal() as session:
        rows = _repo.get_last_n(session, n)
        out: list[dict] = []
        for r in rows:
            d = {k: v for k, v in r.__dict__.items() if not k.startswith("_")}
            if d.get("timestamp") is not None:
                d["timestamp"] = d["timestamp"].isoformat()
            out.append(d)
        return out

def get_thresholds_payload() -> dict:
    return {
        "temp_threshold_core_c": settings.TEMP_THRESHOLD_CORE_C,
        "temp_threshold_vr_c": settings.TEMP_THRESHOLD_VR_C,
        "alert_cooldown_minutes": settings.ALERT_COOLDOWN_MINUTES,
        "alert_hysteresis_c": settings.ALERT_HYSTERESIS_C,
    }


async def get_status_payload() -> dict:
    t = await get_latest()
    if not t or "message" in t:
        return {"has_telemetry": False}

    return {
        "has_telemetry": True,
        "online": bool(t.get("online")),
        "temp_core_c": t.get("temp_core_c"),
        "temp_vr_c": t.get("temp_vr_c"),
        "hash_rate_ghs": t.get("hash_rate_ghs"),
        "power_w": t.get("power_w"),
        "fan_rpm": t.get("fan_rpm"),
        "uptime_seconds": t.get("uptime_seconds"),
        "timestamp": t.get("timestamp"),
    }
