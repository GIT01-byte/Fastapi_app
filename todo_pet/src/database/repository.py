from typing import List

from sqlalchemy import delete, select

from schemas.tasks import TaskCreateSchema
from database.tasks import new_session
from models.tasks import TaskOrm


class TaskRepository:
    @classmethod
    async def get_all(cls):
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models


    @classmethod
    async def get_by_id(cls, task_id: int):
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            task = result.scalars().first()
            return task


    @classmethod
    async def add_task(cls, data: TaskCreateSchema):
        async with new_session() as session:
            task_dict = data.model_dump()
            
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id


    @classmethod
    async def update_task(cls, task: TaskOrm):
        async with new_session() as session:
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task


    @classmethod
    async def delete_task(cls, task_id: int):
        async with new_session() as session:
            query = delete(TaskOrm).where(TaskOrm.id == task_id)
            await session.execute(query)
            await session.commit()
            return True


    @classmethod
    async def delete_tasks(cls, task_ids: List[int]):
        async with new_session() as session:
            query = delete(TaskOrm).where(TaskOrm.id.in_(task_ids))
            await session.execute(query)
            await session.commit()
            return True
        