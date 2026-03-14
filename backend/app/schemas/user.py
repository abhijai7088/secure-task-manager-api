"""
Pydantic schemas for User registration, login, and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------
class UserRegister(BaseModel):
    """Schema for user registration."""
    name: str = Field(..., min_length=1, max_length=100, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["strongpassword"])


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["strongpassword"])


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------
class UserResponse(BaseModel):
    """Public user data returned in API responses."""
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    """Wrapper for auth endpoint responses."""
    message: str
    data: Optional[dict] = None


class UserDataResponse(BaseModel):
    """Successful response containing user data."""
    message: str
    data: UserResponse


class TokenDataResponse(BaseModel):
    """Successful response containing a JWT token."""
    message: str
    data: TokenResponse
