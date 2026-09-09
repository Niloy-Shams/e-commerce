
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderItemIn


ORDER_DEFAULT_EXPIRY_DAYS = 7


VALID_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
    OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
}


TERMINAL_STATES = (OrderStatus.CANCELLED, OrderStatus.DELIVERED)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _default_expires_at() -> datetime:
    return _now() + timedelta(days=ORDER_DEFAULT_EXPIRY_DAYS)


def create_order(
    db: Session,
    *,
    user_id: str,
    items: List[OrderItemIn],
    shipping_name: str,
    shipping_phone: str,
    shipping_address: str,
) -> Order:
    product_ids = sorted({item.product_id for item in items})

    products = []
    for pid in product_ids:
        stmt = select(Product).where(Product.id == pid).with_for_update()
        product = db.execute(stmt).scalar_one_or_none()
        if product is None:
            raise ValueError(f"Product {pid} not found")
        products.append(product)

    product_map = {p.id: p for p in products}

    total_amount = Decimal("0.00")
    order_items = []

    for item in items:
        product = product_map[item.product_id]
        if product.stock < item.quantity:
            raise ValueError(
                f"Insufficient stock for {product.name}. Available: {product.stock}, requested: {item.quantity}."
            )
        line_total = product.price * item.quantity
        total_amount += line_total
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price=product.price,
            )
        )

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        shipping_name=shipping_name,
        shipping_phone=shipping_phone,
        shipping_address=shipping_address,
        status=OrderStatus.PENDING,
        expires_at=_default_expires_at(),
    )
    db.add(order)

    for oi in order_items:
        oi.order = order
        db.add(oi)
        product_map[oi.product_id].stock -= oi.quantity

    db.commit()
    db.refresh(order)
    for oi in order.items:
        db.refresh(oi)
    return order


def get_order(db: Session, order_id: str) -> Optional[Order]:
    stmt = select(Order).where(Order.id == order_id)
    return db.execute(stmt).scalar_one_or_none()


def list_orders_for_user(db: Session, user_id: str) -> List[Order]:
    stmt = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def update_order_status(db: Session, order: Order, new_status: OrderStatus) -> Order:
    if order.status in TERMINAL_STATES:
        raise ValueError("Order is in a terminal state and cannot be modified")

    allowed = VALID_TRANSITIONS.get(order.status, [])
    if new_status not in allowed:
        raise ValueError(
            f"Invalid status transition from {order.status} to {new_status}"
        )

    if new_status == OrderStatus.CANCELLED:
        for oi in order.items:
            stmt = select(Product).where(Product.id == oi.product_id).with_for_update()
            product = db.execute(stmt).scalar_one_or_none()
            if product is not None:
                product.stock += oi.quantity

    order.status = new_status
    order.updated_at = _now()
    db.commit()
    db.refresh(order)
    return order
