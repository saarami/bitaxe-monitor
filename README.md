# ⚡ Bitaxe Monitor – Home Bitcoin Miner Backend

A **backend monitoring system for a home Bitcoin miner (Bitaxe Gamma 601)**, built as a personal hobby project that evolved into a full production-style backend.

The goal of this project is to make **Bitcoin mining more accessible and understandable**, especially for people without deep technical or mining background, by providing clear metrics, alerts, and a simple dashboard.

---

## 🚀 What Is Bitaxe?

**Bitaxe** is an open-source, low-power Bitcoin mining device designed for home use.  
Unlike industrial mining rigs, it is quiet, energy-efficient, and often used as a **learning or hobby miner**.

This project was built around a real Bitaxe Gamma 601 device running at home.

---

## 🎯 Project Goals

- Monitor a home Bitcoin miner in real time
- Collect telemetry and operational metrics automatically
- Notify users when something goes wrong
- Present data in a simple, understandable way
- Serve as an educational backend project around Bitcoin mining

---

## 🧠 Key Features

- **REST API** built with FastAPI
- **Scheduled data collection** (polling the miner at fixed intervals)
- **Telegram-based user** interface for submitting and viewing miner data
- **Real-time alerts** via Telegram
- **Persistent storage** with PostgreSQL
- **Caching** for frequently accessed metrics
- **Dockerized** services for easy deployment
- **React + Vite dashboard** for visualization

---

## 🧱 Architecture Overview

```text
┌──────────────┐
│   Bitaxe     │
│  (Miner HW)  │
└──────┬───────┘
       │ HTTP / JSON
┌──────▼───────┐
│   Poller     │  (Scheduled jobs)
└──────┬───────┘
┌──────▼───────┐
│   FastAPI    │  (REST API)
│   Routers    │
└──────┬───────┘
┌──────▼───────┐
│   Services   │  (Business logic)
└──────┬───────┘
┌──────▼───────┐
│ Repositories │  (DB access)
└──────┬───────┘
┌──────▼───────┐
│ PostgreSQL   │
└──────────────┘

Additional integrations:
- Telegram Bot (alerts)
- React/Vite Dashboard (frontend)
```

---

## 🛠 Tech Stack

| Category | Technology |
|-------|------------|
| Backend | Python 3.11, FastAPI |
| Database | PostgreSQL |
| Scheduling | Background polling |
| Alerts | Telegram Bot |
| Frontend | React + Vite |
| Containers | Docker |
| Deployment | Docker Compose |

---

## 📁 Project Structure

```text
bitaxe-monitor/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── models/
│   │   ├── infra/
│   │   └── main.py
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ▶️ Running Locally

```bash
docker compose up --build
```

Backend API:
```
http://localhost:8000
```

---

## 🔔 Alerts & Monitoring

The system sends Telegram alerts for:
- Miner offline
- Temperature thresholds
- Hashrate drops
- General health issues

This allows hands-off monitoring of a home miner.

---

## 🧩 Why This Project Is Interesting

- Built around **real hardware**
- Combines backend, scheduling, alerts, and visualization
- Designed for **non-expert users**
- Demonstrates end-to-end ownership of a system
- Strong example of a hobby project turned into a serious backend system

---

## 🚧 Future Improvements

- Authentication & multi-user support
- Historical charts & analytics
- Support for additional miners

---

## 👤 Author

**Saar Amikam**  
Backend Developer  
Python · FastAPI · Systems · Cloud  

---
