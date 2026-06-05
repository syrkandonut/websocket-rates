from http import HTTPStatus

from aiohttp.web import Request, Response

from dishka.integrations.aiohttp import FromDishka, inject

from app.integrations.consts import Currency
from app.integrations.client import CurrencyClient
from app.integrations.exceptions import CurrencyClientError
from app.utils import currency as utils

from . import responses as resp

from .consts import PathParam


@inject
async def get_exchange_rate(
    request: Request, currency_client: FromDishka[CurrencyClient]
) -> Response:
    path_currency = request.match_info.get(PathParam.CURRENCY)
    currency = utils.verify_currency(path_currency) if path_currency else Currency.USD

    if not currency:
        return resp.ExchangeRateFailed(
            currency=path_currency,
            status=HTTPStatus.NOT_FOUND,
        ).response()

    try:
        rate = await currency_client.exchange_rate(currency=currency)
    except CurrencyClientError as e:
        return resp.ExchangeRateFailed(
            currency=path_currency,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            msg=f'Internal API Errors: {e}',
        ).response()

    return resp.ExchangeRateSuccess(
        currency=currency,
        rate=rate,
        status=HTTPStatus.OK,
    ).response()
