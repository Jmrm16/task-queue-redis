from app.queue.broker import RedisBroker
from app.worker.executor import TaskWorker

def test_broker_enqueue_and_retrieve():
    broker = RedisBroker(redis_url="redis://localhost:9999/0")
    task = broker.enqueue(task_id="task-123", name="test_job", payload={"count": 5})
    assert task["id"] == "task-123"
    assert task["status"] == "pending"
    retrieved = broker.get_task("task-123")
    assert retrieved["payload"]["count"] == 5
