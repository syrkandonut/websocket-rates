import asyncio

from aiohttp.web import Request, WebSocketResponse, WSMsgType
from aiohttp import WSCloseCode

from dishka.integrations.aiohttp import FromDishka, inject

from app.integrations.consts import Currency
from app.integrations.exceptions import CurrencyClientError
from app.utils import currency as utils

from .manager import WebSocketManager
from .consts import PathParam
from .exceptions import WebSocketException


async def _listen(websocket: WebSocketResponse):
    EXIT_COMMAND: str = 'exit'

    try:
        async for msg in websocket:
            if msg.type == WSMsgType.TEXT:
                if msg.data.lower().strip() == EXIT_COMMAND:
                    await websocket.close(code=WSCloseCode.OK)
                    break

    except asyncio.CancelledError:
        raise
    finally:
        if not websocket.closed:
            await websocket.close()


@inject
async def websocket_handler(
    request: Request,
    manager: FromDishka[WebSocketManager],
) -> WebSocketResponse:
    websocket = WebSocketResponse()
    await websocket.prepare(request)

    path_currency = request.match_info.get(PathParam.CURRENCY)
    currency = utils.verify_currency(path_currency) if path_currency else Currency.USD

    if not currency:
        await websocket.close(
            code=WebSocketException.CURRENCY_NOT_FOUND,
            message=WebSocketException.CURRENCY_NOT_FOUND.name.encode(),
        )
        return websocket

    try:
        await manager.connect(currency, websocket)
        await _listen(websocket)
    except CurrencyClientError as e:
        await websocket.close(
            code=WebSocketException.INTERNAL_API_ERROR,
            message=(WebSocketException.INTERNAL_API_ERROR.name + f':{e}').encode(),
        )
    except asyncio.CancelledError:
        raise
    finally:
        await manager.disconnect(currency, websocket)

    return websocket
