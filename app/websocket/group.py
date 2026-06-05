import asyncio

from random import randint

from aiohttp.web import WebSocketResponse

from app.integrations.client import CurrencyClient
from app.integrations.consts import Currency
from app.websocket.consts import get_random_name
from app.config import get_settings


class CurrencyGroup:
    MATCHED_CURRENCIES_RATE: float = 1.0

    def __init__(self, currency: Currency, client: CurrencyClient) -> None:
        self.currency: Currency = currency
        self.to_currency: Currency = get_settings().rate.currency
        self.client: CurrencyClient = client

        self.websockets: set[WebSocketResponse] = set()
        self.websockets_names: dict[WebSocketResponse, str] = dict()

        self.task: asyncio.Task | None = None

    @staticmethod
    async def _time_volatility():
        MIN_VOLATILITY = 5
        MAX_VOLATILITY = 10

        await asyncio.sleep(delay=randint(MIN_VOLATILITY, MAX_VOLATILITY))

    async def join(self, websocket: WebSocketResponse) -> None:
        self.websockets.add(websocket)
        if self.task is None or self.task.done():
            self.task = asyncio.create_task(self._run_task())

    async def leave(self, websocket: WebSocketResponse) -> None:
        if self.websockets_names.get(websocket):
            del self.websockets_names[websocket]

        self.websockets.remove(websocket)
        if not self.websockets and self.task:
            self.task.cancel()
            self.task = None

    def _get_count_message(self, websocket: WebSocketResponse):
        observers = len(self.websockets)
        match observers:
            case 1:
                self.websockets_names[websocket] = get_random_name()
                return '👁 Only you are watching'

            case _:
                diff = len(self.websockets) - len(self.websockets_names)

                if diff > 0:
                    if websocket not in self.websockets_names:
                        self.websockets_names[websocket] = get_random_name()

                other_names = [
                    name
                    for ws, name in self.websockets_names.items()
                    if ws != websocket
                ]

                return (
                    f'👁 You and {observers - 1} more are watching:<br>'
                    + '<br>'.join(other_names)
                )

    async def _broadcast_count_observers(self):
        while self.websockets:
            for websocket in self.websockets:
                if not websocket.closed:
                    await websocket.send_str(self._get_count_message(websocket))

            await asyncio.sleep(delay=3)

    async def _send_rate(self, rate: float) -> None:
        message: str = f'Rate {self.currency}: {rate}'
        for websocket in self.websockets:
            if not websocket.closed:
                await websocket.send_str(message)

    async def _sync_original_rate(self) -> None:
        if self.currency == self.to_currency:
            rate = self.MATCHED_CURRENCIES_RATE
        else:
            rate = await self.client.exchange_rate(self.currency)

        await self._send_rate(rate)
        await self._time_volatility()

    async def _broadcast_volatile_rate(self) -> None:
        await self._sync_original_rate()

        while self.websockets:
            if self.currency == self.to_currency:
                rate = self.MATCHED_CURRENCIES_RATE
            else:
                rate = await self.client.exchange_volatile_rate(self.currency)

            await self._send_rate(rate)
            await self._time_volatility()

    async def _run_task(self) -> None:
        try:
            await asyncio.gather(
                self._broadcast_count_observers(),
                self._broadcast_volatile_rate(),
            )

        except asyncio.CancelledError:
            raise
