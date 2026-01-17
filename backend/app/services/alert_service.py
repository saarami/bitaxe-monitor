
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Optional

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models.alert_event import AlertEvent
from app.db.repositories.alert_event_repository import AlertEventRepository


ALERT_TEMP_CORE = "TEMP_CORE_HIGH"
ALERT_TEMP_VR = "TEMP_VR_HIGH"

STATUS_SENT = "SENT"
STATUS_SUPPRESSED = "SUPPRESSED"
STATUS_FAILED = "FAILED"


@dataclass(frozen=True)
class AlertDecision:
    type: str
    should_send: bool
    value: float
    threshold: float
    reason: str
    next_allowed_at: Optional[dt.datetime]


def _now() -> dt.datetime:
    return dt.datetime.utcnow()


def _cooldown_delta() -> dt.timedelta:
    return dt.timedelta(minutes=int(settings.ALERT_COOLDOWN_MINUTES))


def _hysteresis() -> float:
    return float(settings.ALERT_HYSTERESIS_C)


def _threshold_core() -> float:
    return float(settings.TEMP_THRESHOLD_CORE_C)


def _threshold_vr() -> float:
    return float(settings.TEMP_THRESHOLD_VR_C)


_repo = AlertEventRepository()


def decide_temperature_alerts(
    *,
    temp_core_c: Optional[float],
    temp_vr_c: Optional[float],
    raw_snapshot: dict,
) -> list[AlertDecision]:
    decisions: list[AlertDecision] = []
    with SessionLocal() as session:
        now = _now()
        if temp_core_c is not None:
            decisions.append(
                _decide_one(
                    session=session,
                    alert_type=ALERT_TEMP_CORE,
                    value=float(temp_core_c),
                    threshold=_threshold_core(),
                    now=now,
                )
            )
        if temp_vr_c is not None:
            decisions.append(
                _decide_one(
                    session=session,
                    alert_type=ALERT_TEMP_VR,
                    value=float(temp_vr_c),
                    threshold=_threshold_vr(),
                    now=now,
                )
            )
    return decisions


def _decide_one(
    *,
    session,
    alert_type: str,
    value: float,
    threshold: float,
    now: dt.datetime,
) -> AlertDecision:
    last = _repo.latest_by_type(session, alert_type)
    cooldown_until = now + _cooldown_delta()

    if value < threshold:
        return AlertDecision(
            type=alert_type,
            should_send=False,
            value=value,
            threshold=threshold,
            reason="Below threshold",
            next_allowed_at=None,
        )

    if last is None:
        return AlertDecision(
            type=alert_type,
            should_send=True,
            value=value,
            threshold=threshold,
            reason="First alert",
            next_allowed_at=cooldown_until,
        )

    # Locked rule: no repeats while still above threshold (until recovered below threshold-hysteresis).
    return AlertDecision(
        type=alert_type,
        should_send=False,
        value=value,
        threshold=threshold,
        reason="Still above threshold (no repeat until recovered)",
        next_allowed_at=last.next_allowed_at,
    )


def record_alert_event(
    *,
    alert_type: str,
    value: float,
    threshold: float,
    status: str,
    next_allowed_at: Optional[dt.datetime],
    raw_snapshot: dict,
) -> None:
    with SessionLocal() as session:
        event = AlertEvent(
            type=alert_type,
            value=value,
            threshold=threshold,
            status=status,
            next_allowed_at=next_allowed_at,
            raw_json=raw_snapshot,
        )
        _repo.create(session, event)
        session.commit()
