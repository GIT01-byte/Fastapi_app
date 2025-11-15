from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.tasks import TaskCreateSchema, TaskSchema, TaskUpdateSchema, TaskIDs
from database.repository import TaskRepository

router = APIRouter(
    prefix='/tasks/v1',
    tags=['To-do ✅']
)


@router.get('', summary='Получить все задачи 📄')
async def get_tasks():
    tasks = await TaskRepository.get_all()
    return {'data': tasks}

@router.post('/add', summary='Добавить задачу ➕')
async def add_task(
    task: TaskCreateSchema,
):
    task_id = await TaskRepository.add_task(task)
    return {'succes': True, 'task_id': task_id}

@router.put('/{task_id}/edit', summary='Изменить задачу 📝')
async def edit_task(
    task_id: int, 
    updated_task: TaskUpdateSchema
    ):
    task = await TaskRepository.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task.name = updated_task.name
    task.description = updated_task.description

    updated_task = await TaskRepository.update_task(task) 
    return {'succes': True, 'task': updated_task}

@router.patch("/{task_id}/complete", response_model=TaskSchema)
async def complete_task(task_id: int):
    task = await TaskRepository.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    task.completed = not task.completed
    updated_task = await TaskRepository.update_task(task)
    return updated_task

@router.delete('/{task_id}/delete', summary='Удалить задачу 🗑')
async def delete_task(task_id: int):
    task = await TaskRepository.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    await TaskRepository.delete_task(task_id)
    return {'succes': True} 

@router.delete('/delete-many', summary='Удалить несколько задач 🗑')
async def delete_tasks(task_ids: List[int] = Query(..., description="Список ID задач для удаления")):
    for task_id in task_ids:
        task = await TaskRepository.get_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Задача с ID {task_id} не найдена") 

    await TaskRepository.delete_tasks(task_ids) 
    return {'success': True, 'deleted_count': len(task_ids)}
