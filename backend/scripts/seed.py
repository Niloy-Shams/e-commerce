import os
import random
import sys
import uuid
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.category import Category
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.store_settings import StoreSettings
from app.models.user import User, UserRole

SAMPLE_CATEGORIES = [
    ("Electronics", "Electronic devices and gadgets"),
    ("Clothing", "Men's and women's fashion"),
    ("Home & Kitchen", "Home appliances and kitchenware"),
    ("Books", "Books and stationery"),
    ("Sports", "Sports equipment and accessories"),
]

SAMPLE_PRODUCTS = [
    ("Wireless Headphones", "High-quality wireless headphones", 59.99, 20, "Electronics", True),
    ("Smart Watch", "Fitness tracking smart watch", 129.99, 15, "Electronics", True),
    ("Laptop Stand", "Adjustable aluminum laptop stand", 39.99, 30, "Electronics", False),
    ("T-Shirt", "Cotton casual t-shirt", 19.99, 50, "Clothing", False),
    ("Jeans", "Denim jeans for men", 49.99, 25, "Clothing", False),
    ("Sneakers", "Running sneakers", 89.99, 10, "Clothing", True),
    ("Blender", "High-speed kitchen blender", 69.99, 12, "Home & Kitchen", False),
    ("Cookware Set", "Non-stick cookware set", 99.99, 8, "Home & Kitchen", True),
    ("Coffee Maker", "Programmable coffee maker", 79.99, 15, "Home & Kitchen", False),
    ("Novel", "Bestselling fiction novel", 14.99, 40, "Books", False),
    ("Notebook", "Hardcover ruled notebook", 9.99, 100, "Books", False),
    ("Yoga Mat", "Non-slip yoga mat", 29.99, 20, "Sports", False),
    ("Dumbbells", "Adjustable dumbbell set", 59.99, 10, "Sports", True),
]

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"
CUSTOMER_EMAIL = "customer@example.com"
CUSTOMER_PASSWORD = "password123"


def seed_users(db):
    admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if not admin:
        admin = User(
            name="Admin User",
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            role=UserRole.ADMIN,
        )
        db.add(admin)
        print(f"Created admin: {ADMIN_EMAIL}")
    else:
        print(f"Admin already exists: {ADMIN_EMAIL}")

    customer = db.query(User).filter(User.email == CUSTOMER_EMAIL).first()
    if not customer:
        customer = User(
            name="Test Customer",
            email=CUSTOMER_EMAIL,
            password_hash=hash_password(CUSTOMER_PASSWORD),
            role=UserRole.CUSTOMER,
        )
        db.add(customer)
        print(f"Created customer: {CUSTOMER_EMAIL}")
    else:
        print(f"Customer already exists: {CUSTOMER_EMAIL}")

    db.commit()
    return admin, customer


def seed_categories(db):
    category_map = {}
    for name, description in SAMPLE_CATEGORIES:
        category = db.query(Category).filter(Category.name == name).first()
        if not category:
            category = Category(name=name, description=description)
            db.add(category)
            db.commit()
            db.refresh(category)
            print(f"Created category: {name}")
        else:
            print(f"Category already exists: {name}")
        category_map[name] = category
    return category_map


def seed_products(db, category_map):
    for name, description, price, stock, category_name, featured in SAMPLE_PRODUCTS:
        existing = db.query(Product).filter(Product.name == name).first()
        if not existing:
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category_id=category_map[category_name].id,
                is_featured=featured,
            )
            db.add(product)
            print(f"Created product: {name}")
        else:
            print(f"Product already exists: {name}")
    db.commit()


def seed_store_settings(db):
    settings = db.query(StoreSettings).filter(StoreSettings.singleton_key == "default").first()
    if not settings:
        settings = StoreSettings(
            store_name="Demo Store",
            description="A sample e-commerce store",
            logo_url="https://via.placeholder.com/150",
            banner_url="https://via.placeholder.com/1200x300",
            primary_color="#2563eb",
            secondary_color="#ffffff",
            contact_email="support@demostore.com",
            contact_phone="8801712345678",
            whatsapp_number="8801712345678",
            address="123 Main Street, Dhaka, Bangladesh",
            singleton_key="default",
        )
        db.add(settings)
        db.commit()
        print("Created store settings")
    else:
        print("Store settings already exist")


def seed_orders(db, customer, products):
    existing_orders = db.query(Order).filter(Order.user_id == customer.id).count()
    if existing_orders > 0:
        print(f"Customer already has {existing_orders} order(s)")
        return

    statuses = [OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED]
    for _ in range(3):
        product = random.choice(products)
        quantity = random.randint(1, 3)
        total = product.price * quantity

        order = Order(
            user_id=customer.id,
            total_amount=total,
            shipping_name="Test Customer",
            shipping_phone="555-1234",
            shipping_address="123 Test Street",
            status=random.choice(statuses),
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price,
        )
        db.add(item)
        db.commit()
        print(f"Created order {order.id} for customer {customer.email}")
    db.commit()


def seed_all():
    db = SessionLocal()
    try:
        print("=== Seeding database ===")
        admin, customer = seed_users(db)
        category_map = seed_categories(db)
        seed_products(db, category_map)
        seed_store_settings(db)

        products = db.query(Product).all()
        if products:
            seed_orders(db, customer, products)

        print("=== Seeding completed ===")
        print("\nYou can now use the following credentials in Swagger UI:")
        print(f"Admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        print(f"Customer: {CUSTOMER_EMAIL} / {CUSTOMER_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
