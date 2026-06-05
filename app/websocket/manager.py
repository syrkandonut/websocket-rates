from aiohttp.web import WebSocketResponse

from app.integrations.client import CurrencyClient
from app.integrations.consts import Currency

from .group import CurrencyGroup


class WebSocketManager:
    def __init__(self, client: CurrencyClient):
        self.client = client
        self.groups: dict[Currency, CurrencyGroup] = dict()

    async def connect(self, currency: Currency, websocket: WebSocketResponse) -> None:
        if currency not in self.groups:
            self.groups[currency] = CurrencyGroup(currency, self.client)

        await self.groups[currency].join(websocket)

    async def disconnect(
        self, currency: Currency, websocket: WebSocketResponse
    ) -> None:
        if group := self.groups.get(currency):
            await group.leave(websocket)
            if not group.websockets:
                del self.groups[currency]
