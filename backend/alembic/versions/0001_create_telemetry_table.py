
"""create telemetry table

Revision ID: 0001
Revises:
Create Date: 2026-01-08

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "telemetry",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("online", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("temp_core_c", sa.Float(), nullable=True),
        sa.Column("temp_vr_c", sa.Float(), nullable=True),
        sa.Column("power_w", sa.Float(), nullable=True),
        sa.Column("fan_rpm", sa.Integer(), nullable=True),
        sa.Column("frequency_mhz", sa.Integer(), nullable=True),
        sa.Column("core_voltage_mv", sa.Integer(), nullable=True),
        sa.Column("wifi_rssi_dbm", sa.Integer(), nullable=True),
        sa.Column("uptime_seconds", sa.Integer(), nullable=True),
        sa.Column("hash_rate_ghs", sa.Float(), nullable=True),
        sa.Column("best_difficulty", sa.Float(), nullable=True),
        sa.Column("response_time_ms", sa.Float(), nullable=True),
        sa.Column("shares_accepted", sa.Integer(), nullable=True),
        sa.Column("shares_rejected", sa.Integer(), nullable=True),
        sa.Column("raw_json", sa.JSON(), nullable=True),
    )
    op.create_index("ix_telemetry_timestamp", "telemetry", ["timestamp"])

def downgrade() -> None:
    op.drop_index("ix_telemetry_timestamp", table_name="telemetry")
    op.drop_table("telemetry")
