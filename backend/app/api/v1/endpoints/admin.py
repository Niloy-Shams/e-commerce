
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.models.order import Order, OrderStatus
from app.schemas.store_settings import StoreSettingsUpdate
from app.services import order as order_service
from app.services import store as store_service

router = APIRouter()


@router.get("/orders")
def list_admin_orders(db: Session = Depends(get_db), _=Depends(require_admin)):
    stmt = select(Order).order_by(Order.created_at.desc())
    orders = db.execute(stmt).scalars().all()
    return [
        {
            "id": str(o.id),
            "user_id": str(o.user_id),
            "total_amount": str(o.total_amount),
            "status": o.status.value,
            "created_at": o.created_at.isoformat() if o.created_at else "",
            "updated_at": o.updated_at.isoformat() if o.updated_at else "",
        }
        for o in orders
    ]


@router.get("/orders/{order_id}")
def get_admin_order(order_id: str, db: Session = Depends(get_db), _=Depends(require_admin)):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {
        "id": str(order.id),
        "user_id": str(order.user_id),
        "total_amount": str(order.total_amount),
        "shipping_name": order.shipping_name,
        "shipping_phone": order.shipping_phone,
        "shipping_address": order.shipping_address,
        "status": order.status.value,
        "expires_at": order.expires_at.isoformat() if order.expires_at else None,
        "items": [
            {
                "product_id": oi.product_id,
                "quantity": oi.quantity,
                "price": str(oi.price),
            }
            for oi in order.items
        ],
        "created_at": order.created_at.isoformat() if order.created_at else "",
        "updated_at": order.updated_at.isoformat() if order.updated_at else "",
    }


@router.patch("/orders/{order_id}/status")
def update_admin_order_status(
    order_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    new_status_str = payload.get("status")
    if new_status_str is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status is required")

    try:
        new_status = OrderStatus(new_status_str)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status") from exc

    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    try:
        updated = order_service.update_order_status(db, order, new_status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {
        "id": str(updated.id),
        "status": updated.status.value,
        "updated_at": updated.updated_at.isoformat() if updated.updated_at else "",
    }


@router.put("/store/settings")
def update_store_settings(
    payload: StoreSettingsUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    data = payload.model_dump(exclude_none=True)
    settings = store_service.update_store_settings(db, **data)
    return {
        "id": settings.id,
        "store_name": settings.store_name,
        "description": settings.description,
        "logo_url": settings.logo_url,
        "banner_url": settings.banner_url,
        "primary_color": settings.primary_color,
        "secondary_color": settings.secondary_color,
        "contact_email": settings.contact_email,
        "contact_phone": settings.contact_phone,
        "whatsapp_number": settings.whatsapp_number,
        "address": settings.address,
        "updated_at": settings.updated_at.isoformat() if settings.updated_at else "",
    }
