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
