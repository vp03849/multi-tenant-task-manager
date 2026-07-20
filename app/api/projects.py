from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from app.db.session import get_db
from app.api.deps import get_current_user, require_permission
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter(prefix="/workspaces/{workspace_id}/projects", tags=["projects"])

@router.post("/", response_model=ProjectOut, status_code=201)
def create_project(workspace_id: uuid.UUID, payload: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_permission(db, user.id, workspace_id, "project:create")
    project = Project(workspace_id=workspace_id, name=payload.name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=list[ProjectOut])
def list_projects(workspace_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_permission(db, user.id, workspace_id, "task:create")
    return db.query(Project).filter(Project.workspace_id == workspace_id).all()