# Task Queue Redis API

A lightweight, asynchronous distributed background task queue and worker execution engine built with **Python 3.11**, **FastAPI**, and **Redis**.

Provides reliable job dispatching, exponential backoff retries with jitter, task cancellation, and status tracking for long-running backend workloads.

---

## 🌟 Key Features

- **Asynchronous Task Broker:** Enqueue jobs with custom payloads, priorities, and unique UUID identifiers.
- **Resilient Worker Execution:** Background consumer with automated exponential backoff retry policies (`delay = factor ** retries`).
- **State Lifecycle Tracking:** Tracks jobs across `QUEUED` ➔ `RUNNING` ➔ `COMPLETED` / `FAILED` / `CANCELLED`.
- **Zero-Config In-Memory Fallback:** Operates with native in-memory queues during local testing or tests, and scales to Redis in production.

---

## 🛠️ Architecture

```text
task-queue-redis/
├── app/
│   ├── api/             # REST endpoints (POST /tasks/, GET /tasks/{id})
│   ├── queue/           # Redis broker, persistence, and queue management
│   ├── worker/          # Consumer daemon and exponential backoff retry loop
│   ├── schemas/         # Pydantic v2 schemas
│   ├── config.py        # Settings and environment configs
│   └── main.py          # FastAPI application factory
├── tests/               # Pytest test suite validating queue lifecycle and retries
├── docker-compose.yml   # Multi-container orchestration (API + Redis 7)
├── Dockerfile           # Minimal Python container image
└── requirements.txt
```

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/Jmrm16/task-queue-redis.git
cd task-queue-redis
pip install -r requirements.txt
```

### 2. Run with Docker Compose
```bash
docker compose up --build
```
Interactive API documentation will be available at:
👉 **http://localhost:8000/docs**

### 3. Example Usage

**Submit a Background Task:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "export_analytics_csv",
    "payload": {"start_date": "2024-01-01", "format": "csv"},
    "priority": 1
  }'
```

**Check Task Status:**
```bash
curl "http://localhost:8000/api/v1/tasks/<TASK_ID>"
```

---

## 🧪 Testing

```bash
pytest -v
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.








