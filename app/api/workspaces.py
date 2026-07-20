from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.db.session import get_db
from app.api.deps import get_current_user, require_permission
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceOut, MemberInvite, MemberOut

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.post("/", response_model=WorkspaceOut, status_code=201)
def create_workspace(payload: WorkspaceCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    workspace = Workspace(name=payload.name)
    db.add(workspace)
    db.flush()  # get workspace.id before commit
    membership = WorkspaceMember(user_id=user.id, workspace_id=workspace.id, role=WorkspaceRole.owner)
    db.add(membership)
    db.commit()
    db.refresh(workspace)
    return workspace

@router.post("/{workspace_id}/members", response_model=MemberOut, status_code=201)
def invite_member(workspace_id: uuid.UUID, payload: MemberInvite, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_permission(db, user.id, workspace_id, "member:invite")
    invitee = db.query(User).filter(User.email == payload.email).first()
    if not invitee:
        raise HTTPException(status_code=404, detail="User with that email not found")
    membership = WorkspaceMember(user_id=invitee.id, workspace_id=workspace_id, role=payload.role)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership

@router.get("/{workspace_id}/members", response_model=list[MemberOut])
def list_members(workspace_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_permission(db, user.id, workspace_id, "task:create")  # any member can view
    return db.query(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id).all()