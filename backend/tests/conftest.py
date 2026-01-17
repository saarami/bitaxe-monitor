import os
import pytest

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
def test_database_url() -> str:
    return os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL", "")

@pytest.fixture(scope="session")
def alembic_ini_path() -> str:
    return os.getenv("ALEMBIC_INI", "alembic.ini")

@pytest.fixture(scope="session")
def app_instance():
    """
    Import and return the FastAPI app.

    Default expected: `from app.main import app`
    Override with APP_IMPORT, e.g.: APP_IMPORT="app.main:app"
    """
    import importlib

    target = os.getenv("APP_IMPORT", "app.main:app")
    if ":" not in target:
        pytest.skip(f"APP_IMPORT should look like 'module:attr', got {target!r}")
    mod_name, attr = target.split(":", 1)
    try:
        mod = importlib.import_module(mod_name)
    except Exception as e:
        pytest.skip(f"Could not import FastAPI module {mod_name!r}: {e}")
    if not hasattr(mod, attr):
        pytest.skip(f"Module {mod_name!r} has no attribute {attr!r}")
    return getattr(mod, attr)

@pytest.fixture
async def client(app_instance):
    """
    Async HTTP client for FastAPI using httpx.ASGITransport.
    """
    import httpx
    transport = httpx.ASGITransport(app=app_instance)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
