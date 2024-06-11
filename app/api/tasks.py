import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas.tasks import TaskCreate, TaskResponse
from app.queue.broker import RedisBroker

router = APIRouter(prefix="/tasks", tags=["Task Queue"])
broker = RedisBroker()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def submit_task(task: TaskCreate):
    task_id = str(uuid.uuid4())
    created = broker.enqueue(task_id=task_id, name=task.name, payload=task.payload, priority=task.priority)
    return created
