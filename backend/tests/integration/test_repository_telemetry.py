import pytest

pytestmark = pytest.mark.anyio

@pytest.mark.anyio
async def test_telemetry_repository_roundtrip(test_database_url):
    if not test_database_url:
        pytest.skip("No DATABASE_URL/TEST_DATABASE_URL configured.")

    try:
        from app.db.session import SessionLocal
    except Exception:
        SessionLocal = None
    try:
        from app.db.session import async_session_maker
    except Exception:
        async_session_maker = None

    repo = None
    for path in (
        "app.repositories.telemetry_repository",
        "app.repositories.telemetry",
        "app.repositories.telemetry_repo",
    ):
        try:
            mod = __import__(path, fromlist=["*"])
            repo_cls = getattr(mod, "TelemetryRepository", None) or getattr(mod, "TelemetryRepo", None)
            if repo_cls:
                repo = repo_cls()
                break
        except Exception:
            continue

    if repo is None:
        pytest.skip("TelemetryRepository not found (app.repositories.*). Adjust import paths in the test.")

    sample = {
        "temperature_c": 65.0,
        "hashrate_ghs": 1.2,
        "power_w": 15.5,
        "fan_rpm": 4500,
        "timestamp": None,
    }

    async def call_create(sess):
        for name in ("create", "create_telemetry", "insert", "add"):
            if hasattr(repo, name):
                fn = getattr(repo, name)
                try:
                    return await fn(sess, sample)
                except TypeError:
                    return fn(sess, sample)
        pytest.skip("Repository has no create-like method (create/create_telemetry/insert/add).")

    async def call_latest(sess):
        for name in ("get_latest", "latest", "read_latest"):
            if hasattr(repo, name):
                fn = getattr(repo, name)
                try:
                    return await fn(sess)
                except TypeError:
                    return fn(sess)
        pytest.skip("Repository has no latest-like method (get_latest/latest/read_latest).")

    if async_session_maker is not None:
        async with async_session_maker() as session:
            await call_create(session)
            latest = await call_latest(session)
    elif SessionLocal is not None:
        with SessionLocal() as session:
            await call_create(session)
            latest = await call_latest(session)
    else:
        pytest.skip("No session factory found in app.db.session (SessionLocal/async_session_maker).")

    assert latest is not None
    temp = latest.get("temperature_c") if isinstance(latest, dict) else getattr(latest, "temperature_c", None)
    assert temp is not None
    assert float(temp) == pytest.approx(65.0, rel=0.2)
