import json
import uuid
import time
from typing import Optional, Dict, Any
from app.config import settings


class TaskBroker:
    """
    In-memory / Redis task broker managing queued jobs, priority states,
    and metadata persistence.
    """

    def __init__(self, redis_client=None):
        self.redis = redis_client
        self._memory_store: Dict[str, Dict[str, Any]] = {}
        self._memory_queue: list[str] = []

    def enqueue(self, task_name: str, payload: Dict[str, Any], priority: int = 1) -> str:
        task_id = str(uuid.uuid4())
        task_record = {
            "id": task_id,
            "name": task_name,
            "payload": payload,
            "priority": priority,
            "status": "QUEUED",
            "created_at": time.time(),
            "updated_at": time.time(),
            "retries": 0,
            "result": None,
            "error": None,
        }

        if self.redis:
            self.redis.set(f"task:{task_id}", json.dumps(task_record))
            self.redis.lpush("queue:tasks", task_id)
        else:
            self._memory_store[task_id] = task_record
            self._memory_queue.append(task_id)

        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        if self.redis:
            raw = self.redis.get(f"task:{task_id}")
            return json.loads(raw) if raw else None
        return self._memory_store.get(task_id)

    def update_task_status(
        self,
        task_id: str,
        status: str,
        result: Any = None,
        error: Optional[str] = None,
    ) -> None:
        task = self.get_task(task_id)
        if not task:
            return

        task["status"] = status
        task["updated_at"] = time.time()
        if result is not None:
            task["result"] = result
        if error:
            task["error"] = error

        if self.redis:
            self.redis.set(f"task:{task_id}", json.dumps(task))
        else:
            self._memory_store[task_id] = task
