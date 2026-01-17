
#!/usr/bin/env bash
set -euo pipefail

cd /app

# Optional: disable migrations in this container (e.g., poller)
RUN_MIGRATIONS="${RUN_MIGRATIONS:-1}"

# Wait for DB (best-effort). Use Python to avoid extra deps.
python - <<'PY'
import os, time
import psycopg
from urllib.parse import urlparse

url = os.environ.get("DATABASE_URL", "")
# Expect SQLAlchemy URL like postgresql+psycopg://user:pass@host:port/db
if "+psycopg" in url:
    url = url.replace("postgresql+psycopg://", "postgresql://", 1)

p = urlparse(url)
host = p.hostname or "db"
port = p.port or 5432
user = p.username or "postgres"
password = p.password or "postgres"
dbname = (p.path or "/postgres").lstrip("/")

dsn = f"host={host} port={port} user={user} password={password} dbname={dbname}"
deadline = time.time() + 60
while True:
    try:
        with psycopg.connect(dsn, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        break
    except Exception as e:
        if time.time() > deadline:
            raise
        time.sleep(1)
PY

if [ "$RUN_MIGRATIONS" != "0" ]; then
  alembic upgrade head
fi

exec "$@"
