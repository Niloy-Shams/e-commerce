
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_customer
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserPublic
from app.schemas.user import UserPublic as DetailedUserPublic
from app.services import auth as auth_service

router = APIRouter()


def _serialize_user(user) -> dict[str, Any]:
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
    }


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 7,
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        user = auth_service.register_user(
            db=db,
            name=payload.name,
            email=payload.email,
            password=payload.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    token = create_access_token(subject=str(user.id))
    _set_auth_cookie(response, token)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserPublic(**_serialize_user(user)),
    )


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=str(user.id))
    _set_auth_cookie(response, token)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserPublic(**_serialize_user(user)),
    )


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"detail": "Logged out"}


@router.get("/me", response_model=DetailedUserPublic)
def get_me(current_user=Depends(get_current_user)):
    return DetailedUserPublic(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.value,
        created_at=current_user.created_at.isoformat() if current_user.created_at else "",
    )
