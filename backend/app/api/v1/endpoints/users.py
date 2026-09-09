
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.schemas.user import UserPublic as DetailedUserPublic

router = APIRouter()


@router.get("/customers", response_model=list[DetailedUserPublic])
def list_customers(db: Session = Depends(get_db), _=Depends(require_admin)):
    from app.models.user import User

    stmt = select(User).order_by(User.created_at.desc())
    users = db.execute(stmt).scalars().all()
    return [
        DetailedUserPublic(
            id=str(u.id),
            name=u.name,
            email=u.email,
            role=u.role.value,
            created_at=u.created_at.isoformat() if u.created_at else "",
        )
        for u in users
    ]


@router.get("/customers/{user_id}", response_model=DetailedUserPublic)
def get_customer(user_id: str, db: Session = Depends(get_db), _=Depends(require_admin)):
    from app.models.user import User

    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return DetailedUserPublic(
        id=str(user.id),
        name=user.name,
        email=user.email,
        role=user.role.value,
        created_at=user.created_at.isoformat() if user.created_at else "",
    )
