from typing import Optional
from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    completed: bool = False


class TaskSchema(BaseModel):
    id: int

