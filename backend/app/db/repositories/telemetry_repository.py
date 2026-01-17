
from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.db.models.telemetry import Telemetry


class TelemetryRepository:
    """DB access for telemetry."""

    def create(self, session: Session, telemetry: Telemetry) -> None:
        session.add(telemetry)

    def get_latest(self, session: Session) -> Optional[Telemetry]:
        return session.query(Telemetry).order_by(Telemetry.timestamp.desc()).first()

    def get_last_n(self, session: Session, n: int) -> Sequence[Telemetry]:
        return (
            session.query(Telemetry)
            .order_by(Telemetry.timestamp.desc())
            .limit(n)
            .all()
        )
