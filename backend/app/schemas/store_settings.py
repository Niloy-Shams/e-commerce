import re

from pydantic import BaseModel, Field, field_validator


class StoreSettingsPublic(BaseModel):
    store_name: str
    description: str | None = None
    logo_url: str | None = None
    banner_url: str | None = None
    primary_color: str
    secondary_color: str
    contact_email: str | None = None
    contact_phone: str | None = None
    whatsapp_number: str
    address: str | None = None


class StoreSettingsUpdate(BaseModel):
    store_name: str | None = None
    description: str | None = None
    logo_url: str | None = None
    banner_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    whatsapp_number: str | None = None
    address: str | None = None

    @field_validator("whatsapp_number")
    @classmethod
    def validate_whatsapp(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not re.match(r"^\+?[1-9]\d{6,14}$", value):
            raise ValueError(
                "whatsapp_number must be in E.164 format, e.g. 8801712345678"
            )
        return value
