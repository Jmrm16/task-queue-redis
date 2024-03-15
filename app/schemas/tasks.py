from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskSubmitRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    payload: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=1, ge=1, le=5)


class TaskStatusResponse(BaseModel):
    id: str
    name: str
    status: str
    created_at: float
    updated_at: float
    result: Optional[Any] = None
    error: Optional[str] = None
