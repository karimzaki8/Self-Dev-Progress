"""Initial product catalog and user data for the electronics store."""

from electronics_store.models.product import Product
from electronics_store.models.user import User


def get_initial_products() -> list[Product]:
    return [
        Product(name="Laptop", price=999.99, stock=50),
        Product(name="Smartphone", price=699.99, stock=120),
        Product(name="Tablet", price=449.99, stock=75),
        Product(name="Headphones", price=149.99, stock=200),
        Product(name="Smartwatch", price=249.99, stock=90),
        Product(name="Keyboard", price=79.99, stock=150),
        Product(name="Mouse", price=49.99, stock=180),
        Product(name="Monitor", price=329.99, stock=40),
        Product(name="Speaker", price=89.99, stock=110),
        Product(name="Camera", price=549.99, stock=35),
        Product(name="Printer", price=199.99, stock=60),
        Product(name="Router", price=69.99, stock=95),
    ]


def get_users() -> list[User]:
    return [
        User(username="admin", password="admin123", display_name="Administrator"),
        User(username="user", password="user123", display_name="Customer"),
        User(username="guest", password="guest123", display_name="Guest User"),
    ]
