FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
