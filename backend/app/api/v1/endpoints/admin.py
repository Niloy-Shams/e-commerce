"""
TODO (feature/admin): implement per IMPLEMENTATION_PLAN.md sections 12 and 14.

All routes here require Depends(require_admin).

  GET   /admin/orders
  GET   /admin/orders/{id}
  PATCH /admin/orders/{id}/status   - validate status transitions
                                       (e.g. block CANCELLED -> normal flow)
  PUT   /admin/store/settings
"""

from fastapi import APIRouter

router = APIRouter()
