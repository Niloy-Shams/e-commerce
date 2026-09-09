
import os

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/ecommerce")

import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.base import Base
from app.models.category import Category
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.store_settings import StoreSettings
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest

settings = get_settings()

_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def _create_tables():
    Base.metadata.create_all(bind=_engine)


def _drop_tables():
    Base.metadata.drop_all(bind=_engine)


def _clear_tables():
    with _engine.connect() as conn:
        transaction = conn.begin()
        try:
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(text(f"TRUNCATE TABLE {table.name} CASCADE"))
            transaction.commit()
        except Exception:
            transaction.rollback()
            raise


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    _create_tables()
    yield
    _drop_tables()


@pytest.fixture(autouse=True)
def clean_tables():
    _clear_tables()
    yield


@pytest.fixture()
def client() -> TestClient:
    from app.main import app

    return TestClient(app)


@pytest.fixture()
def db_session():
    session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def customer(db_session):
    user = User(
        name="Test Customer",
        email="customer@example.com",
        password_hash=hash_password("password123"),
        role=UserRole.CUSTOMER,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def admin(db_session):
    user = User(
        name="Test Admin",
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def category(db_session):
    cat = Category(name="Electronics", description="Electronic devices")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    return cat


@pytest.fixture()
def product(db_session, category):
    product = Product(
        name="Test Product",
        description="A test product",
        price=10.00,
        stock=10,
        category_id=category.id,
        is_featured=False,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture()
def product_out_of_stock(db_session, category):
    product = Product(
        name="Out of Stock Product",
        description="No stock",
        price=5.00,
        stock=0,
        category_id=category.id,
        is_featured=False,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture()
def order(db_session, customer, product):
    order = Order(
        user_id=customer.id,
        total_amount=product.price,
        shipping_name="Test Customer",
        shipping_phone="1234567890",
        shipping_address="123 Test St",
        status=OrderStatus.PENDING,
    )
    db_session.add(order)
    db_session.flush()
    item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=1,
        price=product.price,
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(order)
    return order


@pytest.fixture()
def auth_headers_customer(client, customer):
    csrf_resp = client.get("/api/v1/auth/csrf")
    csrf_token = csrf_resp.json()["csrf_token"]
    response = client.post(
        "/api/v1/auth/login",
        json={"email": customer.email, "password": "password123"},
        headers={"X-CSRF-Token": csrf_token},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    new_csrf = response.cookies.get("csrf_token", csrf_token)
    return {"Authorization": f"Bearer {token}", "X-CSRF-Token": new_csrf}


@pytest.fixture()
def auth_headers_admin(client, admin):
    csrf_resp = client.get("/api/v1/auth/csrf")
    csrf_token = csrf_resp.json()["csrf_token"]
    response = client.post(
        "/api/v1/auth/login",
        json={"email": admin.email, "password": "admin123"},
        headers={"X-CSRF-Token": csrf_token},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    new_csrf = response.cookies.get("csrf_token", csrf_token)
    return {"Authorization": f"Bearer {token}", "X-CSRF-Token": new_csrf}


@pytest.fixture()
def store_settings(db_session):
    settings = StoreSettings(
        store_name="Test Store",
        description="A test store",
        primary_color="#000000",
        secondary_color="#FFFFFF",
        whatsapp_number="8801712345678",
        singleton_key="default",
    )
    db_session.add(settings)
    db_session.commit()
    db_session.refresh(settings)
    return settings
