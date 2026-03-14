"""
Authentication business logic.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)


def register_user(db: Session, name: str, email: str, password: str) -> User:
    """Register a new user. Raises ValueError if email already taken."""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("A user with this email already exists")

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=UserRole.user,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("User registered: %s (id=%d)", email, user.id)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate by email and password. Returns User or None."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user


def create_user_token(user: User) -> str:
    """Create a JWT access token for a user."""
    return create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )


def seed_admin(db: Session, email: str, password: str, name: str = "Admin") -> User:
    """Create an admin user if one doesn't already exist with the given email."""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        logger.info("Admin user already exists: %s", email)
        return existing

    admin = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=UserRole.admin,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    logger.info("Admin user seeded: %s (id=%d)", email, admin.id)
    return admin
