"""
TODO (feature/auth): implement per IMPLEMENTATION_PLAN.md section 8.

POST /register  - create user, hash password, never return password/hash
POST /login      - verify password, return access_token + token_type + user
GET  /me         - return the authenticated user (Depends(get_current_user))
"""

from fastapi import APIRouter

router = APIRouter()
