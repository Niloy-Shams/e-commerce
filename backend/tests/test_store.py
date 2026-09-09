
import pytest
from fastapi import status


def test_get_store_settings_public(client, store_settings):
    response = client.get("/api/v1/store/settings")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["store_name"] == store_settings.store_name
    assert data["whatsapp_number"] == store_settings.whatsapp_number


def test_get_store_settings_returns_defaults_when_none(client, db_session):
    from app.models.store_settings import StoreSettings

    db_session.query(StoreSettings).delete()
    db_session.commit()
    response = client.get("/api/v1/store/settings")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["store_name"] == "My Store"
