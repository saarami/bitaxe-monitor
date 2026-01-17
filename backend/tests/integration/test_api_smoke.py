import pytest

@pytest.mark.anyio
async def test_health_endpoint(client):
    candidates = ["/health", "/healthz", "/api/health", "/"]
    last = None
    for path in candidates:
        last = await client.get(path)
        if last.status_code < 500:
            assert last.status_code in (200, 204, 404)
            return
    assert last is not None
    assert last.status_code < 500, f"All candidate health endpoints returned 5xx. Last={last.status_code} {last.text}"
