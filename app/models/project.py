import uuid
from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id"), nullable=False)
