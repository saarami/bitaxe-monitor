
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # DB
    DATABASE_URL: str

    # Bitaxe
    BITAXE_BASE_URL: str
    POLL_INTERVAL_SECONDS: int = 60

    # Alerts
    TEMP_THRESHOLD_VR_C: float = 70
    TEMP_THRESHOLD_CORE_C: float = 70
    ALERT_COOLDOWN_MINUTES: int = 10
    ALERT_HYSTERESIS_C: float = 2

    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_WEBHOOK_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
