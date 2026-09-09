
import math
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductSort


def _apply_sort(query, sort: ProductSort):
    if sort == ProductSort.PRICE_ASC:
        return query.order_by(Product.price.asc())
    if sort == ProductSort.PRICE_DESC:
        return query.order_by(Product.price.desc())
    if sort == ProductSort.NEWEST:
        return query.order_by(Product.created_at.desc())
    if sort == ProductSort.NAME_ASC:
        return query.order_by(Product.name.asc())
    if sort == ProductSort.NAME_DESC:
        return query.order_by(Product.name.desc())
    return query


def list_products(
    db: Session,
    *,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    sort: ProductSort = ProductSort.NEWEST,
    page: int = 1,
    limit: int = 12,
) -> tuple[List[Product], int, int]:
    query = select(Product).where(Product.stock > 0)

    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    if category_id is not None:
        query = query.where(Product.category_id == category_id)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)

    query = _apply_sort(query, sort)

    count_query = select(func.count()).select_from(query.subquery())
    total = db.execute(count_query).scalar_one()

    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    items = db.execute(query).scalars().all()

    pages = max(1, math.ceil(total / limit)) if total > 0 else 1
    return list(items), int(total), pages


def get_product(db: Session, product_id: int) -> Optional[Product]:
    stmt = select(Product).where(Product.id == product_id)
    return db.execute(stmt).scalar_one_or_none()
