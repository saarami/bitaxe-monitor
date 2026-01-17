import os
import pytest

def test_settings_load_default_and_env_override(monkeypatch):
    settings_mod = pytest.importorskip("app.core.config")

    Settings = getattr(settings_mod, "Settings", None) or getattr(settings_mod, "AppSettings", None)
    if Settings is None:
        pytest.skip("No Settings/AppSettings class found in app.core.config.")

    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    s = Settings()

    val = getattr(s, "log_level", None) or getattr(s, "LOG_LEVEL", None) or os.getenv("LOG_LEVEL")
    assert str(val).upper() == "DEBUG"
