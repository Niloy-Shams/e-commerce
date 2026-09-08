from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class StoreSettings(Base):
    """
    Singleton-style table: for the MVP, exactly one row should exist.
    The backend should serve sensible defaults if no row exists yet
    (see IMPLEMENTATION_PLAN.md 6.6) - implement that fallback in the
    store service, not by relaxing this schema.
    """

    __tablename__ = "store_settings"

    id = Column(Integer, primary_key=True)
    store_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)
    primary_color = Column(String, nullable=False, default="#000000")
    secondary_color = Column(String, nullable=False, default="#FFFFFF")
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
