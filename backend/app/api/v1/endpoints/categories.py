
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter()


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    stmt = select(Category).order_by(Category.name.asc())
    categories = db.execute(stmt).scalars().all()
    return [
        CategoryOut(
            id=c.id,
            name=c.name,
            description=c.description,
            created_at=c.created_at.isoformat() if c.created_at else "",
            updated_at=c.updated_at.isoformat() if c.updated_at else "",
        )
        for c in categories
    ]


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    stmt = select(Category).where(Category.id == category_id)
    category = db.execute(stmt).scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return CategoryOut(
        id=category.id,
        name=category.name,
        description=category.description,
        created_at=category.created_at.isoformat() if category.created_at else "",
        updated_at=category.updated_at.isoformat() if category.updated_at else "",
    )


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    stmt = select(Category).where(Category.name == payload.name)
    existing = db.execute(stmt).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    category = Category(name=payload.name, description=payload.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return CategoryOut(
        id=category.id,
        name=category.name,
        description=category.description,
        created_at=category.created_at.isoformat() if category.created_at else "",
        updated_at=category.updated_at.isoformat() if category.updated_at else "",
    )


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    stmt = select(Category).where(Category.id == category_id)
    category = db.execute(stmt).scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if payload.name is not None:
        category.name = payload.name
    if payload.description is not None:
        category.description = payload.description

    db.commit()
    db.refresh(category)
    return CategoryOut(
        id=category.id,
        name=category.name,
        description=category.description,
        created_at=category.created_at.isoformat() if category.created_at else "",
        updated_at=category.updated_at.isoformat() if category.updated_at else "",
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    stmt = select(Category).where(Category.id == category_id)
    category = db.execute(stmt).scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    from app.models.product import Product

    product_count_stmt = select(Product).where(Product.category_id == category_id)
    has_products = db.execute(product_count_stmt).first() is not None
    if has_products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with associated products",
        )

    db.delete(category)
    db.commit()
    return None
