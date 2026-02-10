# Backend – Bitaxe Monitor

This directory contains the **backend service** responsible for monitoring a home Bitcoin miner (Bitaxe Gamma 601),
collecting telemetry data, persisting it, and triggering alerts.

This README focuses on **developer-oriented details**.

---

## Responsibilities

- Periodic polling of the Bitaxe miner
- Data normalization and validation
- Persistence to PostgreSQL
- Triggering Telegram alerts
- Exposing a REST API for the frontend dashboard

---

## Architecture

- **Routers** – FastAPI endpoints (HTTP layer)
- **Schemas** – Pydantic request/response validation
- **Services** – Business logic (polling, alerts, aggregation)
- **Repositories** – Database access layer
- **Models** – SQLAlchemy ORM entities

---

## Environment Variables

```env
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/db
REDIS_URL=redis://redis:6379/0
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

---

## Run Backend Only

```bash
docker compose up backend --build
```

API will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## Notes

- Polling intervals are configurable in the service layer
- Alerts are intentionally simple and opinionated
- Backend is designed to run independently from the frontend
