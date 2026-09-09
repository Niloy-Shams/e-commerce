
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductSort(str, Enum):
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    NEWEST = "newest"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    price: Decimal = Field(ge=0)
    stock: int = Field(ge=0)
    image_url: str | None = Field(default=None)
    category_id: int
    is_featured: bool = Field(default=False)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None)
    price: Decimal | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
    image_url: str | None = Field(default=None)
    category_id: int | None = Field(default=None)
    is_featured: bool | None = Field(default=None)


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    image_url: str | None
    category_id: int
    is_featured: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    items: List[ProductOut]
    page: int
    limit: int
    total: int
    pages: int
