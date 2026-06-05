from typing import AsyncIterable

from dishka import Provider, Scope, provide

from aiohttp import ClientSession

from app.integrations.client import CurrencyClient


class HttpClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_session(self) -> AsyncIterable[ClientSession]:
        async with ClientSession(raise_for_status=True) as session:
            yield session


class APIProvider(Provider):
    @provide(scope=Scope.APP)
    def get_currency_client(self, session: ClientSession) -> CurrencyClient:
        return CurrencyClient(session=session)
