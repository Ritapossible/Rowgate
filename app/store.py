"""In-memory storage. Good enough for a demo service; reset between tests."""

ORDERS: dict[str, dict] = {}
INVOICES: dict[str, dict] = {}

PRICES_CENTS = {
    "KORA-TEE": 2500,
    "KORA-MUG": 1200,
    "KORA-CAP": 1800,
}
DEFAULT_PRICE_CENTS = 1000
CURRENCY = "USD"
TAX_RATE = 0.075


def reset() -> None:
    ORDERS.clear()
    INVOICES.clear()
