
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, JSON
from app.db.base import Base
import datetime

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    online = Column(Boolean, default=True)

    temp_core_c = Column(Float)
    temp_vr_c = Column(Float)
    power_w = Column(Float)
    fan_rpm = Column(Integer)
    frequency_mhz = Column(Integer)
    core_voltage_mv = Column(Integer)
    wifi_rssi_dbm = Column(Integer)
    uptime_seconds = Column(Integer)

    hash_rate_ghs = Column(Float)
    best_difficulty = Column(Float)
    response_time_ms = Column(Float)
    shares_accepted = Column(Integer)
    shares_rejected = Column(Integer)

    raw_json = Column(JSON)
