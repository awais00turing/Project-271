from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    """Get all tasks for a user."""
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """Get a specific task for a user."""
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def create_task(db: Session, task_in: TaskCreate, user_id: int) -> Task:
    """Create a new task for a user."""
    db_task = Task(
        **task_in.dict(),
        user_id=user_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    """Update a task."""
    update_data = task_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task) -> None:
    """Delete a task."""
    db.delete(task)
    db.commit()