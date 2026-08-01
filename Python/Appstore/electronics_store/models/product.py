"""Product model representing an electronics item in the catalog."""

from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float  # base price in USD
    stock: int

    def is_available(self, quantity: int = 1) -> bool:
        return self.stock >= quantity

    def reduce_stock(self, quantity: int) -> None:
        if not self.is_available(quantity):
            raise ValueError(
                f"Cannot reduce stock by {quantity}: only {self.stock} available"
            )
        self.stock -= quantity
