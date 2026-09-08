"""
Import this module (not app.db.session) from alembic/env.py.

Every model must be imported below so that `Base.metadata` is complete and
`alembic revision --autogenerate` can detect all tables.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so they register themselves on Base.metadata.
from app.models.user import User  # noqa: E402,F401
from app.models.category import Category  # noqa: E402,F401
from app.models.product import Product  # noqa: E402,F401
from app.models.order import Order  # noqa: E402,F401
from app.models.order_item import OrderItem  # noqa: E402,F401
from app.models.store_settings import StoreSettings  # noqa: E402,F401
