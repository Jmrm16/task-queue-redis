import json
import redis
from typing import Dict, Any, Optional
from app.config import settings

class RedisBroker:
    """Manages task queuing and status persistence with Redis."""
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis_url = redis_url
        try:
            self.client = redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            self.is_connected = True
        except Exception:
            self.client = None
            self.is_connected = False
            self._in_memory_queue = []
            self._in_memory_tasks = {}

    def enqueue(self, task_id: str, name: str, payload: Dict[str, Any], priority: int = 0) -> Dict[str, Any]:
        task_data = {"id": task_id, "name": name, "payload": payload, "priority": priority, "status": "pending", "result": None, "retries": 0}
        if self.is_connected and self.client:
            self.client.hset(f"task:{task_id}", mapping={"data": json.dumps(task_data)})
            self.client.lpush("tasks:default", task_id)
        else:
            self._in_memory_tasks[task_id] = task_data
            self._in_memory_queue.insert(0, task_id)
        return task_data
