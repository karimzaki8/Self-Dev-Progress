"""Input validation helpers."""

from electronics_store.config.constants import CURRENCY_RATES


def is_valid_quantity(value: str) -> tuple[bool, int]:
    try:
        qty = int(value)
        return qty > 0, qty
    except (ValueError, TypeError):
        return False, 0


def is_valid_currency(value: str) -> bool:
    return value.upper() in CURRENCY_RATES


def sanitize_currency(value: str) -> str:
    """Return a valid currency code, defaulting to USD for invalid input."""
    upper = value.strip().upper()
    if upper in CURRENCY_RATES:
        return upper
    return "USD"
