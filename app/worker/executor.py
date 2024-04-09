import time
from typing import Dict, Any, Callable
from app.queue.broker import RedisBroker
from app.config import settings

class TaskWorker:
    """Consumes and processes background tasks from the Redis queue."""
    def __init__(self, broker: RedisBroker, max_retries: int = settings.MAX_RETRIES):
        self.broker = broker
        self.max_retries = max_retries
        self.handlers: Dict[str, Callable] = {}

    def register_handler(self, task_name: str, handler_func: Callable):
        self.handlers[task_name] = handler_func
