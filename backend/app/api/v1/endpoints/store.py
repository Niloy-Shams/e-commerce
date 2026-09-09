
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services import store as store_service

router = APIRouter()


@router.get("/settings")
def get_store_settings(db: Session = Depends(get_db)):
    settings = store_service.get_store_settings(db)
    return {
        "store_name": settings.store_name,
        "description": settings.description,
        "logo_url": settings.logo_url,
        "banner_url": settings.banner_url,
        "primary_color": settings.primary_color,
        "secondary_color": settings.secondary_color,
        "contact_email": settings.contact_email,
        "contact_phone": settings.contact_phone,
        "whatsapp_number": settings.whatsapp_number,
        "address": settings.address,
        "updated_at": settings.updated_at.isoformat() if settings.updated_at else "",
    }
