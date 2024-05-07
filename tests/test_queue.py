from fastapi.testclient import TestClient
from app.queue.broker import TaskBroker
from app.worker.executor import TaskWorker
from app.main import app

client = TestClient(app)


def test_broker_enqueue_and_retrieve():
    broker = TaskBroker()
    task_id = broker.enqueue("send_email", {"to": "user@example.com"}, priority=2)
    assert task_id is not None

    task = broker.get_task(task_id)
    assert task["name"] == "send_email"
    assert task["status"] == "QUEUED"
    assert task["priority"] == 2


def test_worker_processes_task_successfully():
    broker = TaskBroker()
    worker = TaskWorker(broker=broker, max_retries=1)

    # Register mock task handler
    worker.register_handler("calculate_sum", lambda p: p["a"] + p["b"])

    task_id = broker.enqueue("calculate_sum", {"a": 10, "b": 25})
    success = worker.process_task(task_id)

    assert success is True
    updated = broker.get_task(task_id)
    assert updated["status"] == "COMPLETED"
    assert updated["result"] == 35


def test_worker_handles_retries_and_failure():
    broker = TaskBroker()
    worker = TaskWorker(broker=broker, max_retries=2, backoff_factor=1.0)

    attempts = 0
    def failing_handler(payload):
        nonlocal attempts
        attempts += 1
        raise ValueError("Simulated network failure")

    worker.register_handler("flaky_job", failing_handler)
    task_id = broker.enqueue("flaky_job", {})

    success = worker.process_task(task_id)
    assert success is False
    assert attempts == 3  # Initial try + 2 retries
    updated = broker.get_task(task_id)
    assert updated["status"] == "FAILED"
    assert "Exhausted 2 retries" in updated["error"]


def test_api_submit_and_query_task():
    resp = client.post("/api/v1/tasks/", json={"name": "generate_report", "payload": {"year": 2024}})
    assert resp.status_code == 202
    data = resp.json()
    task_id = data["id"]
    assert data["status"] == "QUEUED"

    get_resp = client.get(f"/api/v1/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == task_id
