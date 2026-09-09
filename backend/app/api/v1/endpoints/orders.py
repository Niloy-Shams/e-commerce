
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin, require_customer
from app.models.user import User
from app.schemas.order import OrderCreate, OrderItemIn, OrderItemOut, OrderOut, OrderStatusUpdate
from app.services import order as order_service

router = APIRouter()


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        order = order_service.create_order(
            db,
            user_id=str(current_user.id),
            items=payload.items,
            shipping_name=payload.shipping_name,
            shipping_phone=payload.shipping_phone,
            shipping_address=payload.shipping_address,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return OrderOut(
        id=str(order.id),
        user_id=str(order.user_id),
        total_amount=order.total_amount,
        shipping_name=order.shipping_name,
        shipping_phone=order.shipping_phone,
        shipping_address=order.shipping_address,
        status=order.status.value,
        expires_at=order.expires_at,
        items=[
            OrderItemOut(
                product_id=oi.product_id,
                name="",
                quantity=oi.quantity,
                price=oi.price,
            )
            for oi in order.items
        ],
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(require_customer)):
    orders = order_service.list_orders_for_user(db, str(current_user.id))
    return [
        OrderOut(
            id=str(o.id),
            user_id=str(o.user_id),
            total_amount=o.total_amount,
            shipping_name=o.shipping_name,
            shipping_phone=o.shipping_phone,
            shipping_address=o.shipping_address,
            status=o.status.value,
            expires_at=o.expires_at,
            items=[
                OrderItemOut(
                    product_id=oi.product_id,
                    name="",
                    quantity=oi.quantity,
                    price=oi.price,
                )
                for oi in o.items
            ],
            created_at=o.created_at,
            updated_at=o.updated_at,
        )
        for o in orders
    ]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_customer)):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.user_id != current_user.id and current_user.role.value != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return OrderOut(
        id=str(order.id),
        user_id=str(order.user_id),
        total_amount=order.total_amount,
        shipping_name=order.shipping_name,
        shipping_phone=order.shipping_phone,
        shipping_address=order.shipping_address,
        status=order.status.value,
        expires_at=order.expires_at,
        items=[
            OrderItemOut(
                product_id=oi.product_id,
                name="",
                quantity=oi.quantity,
                price=oi.price,
            )
            for oi in order.items
        ],
        created_at=order.created_at,
        updated_at=order.updated_at,
    )
