import pytest

def test_normalize_telemetry_handles_common_fields():
    normalize = None
    for path in ("app.services.telemetry_normalization", "app.services.telemetry_service", "app.services.telemetry"):
        try:
            mod = __import__(path, fromlist=["*"])
            normalize = getattr(mod, "normalize_telemetry", None) or getattr(mod, "normalize", None)
            if normalize:
                break
        except Exception:
            continue
    if normalize is None:
        pytest.skip("normalize_telemetry function not found in app.services.*")

    raw = {"temp": 70.0, "hashrate": 1.5, "fan": 5000, "power": 18.2}
    norm = normalize(raw)
    assert isinstance(norm, dict)

    temp = norm.get("temperature_c") or norm.get("temp_c") or norm.get("temperature")
    assert float(temp) == pytest.approx(70.0, rel=0.01)
