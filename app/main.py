from fastapi import FastAPI, Depends

from app.api import auth
from app.api.deps import get_current_user

app = FastAPI(title="Task Manager Backend")

app.include_router(auth.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }