from __future__ import annotations

import re

import httpx

from app.core.config import settings
from app.services.telemetry_service import (
    get_last_n,
    get_status_payload,
    get_thresholds_payload,
)


def _fmt_uptime(seconds: int | None) -> str:
    if not seconds:
        return "N/A"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d:
        return f"{d}d {h}h {m}m"
    if h:
        return f"{h}h {m}m"
    return f"{m}m"


async def send_message(text: str) -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
        )


async def handle_command(payload: dict) -> None:
    msg = payload.get("message") or {}
    text = (msg.get("text") or "").strip()

    # Allow only one chat ID
    chat = msg.get("chat") or {}
    chat_id = chat.get("id")
    if str(chat_id) != str(settings.TELEGRAM_CHAT_ID):
        return  # silently ignore

    if text.startswith("/status"):
        s = await get_status_payload()
        if not s.get("has_telemetry"):
            await send_message("*Status*\nNo telemetry yet.")
            return

        online = "✅ Online" if s.get("online") else "❌ Offline"
        await send_message(
            f"*Status*\n"
            f"{online}\n"
            f"*Core:* {s.get('temp_core_c')}°C\n"
            f"*VR:* {s.get('temp_vr_c')}°C\n"
            f"*Hashrate:* {s.get('hash_rate_ghs')} GH/s\n"
            f"*Power:* {s.get('power_w')} W\n"
            f"*Fan:* {s.get('fan_rpm')} RPM\n"
            f"*Uptime:* {_fmt_uptime(s.get('uptime_seconds'))}\n"
            f"*Timestamp:* {s.get('timestamp', 'N/A')}"
        )
        return

    if text.startswith("/last"):
        # Supports: /last 10 (default 10)
        m = re.match(r"^/last(?:\s+(\d+))?$", text)
        n = 10
        if m and m.group(1):
            n = max(1, min(50, int(m.group(1))))

        rows = await get_last_n(n)
        if not rows:
            await send_message("No telemetry yet.")
            return

        lines = []
        for r in rows:
            ts = r.get("timestamp", "")
            core = r.get("temp_core_c")
            vr = r.get("temp_vr_c")
            hr = r.get("hash_rate_ghs")
            ok = "OK" if r.get("online") else "OFF"
            # Keep it short per line
            lines.append(f"{ts} | Core {core}°C | VR {vr}°C | {hr} GH/s | {ok}")
        await send_message("*Last telemetry*\n" + "\n".join(lines))
        return

    if text.startswith("/thresholds"):
        th = get_thresholds_payload()
        await send_message(
            f"*Thresholds*\n"
            f"*Core:* ≥ {th['temp_threshold_core_c']}°C\n"
            f"*VR:* ≥ {th['temp_threshold_vr_c']}°C\n"
            f"*Cooldown:* {th['alert_cooldown_minutes']} min\n"
            f"*Hysteresis:* {th['alert_hysteresis_c']}°C"
        )
        return

    await send_message("Unknown command. Use /status, /last 10, or /thresholds.")
