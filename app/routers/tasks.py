from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import Task
from app.schemas import TaskResponse, CreateTask, UpdateTask
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):

    db_response = db.scalars(select(Task).where(Task.user_id == current_user.id)).all()

    return db_response


@router.get("/{task_id}", status_code=200, response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_response = db.scalars(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).one_or_none()
    if db_response is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_response


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: CreateTask,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_task = Task(title=task.title, user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.patch("/{task_id}", response_model=TaskResponse, status_code=200)
def update_task(
    task_id: int,
    updates: UpdateTask,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_task = db.scalars(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updates_data = updates.model_dump(exclude_unset=True)

    for field, value in updates_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_task = db.scalars(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).one_or_none()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
