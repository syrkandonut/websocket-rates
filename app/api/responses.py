import orjson

from dataclasses import dataclass

from http import HTTPStatus

from aiohttp.web import Response

from app.integrations.consts import Currency

from .consts import ContentType


class APIResponse:
    def _as_response(
        self,
        data: dict,
        status: HTTPStatus,
        content_type: ContentType = ContentType.JSON,
    ) -> Response:
        return Response(
            body=orjson.dumps(data),
            status=status,
            content_type=content_type,
        )


@dataclass(slots=True, frozen=True)
class ExchangeRateFailed(APIResponse):
    currency: str | None
    status: HTTPStatus
    msg: str = 'CURRENCY_NOT_FOUND'

    def response(self) -> Response:
        data = {
            f'CURRENCY_{self.currency}': self.msg,
        }

        return self._as_response(data, self.status)


@dataclass(slots=True, frozen=True)
class ExchangeRateSuccess(APIResponse):
    currency: Currency
    rate: int | float
    status: HTTPStatus

    def response(self) -> Response:
        data = {
            f'CURRENCY_{self.currency}': self.rate,
        }

        return self._as_response(data, self.status)
