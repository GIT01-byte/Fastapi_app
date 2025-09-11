from typing import Annotated

from fastapi import APIRouter, Depends

from schemas.tasks import TaskCreateSchema
from database.repository import TaskRepository

router = APIRouter(
    prefix='/tasks/v1',
    tags=['To-do']
)

@router.post('/add')
async def add_task(
    task: Annotated[TaskCreateSchema, Depends()]
):
    task_id = await TaskRepository.add_task(task)
    return {'succes': True, 'task_id': task_id}

@router.get('')
async def get_tasks():
    tasks = await TaskRepository.get_all()
    return {'data': tasks}
