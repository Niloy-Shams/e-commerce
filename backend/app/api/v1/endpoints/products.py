
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin, validate_csrf_token
from app.models.category import Category
from app.schemas.category import CategoryOut
from app.schemas.product import ProductCreate, ProductListResponse, ProductOut, ProductSort, ProductUpdate
from app.services import product as product_service

router = APIRouter()


@router.get("", response_model=ProductListResponse)
def list_products(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    sort: ProductSort = ProductSort.NEWEST,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
):
    items, total, pages = product_service.list_products(
        db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        page=page,
        limit=limit,
    )
    return ProductListResponse(
        items=[
            ProductOut(
                id=p.id,
                name=p.name,
                description=p.description,
                price=p.price,
                stock=p.stock,
                image_url=p.image_url,
                category_id=p.category_id,
                is_featured=p.is_featured,
                created_at=p.created_at or datetime.now(),
                updated_at=p.updated_at or datetime.now(),
            )
            for p in items
        ],
        page=page,
        limit=limit,
        total=total,
        pages=pages,
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductOut(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
        category_id=product.category_id,
        is_featured=product.is_featured,
        created_at=product.created_at or datetime.now(),
        updated_at=product.updated_at or datetime.now(),
    )


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), _=Depends(require_admin), __=Depends(validate_csrf_token)):
    category = db.get(Category, payload.category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")

    from app.models.product import Product

    product = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
        image_url=payload.image_url,
        category_id=payload.category_id,
        is_featured=payload.is_featured,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductOut(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
        category_id=product.category_id,
        is_featured=product.is_featured,
        created_at=product.created_at or datetime.now(),
        updated_at=product.updated_at or datetime.now(),
    )


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db), _=Depends(require_admin), __=Depends(validate_csrf_token)):
    from app.models.product import Product

    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if payload.category_id is not None:
        category = db.get(Category, payload.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")
        product.category_id = payload.category_id

    if payload.name is not None:
        product.name = payload.name
    if payload.description is not None:
        product.description = payload.description
    if payload.price is not None:
        product.price = payload.price
    if payload.stock is not None:
        product.stock = payload.stock
    if payload.image_url is not None:
        product.image_url = payload.image_url
    if payload.is_featured is not None:
        product.is_featured = payload.is_featured

    db.commit()
    db.refresh(product)
    return ProductOut(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
        category_id=product.category_id,
        is_featured=product.is_featured,
        created_at=product.created_at or datetime.now(),
        updated_at=product.updated_at or datetime.now(),
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(require_admin), __=Depends(validate_csrf_token)):
    from app.models.product import Product

    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()
    return None
