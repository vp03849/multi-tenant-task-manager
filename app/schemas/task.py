from pydantic import BaseModel
import uuid
from app.models.task import TaskStatus

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    assignee_id: uuid.UUID | None = None

class TaskOut(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    assignee_id: uuid.UUID | None = None
    title: str
    status: TaskStatus

    class Config:
        from_attributes = True