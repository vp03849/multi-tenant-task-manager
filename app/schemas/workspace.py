from pydantic import BaseModel, EmailStr
import uuid
from app.models.workspace import WorkspaceRole

class WorkspaceCreate(BaseModel):
    name: str

class WorkspaceOut(BaseModel):
    id: uuid.UUID
    name: str
    class Config:
        from_attributes = True

class MemberInvite(BaseModel):
    email: EmailStr
    role: WorkspaceRole = WorkspaceRole.member

class MemberOut(BaseModel):
    user_id: uuid.UUID
    role: WorkspaceRole
    class Config:
        from_attributes = True