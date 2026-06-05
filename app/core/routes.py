from aiohttp import web

from app.api.currency import get_exchange_rate
from app.websocket.handler import websocket_handler


async def index(request):
    return web.FileResponse('./static/index.html')


routes = [
    web.get('/{currency}', index),
    web.get('/api/{currency}', get_exchange_rate),
    web.get('/ws/{currency}', websocket_handler),
]
