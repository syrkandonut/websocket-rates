from app.integrations.consts import Currency


def verify_currency(currency: str) -> Currency | None:
    try:
        return Currency(currency.upper())
    except ValueError:
        return None
