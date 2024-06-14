from fastapi import APIRouter, HTTPException, status
from app.schemas.tasks import TaskSubmitRequest, TaskStatusResponse
from app.queue.broker import TaskBroker

router = APIRouter(prefix="/tasks", tags=["Task Queue"])
broker = TaskBroker()


@router.post("/", response_model=TaskStatusResponse, status_code=status.HTTP_202_ACCEPTED)
def submit_task(req: TaskSubmitRequest):
    task_id = broker.enqueue(task_name=req.name, payload=req.payload, priority=req.priority)
    task = broker.get_task(task_id)
    return task


@router.get("/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: str):
    task = broker.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/{task_id}/cancel", response_model=TaskStatusResponse)
def cancel_task(task_id: str):
    task = broker.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task["status"] in ("COMPLETED", "FAILED"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel task already in '{task['status']}' state."
        )
    broker.update_task_status(task_id, "CANCELLED")
    return broker.get_task(task_id)
