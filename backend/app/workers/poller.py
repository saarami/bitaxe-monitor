
from __future__ import annotations

import asyncio
import logging

from app.core.config import settings
from app.services.telemetry_service import collect_and_store
from app.services.alert_service import decide_temperature_alerts, record_alert_event, STATUS_SENT, STATUS_SUPPRESSED, STATUS_FAILED
from app.services.telegram_service import send_message

logger = logging.getLogger(__name__)


def _format_alert_message(alert_type: str, value: float, threshold: float) -> str:
    title = "🔥 *Temperature Alert*"
    kind = "Core" if alert_type == "TEMP_CORE_HIGH" else "VR"
    return f"{title}\n{kind}: {value}°C (threshold {threshold}°C)"


async def run() -> None:
    while True:
        telemetry = await collect_and_store()

        # Do not alert if offline
        if telemetry.get("online"):
            decisions = decide_temperature_alerts(
                temp_core_c=telemetry.get("temp_core_c"),
                temp_vr_c=telemetry.get("temp_vr_c"),
                raw_snapshot=telemetry.get("raw_json") or {},
            )
            for d in decisions:
                if d.should_send:
                    try:
                        await send_message(_format_alert_message(d.type, d.value, d.threshold))
                        record_alert_event(
                            alert_type=d.type,
                            value=d.value,
                            threshold=d.threshold,
                            status=STATUS_SENT,
                            next_allowed_at=d.next_allowed_at,
                            raw_snapshot=telemetry.get("raw_json") or {},
                        )
                    except Exception as e:
                        logger.exception("Failed to send alert: %s", e)
                        record_alert_event(
                            alert_type=d.type,
                            value=d.value,
                            threshold=d.threshold,
                            status=STATUS_FAILED,
                            next_allowed_at=d.next_allowed_at,
                            raw_snapshot={"error": str(e), "telemetry": telemetry.get("raw_json")},
                        )
                else:
                    # Record suppressed decisions only if above threshold (useful audit)
                    if d.reason.startswith("Still above") or d.reason == "First alert":
                        record_alert_event(
                            alert_type=d.type,
                            value=d.value,
                            threshold=d.threshold,
                            status=STATUS_SUPPRESSED,
                            next_allowed_at=d.next_allowed_at,
                            raw_snapshot=telemetry.get("raw_json") or {},
                        )

        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(run())
