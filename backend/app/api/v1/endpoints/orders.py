"""
TODO (feature/orders): implement per IMPLEMENTATION_PLAN.md section 11.

Customer (Depends(require_customer)):
  POST /orders      - validate products, verify stock, price from DB (never
                       trust frontend price/total/user_id), create Order +
                       OrderItems, decrease stock, all in one transaction
  GET  /orders       - only the current user's own orders
  GET  /orders/{id}  - only if it belongs to the current user (or is admin)
"""

from fastapi import APIRouter

router = APIRouter()
