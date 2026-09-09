import pytest
from sqlalchemy import inspect

from app.models.order import Order
from app.models.store_settings import StoreSettings


def test_store_settings_has_whatsapp_number():
    mapper = inspect(StoreSettings)
    assert "whatsapp_number" in mapper.columns
    column = mapper.columns["whatsapp_number"]
    assert not column.nullable
    assert str(column.type) == "VARCHAR"


def test_store_settings_has_singleton_key_unique():
    mapper = inspect(StoreSettings)
    assert "singleton_key" in mapper.columns
    column = mapper.columns["singleton_key"]
    assert column.unique is True
    assert column.default is not None


def test_order_has_expires_at():
    mapper = inspect(Order)
    assert "expires_at" in mapper.columns
    column = mapper.columns["expires_at"]
    assert column.nullable is True
