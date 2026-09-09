
import pytest
from fastapi import status

from app.core.security import hash_password
from app.models.user import User, UserRole
from app.schemas.order import OrderItemIn


def test_create_order_requires_auth(client):
    response = client.post("/api/v1/orders", json={"items": [], "shipping_name": "A", "shipping_phone": "B", "shipping_address": "C"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_order_success(client, auth_headers_customer, product):
    payload = {
        "items": [{"product_id": product.id, "quantity": 1}],
        "shipping_name": "Test Customer",
        "shipping_phone": "555-1234",
        "shipping_address": "123 Main St",
    }
    response = client.post("/api/v1/orders", json=payload, headers=auth_headers_customer)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["status"] == "PENDING"
    assert float(data["total_amount"]) == float(product.price)


def test_create_order_insufficient_stock_returns_409(client, auth_headers_customer, product):
    payload = {
        "items": [{"product_id": product.id, "quantity": product.stock + 1}],
        "shipping_name": "Test",
        "shipping_phone": "555",
        "shipping_address": "Addr",
    }
    response = client.post("/api/v1/orders", json=payload, headers=auth_headers_customer)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Insufficient stock" in response.json()["detail"]


def test_create_order_invalid_product_returns_409(client, auth_headers_customer):
    payload = {
        "items": [{"product_id": 9999, "quantity": 1}],
        "shipping_name": "Test",
        "shipping_phone": "555",
        "shipping_address": "Addr",
    }
    response = client.post("/api/v1/orders", json=payload, headers=auth_headers_customer)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_list_orders_returns_own_orders(client, auth_headers_customer, order):
    response = client.get("/api/v1/orders", headers=auth_headers_customer)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == str(order.id)


def test_get_order_owner_can_view(client, auth_headers_customer, order):
    response = client.get(f"/api/v1/orders/{order.id}", headers=auth_headers_customer)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(order.id)


def test_get_order_other_user_denied(client, auth_headers_customer, db_session, order):
    other = User(
        name="Other",
        email="other@example.com",
        password_hash=hash_password("password123"),
        role=UserRole.CUSTOMER,
    )
    db_session.add(other)
    db_session.commit()
    db_session.refresh(other)
    csrf_resp = client.get("/api/v1/auth/csrf")
    csrf_token = csrf_resp.json()["csrf_token"]
    login = client.post(
        "/api/v1/auth/login",
        json={"email": other.email, "password": "password123"},
        headers={"X-CSRF-Token": csrf_token},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    response = client.get(f"/api/v1/orders/{order.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_order_requires_auth(client, order):
    response = client.get(f"/api/v1/orders/{order.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
