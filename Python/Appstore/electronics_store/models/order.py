"""Completed order record."""

from dataclasses import dataclass, field
from datetime import datetime

from electronics_store.models.cart import CartItem


@dataclass
class Order:
    items: list[CartItem]
    delivery_method: str
    currency: str
    service_charge: float
    subtotal: float
    total: float
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
