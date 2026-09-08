"""
TODO (feature/products): implement per IMPLEMENTATION_PLAN.md section 10.

Public:
  GET /products     - search, category_id, min_price, max_price, sort, page, limit
  GET /products/{id}

Admin only (Depends(require_admin)):
  POST   /products
  PUT    /products/{id}
  DELETE /products/{id}

Validate everything on the backend even though the frontend also validates.
"""

from fastapi import APIRouter

router = APIRouter()
