
import pytest
from fastapi import status

from app.schemas.auth import RegisterRequest


def test_register_creates_customer(client, db_session):
    payload = RegisterRequest(name="New User", email="newuser@example.com", password="securepass")
    response = client.post("/api/v1/auth/register", json=payload.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["name"] == "New User"
    assert data["user"]["role"] == "CUSTOMER"
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email_returns_400(client):
    payload = RegisterRequest(name="User", email="dup@example.com", password="pass123")
    client.post("/api/v1/auth/register", json=payload.model_dump())
    response = client.post("/api/v1/auth/register", json=payload.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already" in response.json()["detail"].lower()


def test_login_returns_token(client, customer):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": customer.email, "password": "password123"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user"]["email"] == customer.email
    assert "access_token" in data


def test_login_wrong_password_returns_401(client, customer):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": customer.email, "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_requires_auth(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_returns_user(client, auth_headers_customer, customer):
    response = client.get("/api/v1/auth/me", headers=auth_headers_customer)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == customer.email
    assert data["name"] == customer.name
    assert "created_at" in data
