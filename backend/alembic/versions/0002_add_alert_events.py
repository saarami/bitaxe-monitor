
"""add alert_events

Revision ID: 0002
Revises: 0001
Create Date: 2026-01-08T18:03:33.668674Z
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "alert_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("threshold", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("next_allowed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("raw_json", sa.JSON(), nullable=True),
    )
    op.create_index("ix_alert_events_type_created_at", "alert_events", ["type", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_alert_events_type_created_at", table_name="alert_events")
    op.drop_table("alert_events")
