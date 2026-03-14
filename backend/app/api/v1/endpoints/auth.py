"""
Authentication endpoints: register, login, me.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    UserDataResponse,
    TokenDataResponse,
)
from app.services.auth_service import authenticate_user, create_user_token, register_user
from app.utils.responses import success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_model=UserDataResponse,
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """Create a new user account."""
    try:
        user = register_user(db, payload.name, payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    return success_response(
        "User registered successfully",
        data=UserResponse.model_validate(user).model_dump(),
    )


@router.post(
    "/login",
    summary="Login and receive a JWT token",
    response_model=TokenDataResponse,
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return an access token."""
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_user_token(user)
    return success_response(
        "Login successful",
        data=TokenResponse(access_token=token).model_dump(),
    )


@router.get(
    "/me",
    summary="Get current authenticated user",
    response_model=UserDataResponse,
)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the profile of the currently authenticated user."""
    return success_response(
        "User profile retrieved",
        data=UserResponse.model_validate(current_user).model_dump(),
    )
