
"""SQLAlchemy models package.

Import ORM models here so Alembic can discover them via Base.metadata.
"""

from app.db.models.telemetry import Telemetry  # noqa: F401
from app.db.models.alert_event import AlertEvent  # noqa: F401
