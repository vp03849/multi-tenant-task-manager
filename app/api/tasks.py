from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.db.session import get_db
from app.api.deps import get_current_user, require_permission
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/workspaces/{workspace_id}/projects/{project_id}/tasks", tags=["tasks"])

def _get_project_or_404(db: Session, workspace_id: uuid.UUID, project_id: uuid.UUID) -> Project:
    project = db.query(Project).filter(Project.id == project_id, Project.workspace_id == workspace_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(workspace_id: uuid.UUID, project_id: uuid.UUID, payload: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_permission(db, user.id, workspace_id, "task:create")
    _get_project_or_404(db, workspace_id, project_id)
    task = Task(project_id=project_id, title=payload.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=list[TaskOut])
def list_tasks(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    status_filter: TaskStatus | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    require_permission(db, user.id, workspace_id, "task:create")
    _get_project_or_404(db, workspace_id, project_id)
    query = db.query(Task).filter(Task.project_id == project_id)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    return query.offset(offset).limit(limit).all()

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(workspace_id: uuid.UUID, project_id: uuid.UUID, task_id: uuid.UUID, payload: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_permission(db, user.id, workspace_id, "task:update")
    _get_project_or_404(db, workspace_id, project_id)
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.status is not None:
        task.status = payload.status
    if payload.assignee_id is not None:
        require_permission(db, user.id, workspace_id, "task:assign")
        task.assignee_id = payload.assignee_id
    db.commit()
    db.refresh(task)
    return task