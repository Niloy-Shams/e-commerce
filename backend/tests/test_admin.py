
import pytest
from fastapi import status

from app.models.order import OrderStatus
from app.schemas.store_settings import StoreSettingsUpdate


def test_list_admin_orders_requires_admin(client, order, auth_headers_customer):
    response = client.get("/api/v1/admin/orders", headers=auth_headers_customer)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_admin_orders_admin_success(client, auth_headers_admin, order):
    response = client.get("/api/v1/admin/orders", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


def test_get_admin_order_requires_admin(client, order, auth_headers_customer):
    response = client.get(f"/api/v1/admin/orders/{order.id}", headers=auth_headers_customer)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_admin_order_success(client, auth_headers_admin, order):
    response = client.get(f"/api/v1/admin/orders/{order.id}", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(order.id)


def test_update_order_status_valid_transition(client, auth_headers_admin, order, db_session):
    response = client.patch(
        f"/api/v1/admin/orders/{order.id}/status",
        json={"status": OrderStatus.CONFIRMED.value},
        headers=auth_headers_admin,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == OrderStatus.CONFIRMED.value


def test_update_order_status_invalid_transition_returns_400(client, auth_headers_admin, order, db_session):
    order.status = OrderStatus.CANCELLED
    db_session.commit()
    response = client.patch(
        f"/api/v1/admin/orders/{order.id}/status",
        json={"status": OrderStatus.CONFIRMED.value},
        headers=auth_headers_admin,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_store_settings_requires_admin(client):
    response = client.put("/api/v1/admin/store/settings", json={"store_name": "New Name"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_store_settings_admin_success(client, auth_headers_admin, store_settings):
    payload = StoreSettingsUpdate(store_name="Updated Store", whatsapp_number="8801712345678").model_dump()
    response = client.put("/api/v1/admin/store/settings", json=payload, headers=auth_headers_admin)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["store_name"] == "Updated Store"
