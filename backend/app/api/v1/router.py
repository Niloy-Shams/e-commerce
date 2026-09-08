from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, categories, orders, products, store, users

api_router = APIRouter()


@api_router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """IMPLEMENTATION_PLAN.md section 7.1 - GET /api/v1/health -> {"status": "ok"}"""
    return {"status": "ok"}


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/admin", tags=["admin-customers"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(store.router, prefix="/store", tags=["store"])
