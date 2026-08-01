"""Shopping cart model managing selected products and pricing."""

from dataclasses import dataclass, field

from electronics_store.config.constants import (
    DISCOUNT_STEP,
    DISCOUNT_RATE_PER_STEP,
    MAX_DISCOUNT_RATE,
    DELIVERY_CHARGE,
    PICKUP_CHARGE,
    CURRENCY_RATES,
    DEFAULT_CURRENCY,
)


@dataclass
class CartItem:
    product_name: str
    unit_price: float
    quantity: int
    discount_rate: float
    discounted_total: float


class Cart:
    def __init__(self) -> None:
        self.items: list[CartItem] = []
        self.delivery_method: str = "delivery"
        self.currency: str = DEFAULT_CURRENCY

    @staticmethod
    def calculate_discount_rate(quantity: int) -> float:
        steps = quantity // DISCOUNT_STEP
        rate = steps * DISCOUNT_RATE_PER_STEP
        return min(rate, MAX_DISCOUNT_RATE)

    def add_item(self, product_name: str, unit_price: float, quantity: int) -> CartItem:
        discount_rate = self.calculate_discount_rate(quantity)
        subtotal = unit_price * quantity
        discounted_total = subtotal * (1 - discount_rate)

        item = CartItem(
            product_name=product_name,
            unit_price=unit_price,
            quantity=quantity,
            discount_rate=discount_rate,
            discounted_total=discounted_total,
        )
        self.items.append(item)
        return item

    def remove_item(self, index: int) -> None:
        if 0 <= index < len(self.items):
            self.items.pop(index)

    @property
    def subtotal(self) -> float:
        return sum(item.discounted_total for item in self.items)

    @property
    def service_charge(self) -> float:
        if self.delivery_method == "delivery":
            return DELIVERY_CHARGE
        return PICKUP_CHARGE

    @property
    def total_usd(self) -> float:
        return self.subtotal + self.service_charge

    @property
    def total_in_currency(self) -> float:
        rate = CURRENCY_RATES.get(self.currency, CURRENCY_RATES[DEFAULT_CURRENCY])
        return self.total_usd * rate

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0

    def clear(self) -> None:
        self.items.clear()
        self.delivery_method = "delivery"
        self.currency = DEFAULT_CURRENCY
