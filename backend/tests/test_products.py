
import pytest
from fastapi import status

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductSort


def test_list_products_public(client, product):
    response = client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1
    assert data["limit"] == 12
    assert data["page"] == 1


def test_list_products_with_search(client, product):
    response = client.get("/api/v1/products", params={"search": product.name})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1
    assert data["items"][0]["name"] == product.name


def test_list_products_with_category_filter(client, product):
    response = client.get("/api/v1/products", params={"category_id": product.category_id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] >= 1


def test_list_products_pagination(client, product, db_session):
    for i in range(15):
        p = Product(name=f"Product {i}", price=1.00, stock=5, category_id=product.category_id)
        db_session.add(p)
    db_session.commit()
    response = client.get("/api/v1/products", params={"limit": 5, "page": 1})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["limit"] == 5
    assert data["total"] >= 16
    assert len(data["items"]) == 5


def test_list_products_sort_newest(client, product, db_session):
    from datetime import datetime, timezone

    old = Product(
        name="Old Product",
        price=1.00,
        stock=5,
        category_id=product.category_id,
        created_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )
    db_session.add(old)
    db_session.commit()
    response = client.get("/api/v1/products", params={"sort": ProductSort.NEWEST.value})
    assert response.status_code == status.HTTP_200_OK
    names = [p["name"] for p in response.json()["items"]]
    assert names[0] == product.name


def test_get_product_public(client, product):
    response = client.get(f"/api/v1/products/{product.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == product.name


def test_get_product_not_found(client):
    response = client.get("/api/v1/products/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_product_requires_admin(client):
    response = client.post("/api/v1/products", json={"name": "New", "price": 1, "stock": 1, "category_id": 1})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_product_admin_success(client, auth_headers_admin, category):
    payload = ProductCreate(
        name="Admin Product", description="Test", price=9.99, stock=10, category_id=category.id
    ).model_dump(mode="json")
    response = client.post("/api/v1/products", json=payload, headers=auth_headers_admin)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Admin Product"


def test_create_product_invalid_category_returns_400(client, auth_headers_admin):
    payload = ProductCreate(name="Bad", price=1, stock=1, category_id=9999).model_dump(mode="json")
    response = client.post("/api/v1/products", json=payload, headers=auth_headers_admin)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_product_admin_success(client, auth_headers_admin, product):
    response = client.put(
        f"/api/v1/products/{product.id}",
        json={"name": "Updated Product", "price": 15.00},
        headers=auth_headers_admin,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Product"
    assert float(response.json()["price"]) == 15.00


def test_delete_product_requires_admin(client, product):
    response = client.delete(f"/api/v1/products/{product.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_product_admin_success(client, auth_headers_admin, db_session, category):
    p = Product(name="To Delete", price=1, stock=1, category_id=category.id)
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    response = client.delete(f"/api/v1/products/{p.id}", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_204_NO_CONTENT
