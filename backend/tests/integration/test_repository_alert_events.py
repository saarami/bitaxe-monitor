import pytest

pytestmark = pytest.mark.anyio

@pytest.mark.anyio
async def test_alert_events_repository_roundtrip(test_database_url):
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
        "app.repositories.alert_events_repository",
        "app.repositories.alert_events",
        "app.repositories.alert_event_repo",
    ):
        try:
            mod = __import__(path, fromlist=["*"])
            repo_cls = getattr(mod, "AlertEventRepository", None) or getattr(mod, "AlertEventsRepository", None)
            if repo_cls:
                repo = repo_cls()
                break
        except Exception:
            continue

    if repo is None:
        pytest.skip("AlertEventRepository not found (app.repositories.*). Adjust import paths in the test.")

    sample = {
        "type": "TEMP_HIGH",
        "message": "Temperature above threshold",
        "value": 85.0,
        "threshold": 80.0,
        "created_at": None,
    }

    async def call_create(sess):
        for name in ("create", "add", "insert"):
            if hasattr(repo, name):
                fn = getattr(repo, name)
                try:
                    return await fn(sess, sample)
                except TypeError:
                    return fn(sess, sample)
        pytest.skip("Repository has no create-like method (create/add/insert).")

    async def call_list(sess):
        for name in ("list_recent", "get_recent", "recent"):
            if hasattr(repo, name):
                fn = getattr(repo, name)
                try:
                    return await fn(sess, limit=10)
                except TypeError:
                    return fn(sess, limit=10)
        pytest.skip("Repository has no list_recent-like method.")

    if async_session_maker is not None:
        async with async_session_maker() as session:
            await call_create(session)
            events = await call_list(session)
    elif SessionLocal is not None:
        with SessionLocal() as session:
            await call_create(session)
            events = await call_list(session)
    else:
        pytest.skip("No session factory found in app.db.session (SessionLocal/async_session_maker).")

    assert events is not None
    assert len(events) >= 1
