"""
Pydantic schemas for Task CRUD operations.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskStatusEnum(str, Enum):
    """Allowed task statuses for API."""
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------
class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, examples=["Implement login page"])
    description: Optional[str] = Field(None, max_length=2000, examples=["Build the login page with validation"])
    status: TaskStatusEnum = Field(default=TaskStatusEnum.pending)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatusEnum] = None


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------
class TaskResponse(BaseModel):
    """Single task in API responses."""
    id: int
    title: str
    description: Optional[str]
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    """Paginated task list response."""
    message: str
    data: List[TaskResponse]
    total: int
    page: int
    per_page: int


class TaskDataResponse(BaseModel):
    """Successful response containing a single task."""
    message: str
    data: TaskResponse


class MessageResponse(BaseModel):
    """Simple message-only response."""
    message: str
