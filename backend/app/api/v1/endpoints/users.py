"""
TODO (feature/admin): implement per IMPLEMENTATION_PLAN.md section 13.

GET /admin/customers       - admin only, list customers (no password hashes)
GET /admin/customers/{id}  - admin only, single customer detail
"""

from fastapi import APIRouter

router = APIRouter()
