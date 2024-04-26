from app.queue.broker import RedisBroker
from app.worker.executor import TaskWorker

def test_broker_enqueue_and_retrieve():
    broker = RedisBroker(redis_url="redis://localhost:9999/0")
    task = broker.enqueue(task_id="task-123", name="test_job", payload={"count": 5})
    assert task["id"] == "task-123"
    assert task["status"] == "pending"
    retrieved = broker.get_task("task-123")
    assert retrieved["payload"]["count"] == 5

def test_worker_processes_task_successfully():
    broker = RedisBroker(redis_url="redis://localhost:9999/0")
    worker = TaskWorker(broker=broker)
    worker.register_handler("compute", lambda p: {"total": p["a"] + p["b"]})
    broker.enqueue(task_id="task-success", name="compute", payload={"a": 10, "b": 20})
    result = worker.process_single_task()
    assert result["status"] == "completed"
    assert result["result"] == {"total": 30}
