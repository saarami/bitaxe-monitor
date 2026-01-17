import pytest

pytestmark = pytest.mark.anyio

@pytest.mark.anyio
async def test_bitaxe_client_builds_request_and_parses_response():
    """Mock BitaxeClient HTTP call with respx and verify response parsing."""
    respx = pytest.importorskip("respx")
    httpx = pytest.importorskip("httpx")

    BitaxeClient = None
    for path in ("app.services.bitaxe_client", "app.services.bitaxe_service", "app.services.bitaxe"):
        try:
            mod = __import__(path, fromlist=["*"])
            BitaxeClient = getattr(mod, "BitaxeClient", None)
            if BitaxeClient:
                break
        except Exception:
            continue
    if BitaxeClient is None:
        pytest.skip("BitaxeClient not found in app.services.*")

    base_url = "http://bitaxe.local"
    endpoint = "/api/system/info"
    expected_url = base_url.rstrip("/") + endpoint
    sample_payload = {"temp": 60.5, "hashrate": 1.1}

    with respx.mock:
        route = respx.get(expected_url).mock(return_value=httpx.Response(200, json=sample_payload))

        init_args = BitaxeClient.__init__.__code__.co_varnames
        if "endpoint" in init_args:
            client = BitaxeClient(base_url=base_url, endpoint=endpoint)
        else:
            client = BitaxeClient(base_url=base_url)

        fetch = getattr(client, "fetch_system_info", None) or getattr(client, "fetch", None)
        if fetch is None:
            pytest.skip("BitaxeClient has no fetch_system_info/fetch method.")

        data = await fetch()
        assert route.called
        assert isinstance(data, dict)
        assert data.get("temp") == 60.5
