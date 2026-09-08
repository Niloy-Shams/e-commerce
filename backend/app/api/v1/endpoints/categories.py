"""
TODO (feature/products): implement per IMPLEMENTATION_PLAN.md section 9.

Public:
  GET /categories
  GET /categories/{id}

Admin only (Depends(require_admin)):
  POST   /categories
  PUT    /categories/{id}
  DELETE /categories/{id}   - block deletion while products still reference it
"""

from fastapi import APIRouter

router = APIRouter()
