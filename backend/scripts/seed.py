import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User, UserRole


def seed_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@example.com").first()
        if existing:
            print("Admin user already exists: admin@example.com")
            return

        admin = User(
            name="Admin",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Admin user created: {admin.email}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
