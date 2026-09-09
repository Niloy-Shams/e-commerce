from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemIn]
    shipping_name: str = Field(min_length=1)
    shipping_phone: str = Field(min_length=1)
    shipping_address: str = Field(min_length=1)


class OrderItemOut(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: Decimal


class OrderOut(BaseModel):
    id: str
    user_id: str
    total_amount: Decimal
    shipping_name: str
    shipping_phone: str
    shipping_address: str
    status: str
    expires_at: datetime | None
    items: List[OrderItemOut]
    created_at: datetime
    updated_at: datetime


class OrderStatusUpdate(BaseModel):
    status: str
