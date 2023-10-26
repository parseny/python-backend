from celery import Celery
from config import REDIS_URL, RMQ_URL
from fastapi import APIRouter

router = APIRouter()

celery_app = Celery('tasks', broker=RMQ_URL, backend=REDIS_URL)

@router.post("/orders/create")
async def start_create_task(description: str):
    task = celery_app.send_task("tasks.accept_order", args=[description])
    result = task.get() if task.state == 'SUCCESS' else None
    return {"status": task.state, "task_id": task.id, "result": result}

@router.post("/oreders/prepare/")
async def start_prepare_task(order_id: int):
    task = celery_app.send_task("tasks.prepare_order", args=[order_id])
    result = task.get() if task.state == 'SUCCESS' else None
    return {"status": task.state, "task_id": task.id, "result": result}

@router.post("/orders/deliver/")
async def start_prepare_task(order_id: int):
    task = celery_app.send_task("tasks.deliver_order", args=[order_id])
    result = task.get() if task.state == 'SUCCESS' else None
    return {"status": task.state, "task_id": task.id, "result": result}
