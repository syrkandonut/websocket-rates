import random

from http import HTTPStatus

from aiohttp import ClientSession

from app.config import get_settings

from .consts import Currency
from .cache import ttl_rate

from . import exceptions as exc


class CurrencyClient:
    ROUND_TO_DIGITS: int = 4

    def __init__(self, session: ClientSession):
        self.session = session
        self.base_url = get_settings().resource.api
        self.to_currency: Currency = get_settings().rate.currency

    def make_inaccuracy_rate(self, rate) -> float:
        MIN_INACCURACY: int = 0
        MAX_INACCURACY: int = 100

        inaccuracy: float = random.randint(MIN_INACCURACY, MAX_INACCURACY) / 10000
        value_with_inaccuracy: float = round(rate + inaccuracy, self.ROUND_TO_DIGITS)

        return value_with_inaccuracy

    def prepare_rate(self, rate: float) -> float:
        value: float = round(rate, self.ROUND_TO_DIGITS)

        return value

    def make_url(self, currency: Currency) -> str:
        return self.base_url + currency

    @ttl_rate()
    async def exchange_rate(
        self,
        currency: Currency,
    ) -> float:
        async with self.session.get(url=self.make_url(currency)) as response:
            if response.status != HTTPStatus.OK:
                raise exc.IncorrectStatusCode(response.status)

            response_json = await response.json()
            rates = response_json.get('rates')
            if not rates:
                raise exc.IncorrectResponse('No rates')

            rate: float = rates[self.to_currency]

            return self.prepare_rate(rate)

    async def exchange_volatile_rate(
        self,
        currency: Currency,
    ) -> float:
        rate = await self.exchange_rate(currency)
        return self.make_inaccuracy_rate(rate=rate)
