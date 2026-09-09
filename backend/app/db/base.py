"""
Import this module from alembic/env.py and from application startup
to ensure all SQLAlchemy models are registered on Base.metadata.

Individual model files must still import Base from here, but this module
itself does NOT import model classes to avoid circular imports.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
