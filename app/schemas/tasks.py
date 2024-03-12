from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Task identifier")
    payload: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(0, ge=0, le=10)
