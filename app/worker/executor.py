import time
import math
from typing import Callable, Dict, Any, Optional
from app.queue.broker import TaskBroker


class TaskWorker:
    """
    Pulls jobs from the task broker and executes registered handler functions
    with exponential backoff retry semantics.
    """

    def __init__(
        self,
        broker: TaskBroker,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
    ):
        self.broker = broker
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register_handler(self, task_name: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._handlers[task_name] = handler

    def process_task(self, task_id: str) -> bool:
        task = self.broker.get_task(task_id)
        if not task:
            return False

        task_name = task["name"]
        handler = self._handlers.get(task_name)
        if not handler:
            self.broker.update_task_status(task_id, "FAILED", error=f"No handler registered for '{task_name}'")
            return False

        self.broker.update_task_status(task_id, "RUNNING")

        retries = 0
        while retries <= self.max_retries:
            try:
                result = handler(task["payload"])
                self.broker.update_task_status(task_id, "COMPLETED", result=result)
                return True
            except Exception as exc:
                retries += 1
                if retries > self.max_retries:
                    self.broker.update_task_status(
                        task_id,
                        "FAILED",
                        error=f"Exhausted {self.max_retries} retries. Error: {str(exc)}"
                    )
                    return False
                
                # Exponential backoff delay
                delay = self.backoff_factor ** retries
                time.sleep(min(delay, 5.0))
        return False
