import os
import pytest

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine


def _get_db_url(cfg: Config) -> str:
    # Prefer env (typical in containers), fallback to alembic.ini sqlalchemy.url if exists
    return (
        os.getenv("TEST_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or cfg.get_main_option("sqlalchemy.url")
        or ""
    )


def _get_current_revision(db_url: str) -> str | None:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        return ctx.get_current_revision()


def test_alembic_upgrade_head_smoke(alembic_ini_path: str):
    if not os.path.exists(alembic_ini_path):
        pytest.skip(f"{alembic_ini_path} not found. Set ALEMBIC_INI env var if needed.")

    cfg = Config(alembic_ini_path)

    db_url = _get_db_url(cfg)
    if not db_url:
        pytest.skip("No DATABASE_URL/TEST_DATABASE_URL/sqlalchemy.url configured for Alembic smoke test.")

    # upgrade to head
    command.upgrade(cfg, "head")

    # expected head revision from migration scripts
    script = ScriptDirectory.from_config(cfg)
    head_rev = script.get_current_head()
    assert head_rev, "Could not resolve Alembic head revision from scripts."

    # current revision from DB
    current_rev = _get_current_revision(db_url)
    assert current_rev, "DB current revision is empty after upgrade."
    assert current_rev == head_rev, f"DB revision {current_rev} != head {head_rev}"
