
from sqlalchemy import select

from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.db.session import SessionLocal
from app.models.user import User, UserRole


def register_user(db: Session, name: str, email: str, password: str) -> User:
    stmt = select(User).where(User.email == email)
    existing = db.execute(stmt).scalar_one_or_none()
    if existing is not None:
        raise ValueError("Email already registered")

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=UserRole.CUSTOMER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
