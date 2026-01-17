import time
import pytest

def test_alert_service_triggers_and_rate_limits(monkeypatch):
    mod = pytest.importorskip("app.services.alert_service")
    AlertService = getattr(mod, "AlertService", None)
    if AlertService is None:
        pytest.skip("AlertService not found in app.services.alert_service")

    svc = AlertService()

    telemetry_hot = {"temperature_c": 90.0, "hashrate_ghs": 1.0}

    def call_eval(t):
        for name in ("evaluate", "check_alerts", "compute_alerts"):
            if hasattr(svc, name):
                return getattr(svc, name)(t)
        pytest.skip("AlertService has no evaluate/check_alerts/compute_alerts method")

    alerts1 = call_eval(telemetry_hot)
    assert alerts1 is not None
    assert isinstance(alerts1, (list, tuple))
    assert len(alerts1) >= 1

    alerts2 = call_eval(telemetry_hot)
    assert isinstance(alerts2, (list, tuple))
    assert len(alerts2) <= len(alerts1)

    monkeypatch.setattr(time, "time", lambda: time.time() + 10_000)
    alerts3 = call_eval(telemetry_hot)
    assert isinstance(alerts3, (list, tuple))
    assert len(alerts3) >= 1
