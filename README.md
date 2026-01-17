# Bitaxe Monitor – Backend

Backend monitoring service for a Bitaxe miner, built with **FastAPI**, **PostgreSQL**, **Docker**, and **Telegram Bot integration**.
The system collects telemetry data, stores it in a database, and sends alerts / status updates via Telegram.

---

## Features

- FastAPI REST backend
- PostgreSQL database with Alembic migrations
- Telegram Bot integration (Webhook-based)
- Docker & Docker Compose setup
- Separation of concerns: API, services, repositories
- Environment-based configuration

---

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL 16
- SQLAlchemy + Alembic
- Docker / Docker Compose
- Telegram Bot API
- ngrok (for local webhook testing)

---

## Project Structure

```
backend/
├── alembic/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── telegram/
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── services/
│   │   └── telegram_service.py
│   ├── repositories/
│   ├── models/
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file (not committed to Git):

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/bitaxe_monitor_db

TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_SECRET=your_webhook_secret_here
```

---

## Running the Project (Docker)

```bash
docker compose up --build
```

API:
```
http://localhost:8000
```

Swagger:
```
http://localhost:8000/docs
```

---

## Telegram Webhook Setup

```bash
ngrok http 8000
```

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook"   -d "url=https://<NGROK_URL>/api/v1/telegram/webhook"   -d "secret_token=<YOUR_WEBHOOK_SECRET>"
```

Verify:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

---

## Webhook Endpoint

```
POST /api/v1/telegram/webhook
```

- Validates Telegram secret header
- Receives Telegram Update payload
- Delegates logic to service layer

---

## Database Migrations

```bash
docker compose exec api alembic upgrade head
```

---

## Security

- Do not commit `.env`
- Revoke exposed tokens
- Webhook secret validation enabled

---

## Purpose

Portfolio / learning project demonstrating backend architecture,
external integrations, and Docker-based workflows.

---

## Author

Saar Amikam  
Backend Developer
