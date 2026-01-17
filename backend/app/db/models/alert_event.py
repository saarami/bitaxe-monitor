
from __future__ import annotations

import datetime as dt
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Index

from app.db.base import Base


class AlertEvent(Base):
    """Stores alert decisions for auditing and cooldown enforcement."""

    __tablename__ = "alert_events"

    id = Column(Integer, primary_key=True)

    # Single-miner v1: no miner_id FK yet. Can be added in V2 if needed.
    type = Column(String(32), nullable=False)  # TEMP_CORE_HIGH / TEMP_VR_HIGH
    value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)

    status = Column(String(16), nullable=False)  # SENT / SUPPRESSED / FAILED
    next_allowed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    raw_json = Column(JSON, nullable=True)


Index("ix_alert_events_type_created_at", AlertEvent.type, AlertEvent.created_at.desc())
