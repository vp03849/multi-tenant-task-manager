from pydantic import BaseModel
import uuid

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    name: str

    class Config:
        from_attributes = True