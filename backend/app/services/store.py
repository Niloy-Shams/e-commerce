
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

from app.models.store_settings import StoreSettings


DEFAULT_STORE_SETTINGS = {
    "store_name": "My Store",
    "description": "",
    "logo_url": "",
    "banner_url": "",
    "primary_color": "#000000",
    "secondary_color": "#FFFFFF",
    "contact_email": "",
    "contact_phone": "",
    "whatsapp_number": "",
    "address": "",
    "singleton_key": "default",
}


def get_store_settings(db: Session) -> StoreSettings:
    stmt = select(StoreSettings).where(StoreSettings.singleton_key == "default")
    settings = db.execute(stmt).scalar_one_or_none()
    if settings is None:
        settings = StoreSettings(**DEFAULT_STORE_SETTINGS)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def update_store_settings(db: Session, **kwargs) -> StoreSettings:
    settings = get_store_settings(db)
    for key, value in kwargs.items():
        if value is not None and hasattr(settings, key):
            setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings
