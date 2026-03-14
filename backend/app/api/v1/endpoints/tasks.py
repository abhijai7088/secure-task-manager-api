"""
Task CRUD endpoints with role-based access control.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskDataResponse, TaskListResponse, TaskResponse, TaskUpdate, MessageResponse
from app.services.task_service import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks,
    update_task,
)
from app.utils.responses import success_response

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_model=TaskDataResponse,
)
def create_new_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a task owned by the authenticated user."""
    task = create_task(
        db,
        owner_id=current_user.id,
        title=payload.title,
        description=payload.description,
        status=payload.status.value,
    )
    return success_response(
        "Task created successfully",
        data=TaskResponse.model_validate(task).model_dump(),
    )


@router.get(
    "",
    summary="List tasks (paginated, filterable)",
    response_model=TaskListResponse,
)
def list_tasks(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in title"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List tasks with pagination.
    Regular users see their own tasks; admins see all tasks.
    """
    tasks, total = get_tasks(db, current_user, page, per_page, status_filter, search)
    return TaskListResponse(
        message="Tasks retrieved successfully",
        data=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{task_id}",
    summary="Get a task by ID",
    response_model=TaskDataResponse,
)
def get_single_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a task. Users can only access their own tasks; admins can access any."""
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if current_user.role != UserRole.admin and task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return success_response(
        "Task retrieved successfully",
        data=TaskResponse.model_validate(task).model_dump(),
    )


@router.put(
    "/{task_id}",
    summary="Update a task",
    response_model=TaskDataResponse,
)
def update_existing_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a task. Users can only update their own tasks; admins can update any."""
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if current_user.role != UserRole.admin and task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    updated = update_task(
        db,
        task,
        title=payload.title,
        description=payload.description,
        status=payload.status.value if payload.status else None,
    )
    return success_response(
        "Task updated successfully",
        data=TaskResponse.model_validate(updated).model_dump(),
    )


@router.delete(
    "/{task_id}",
    summary="Delete a task",
    response_model=MessageResponse,
)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task. Users can only delete their own tasks; admins can delete any."""
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if current_user.role != UserRole.admin and task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    delete_task(db, task)
    return success_response("Task deleted successfully")
