from fastapi import FastAPI
from app.routers.tasks import router as task_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
def root():
    return {"message": "Hello"}
