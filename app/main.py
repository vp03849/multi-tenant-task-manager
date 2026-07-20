from fastapi import FastAPI, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.api import auth, workspaces, projects, tasks

app = FastAPI(title="Task Manager API")

app.include_router(auth.router)
app.include_router(workspaces.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)

@app.get("/me")
def read_current_user(user: User = Depends(get_current_user)):
    return {"email": user.email}