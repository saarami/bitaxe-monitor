
# Bitaxe Monitor API (V1)

Production-grade FastAPI backend for monitoring a Bitaxe Gamma 601 miner.

## Features
- Polls miner telemetry every 60 seconds
- Stores normalized telemetry in PostgreSQL
- Temperature alerting with cooldown + hysteresis
- Telegram webhook bot with commands:
  - /status
  - /last 10
  - /thresholds
- Dockerized (API + Poller + DB)
- Clean layered architecture
- Unit & integration tests

## Run
docker compose up --build


## Migrations
Migrations are applied automatically on container startup via Alembic.
