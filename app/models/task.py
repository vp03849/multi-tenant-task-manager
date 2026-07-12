import uuid
from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    status = Column(String, default="todo")
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    assigned_user_id = Column(String, ForeignKey("users.id"), nullable=True)
