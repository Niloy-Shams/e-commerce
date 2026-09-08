"""
Reusable FastAPI dependencies.

get_db is ready to use immediately.

get_current_user / require_customer / require_admin are the three
dependencies named in IMPLEMENTATION_PLAN.md section 15. Their bodies are
intentionally left as TODOs: wiring them up needs the User model and the
auth endpoints (register/login), which belong to the `feature/auth`
branch/prompt rather than the Phase 1 scaffolding step. Implement them
together with app/api/v1/endpoints/auth.py.
"""

from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    TODO (feature/auth):
    1. Reject if token is missing -> 401.
    2. Decode token with app.core.security.decode_access_token -> 401 if invalid/expired.
    3. Load the User by id (token's "sub" claim) -> 401 if not found.
    4. Return the User.
    """
    raise NotImplementedError("Implement get_current_user in the auth feature branch.")


def require_customer(current_user=Depends(get_current_user)):
    """TODO (feature/auth): raise 403 unless current_user.role == CUSTOMER (or ADMIN, if admins should also act as customers)."""
    raise NotImplementedError("Implement require_customer in the auth feature branch.")


def require_admin(current_user=Depends(get_current_user)):
    """TODO (feature/auth): raise 403 unless current_user.role == ADMIN."""
    raise NotImplementedError("Implement require_admin in the auth feature branch.")
