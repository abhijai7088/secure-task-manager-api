"""
Task business logic.
"""

import logging
from typing import Optional, Tuple, List

from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)


def create_task(
    db: Session,
    owner_id: int,
    title: str,
    description: Optional[str] = None,
    status: str = "pending",
) -> Task:
    """Create a new task owned by the given user."""
    task = Task(
        title=title,
        description=description,
        status=TaskStatus(status),
        owner_id=owner_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info("Task created: id=%d owner=%d", task.id, owner_id)
    return task


def get_tasks(
    db: Session,
    user: User,
    page: int = 1,
    per_page: int = 20,
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
) -> Tuple[List[Task], int]:
    """
    Return paginated tasks.
    Admins see all tasks; regular users see only their own.
    """
    query = db.query(Task)

    if user.role != UserRole.admin:
        query = query.filter(Task.owner_id == user.id)

    if status_filter:
        query = query.filter(Task.status == TaskStatus(status_filter))

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    total = query.count()
    tasks = (
        query.order_by(Task.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return tasks, total


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """Fetch a single task by primary key."""
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(
    db: Session,
    task: Task,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Task:
    """Update task fields."""
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = TaskStatus(status)
    db.commit()
    db.refresh(task)
    logger.info("Task updated: id=%d", task.id)
    return task


def delete_task(db: Session, task: Task) -> None:
    """Delete a task."""
    task_id = task.id
    db.delete(task)
    db.commit()
    logger.info("Task deleted: id=%d", task_id)
