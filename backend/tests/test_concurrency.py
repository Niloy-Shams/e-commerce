
import asyncio
import pytest
from fastapi import status

from app.models.order import OrderStatus


@pytest.mark.asyncio
async def test_concurrent_order_creation_only_one_succeeds(client, customer, product, db_session):
    import httpx

    product.stock = 1
    db_session.commit()
    db_session.refresh(product)

    from app.main import app

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        login_resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "customer@example.com", "password": "password123"},
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "items": [{"product_id": product.id, "quantity": 1}],
            "shipping_name": "Test",
            "shipping_phone": "555",
            "shipping_address": "Addr",
        }

        responses = await asyncio.gather(
            ac.post("/api/v1/orders", json=payload, headers=headers),
            ac.post("/api/v1/orders", json=payload, headers=headers),
        )

    status_codes = sorted([r.status_code for r in responses])
    assert status_codes == [201, 409]

    from app.models.product import Product as ProdModel
    from app.models.order import Order

    db_session.expire_all()
    refreshed = db_session.get(ProdModel, product.id)
    assert refreshed.stock == 0

    order_count = db_session.query(Order).count()
    assert order_count == 1


def test_cancel_order_restores_stock(client, auth_headers_admin, order, db_session):
    from app.models.product import Product

    product = db_session.get(Product, order.items[0].product_id)
    initial_stock = product.stock

    response = client.patch(
        f"/api/v1/admin/orders/{order.id}/status",
        json={"status": OrderStatus.CANCELLED.value},
        headers=auth_headers_admin,
    )
    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(product)
    assert product.stock == initial_stock + order.items[0].quantity
