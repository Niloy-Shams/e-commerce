import pytest
from pydantic import ValidationError

from app.schemas.order import OrderCreate, OrderItemIn
from app.schemas.store_settings import StoreSettingsUpdate


def test_store_settings_update_accepts_valid_whatsapp():
    data = StoreSettingsUpdate(whatsapp_number="8801712345678")
    assert data.whatsapp_number == "8801712345678"


def test_store_settings_update_accepts_whatsapp_with_plus():
    data = StoreSettingsUpdate(whatsapp_number="+8801712345678")
    assert data.whatsapp_number == "+8801712345678"


def test_store_settings_update_rejects_invalid_whatsapp():
    with pytest.raises(ValidationError):
        StoreSettingsUpdate(whatsapp_number="not-a-phone-number")


def test_store_settings_update_rejects_empty_whatsapp():
    with pytest.raises(ValidationError):
        StoreSettingsUpdate(whatsapp_number="")


def test_order_item_in_rejects_zero_quantity():
    with pytest.raises(ValidationError):
        OrderItemIn(product_id=1, quantity=0)


def test_order_item_in_rejects_negative_quantity():
    with pytest.raises(ValidationError):
        OrderItemIn(product_id=1, quantity=-1)


def test_order_create_requires_shipping_fields():
    with pytest.raises(ValidationError):
        OrderCreate(items=[], shipping_name="", shipping_phone="", shipping_address="")
