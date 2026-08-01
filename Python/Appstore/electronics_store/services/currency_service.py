"""Currency conversion utilities."""

from electronics_store.config.constants import CURRENCY_RATES, DEFAULT_CURRENCY, CURRENCY_SYMBOLS


class CurrencyService:
    @staticmethod
    def convert(amount_usd: float, target_currency: str) -> float:
        rate = CURRENCY_RATES.get(target_currency.upper(), CURRENCY_RATES[DEFAULT_CURRENCY])
        return amount_usd * rate

    @staticmethod
    def get_rate(currency: str) -> float:
        return CURRENCY_RATES.get(currency.upper(), CURRENCY_RATES[DEFAULT_CURRENCY])

    @staticmethod
    def get_symbol(currency: str) -> str:
        return CURRENCY_SYMBOLS.get(currency.upper(), "$")

    @staticmethod
    def available_currencies() -> list[str]:
        return list(CURRENCY_RATES.keys())
