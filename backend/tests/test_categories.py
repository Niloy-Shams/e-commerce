
import pytest
from fastapi import status

from app.models.category import Category
from app.schemas.category import CategoryCreate


def test_list_categories_public(client, category):
    response = client.get("/api/v1/categories")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == category.name


def test_get_category_public(client, category):
    response = client.get(f"/api/v1/categories/{category.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == category.name


def test_get_category_not_found(client):
    response = client.get("/api/v1/categories/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_category_requires_admin(client):
    response = client.post("/api/v1/categories", json={"name": "New Cat"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_category_admin_success(client, auth_headers_admin):
    payload = CategoryCreate(name="Admin Category", description="Created by admin").model_dump()
    response = client.post("/api/v1/categories", json=payload, headers=auth_headers_admin)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Admin Category"


def test_create_duplicate_category_admin_returns_400(client, auth_headers_admin, category):
    payload = CategoryCreate(name=category.name).model_dump()
    response = client.post("/api/v1/categories", json=payload, headers=auth_headers_admin)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_category_requires_admin(client, category):
    response = client.put(f"/api/v1/categories/{category.id}", json={"name": "Updated"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_category_admin_success(client, auth_headers_admin, category):
    response = client.put(
        f"/api/v1/categories/{category.id}",
        json={"name": "Updated Category"},
        headers=auth_headers_admin,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Category"


def test_delete_category_requires_admin(client, category):
    response = client.delete(f"/api/v1/categories/{category.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_category_with_products_blocked(client, auth_headers_admin, category, product):
    response = client.delete(f"/api/v1/categories/{category.id}", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "products" in response.json()["detail"].lower()


def test_delete_category_admin_success(client, auth_headers_admin, db_session):
    cat = Category(name="Deletable", description="Will be deleted")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    response = client.delete(f"/api/v1/categories/{cat.id}", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_204_NO_CONTENT
