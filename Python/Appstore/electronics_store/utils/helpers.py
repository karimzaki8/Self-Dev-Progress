"""Miscellaneous utility functions."""

import random
import string

from electronics_store.config.constants import CURRENCY_SYMBOLS


def generate_verification_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


def format_price(amount: float, currency: str = "USD") -> str:
    symbol = CURRENCY_SYMBOLS.get(currency, "$")
    return f"{symbol}{amount:,.2f}"
