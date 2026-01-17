
from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.alert_event import AlertEvent


class AlertEventRepository:
    """DB access for alert events."""

    def create(self, session: Session, event: AlertEvent) -> None:
        session.add(event)

    def latest_by_type(self, session: Session, alert_type: str) -> Optional[AlertEvent]:
        return (
            session.query(AlertEvent)
            .filter(AlertEvent.type == alert_type)
            .order_by(AlertEvent.created_at.desc())
            .first()
        )
