from dishka import Provider, Scope, provide

from app.integrations.client import CurrencyClient
from app.websocket.manager import WebSocketManager


class WSManagerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_ws_manager(self, client: CurrencyClient) -> WebSocketManager:
        return WebSocketManager(client=client)
