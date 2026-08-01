"""Store service — catalog management, stock, and order processing."""

from electronics_store.models.product import Product
from electronics_store.models.cart import Cart, CartItem
from electronics_store.models.order import Order
from electronics_store.data.store_data import get_initial_products


class StoreService:
    def __init__(self) -> None:
        self._products: list[Product] = get_initial_products()
        self._cart = Cart()
        self._orders: list[Order] = []

    @property
    def products(self) -> list[Product]:
        return self._products

    @property
    def cart(self) -> Cart:
        return self._cart

    @property
    def orders(self) -> list[Order]:
        return self._orders

    def find_product(self, name: str) -> Product | None:
        name_lower = name.strip().lower()
        for p in self._products:
            if p.name.lower() == name_lower:
                return p
        return None

    def add_to_cart(self, product_name: str, quantity: int) -> tuple[bool, str, CartItem | None]:
        product = self.find_product(product_name)
        if product is None:
            return False, f"Product '{product_name}' not found in the catalog.", None
        if not product.is_available(quantity):
            return (
                False,
                f"Insufficient stock for '{product.name}'. "
                f"Only {product.stock} unit(s) available.",
                None,
            )
        item = self._cart.add_item(product.name, product.price, quantity)
        return True, f"Added {quantity}× {product.name} to cart.", item

    def remove_from_cart(self, index: int) -> None:
        self._cart.remove_item(index)

    def checkout(self) -> Order:
        """Finalize the order: reduce stock, record order, clear cart."""
        for item in self._cart.items:
            product = self.find_product(item.product_name)
            if product:
                product.reduce_stock(item.quantity)

        order = Order(
            items=list(self._cart.items),
            delivery_method=self._cart.delivery_method,
            currency=self._cart.currency,
            service_charge=self._cart.service_charge,
            subtotal=self._cart.subtotal,
            total=self._cart.total_in_currency,
        )
        self._orders.append(order)
        self._cart.clear()
        return order

    def reset_catalog(self) -> None:
        self._products = get_initial_products()
