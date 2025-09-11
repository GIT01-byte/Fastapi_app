from sqlalchemy import select
from schemas.tasks import TaskCreateSchema
from database.tasks import new_session
from models.tasks import TaskOrm


class TaskRepository:
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
    async def get_all(cls):
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models
