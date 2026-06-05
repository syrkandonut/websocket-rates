from dataclasses import dataclass

from app.integrations.consts import Currency

from .utils import load_config


@dataclass(frozen=True, slots=True)
class RateConfig:
    currency: Currency


def get_rate_config() -> RateConfig:
    currency: Currency = load_config()['rate']['currency']

    return RateConfig(
        currency=currency,
    )
