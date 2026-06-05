import asyncio
import time

from aiohttp.web import middleware, Request, Response, HTTPException

from ..api.logs import http_logger, ws_logger


async def log_request(request: Request) -> None:
    http_logger.info(
        '| [%s] %s',
        request.method,
        request.path,
    )

    if request.can_read_body:
        request_body = await request.text()
        http_logger.info(
            '|→ %s',
            request_body,
        )


async def log_response(response: Response, duration: float) -> None:
    if not isinstance(response, Response) or not response.body:
        return None

    http_logger.info(
        '|← %s',
        response.body.decode()[:200],
    )
    http_logger.info(
        '└' + 20 * '─' + '[%s]' + 20 * '─' + '[%.4fs]',
        f'{response.status} {response.reason}',
        duration,
    )


async def log_ws_request(request: Request) -> None:
    ws_logger.info(
        '| [WS CONNECTING] %s - %s',
        request.path,
        request.remote,
    )


async def log_ws_response(request: Request) -> None:
    ws_logger.info(
        '| [WS CLOSED] %s - %s',
        request.path,
        request.remote,
    )


async def get_response(request: Request, handler) -> Response:
    try:
        return await handler(request)
    except HTTPException as e:
        return e


@middleware
async def http_logger_middleware(request: Request, handler):
    start_time = time.perf_counter()

    is_websocket = request.headers.get('Upgrade', '').lower() == 'websocket'
    if is_websocket:
        await log_ws_request(request=request)
    else:
        await log_request(request=request)

    duration = time.perf_counter() - start_time

    response: Response = await get_response(request=request, handler=handler)

    if is_websocket:
        asyncio.create_task(log_ws_response(request=request))
    else:
        await log_response(response=response, duration=duration)

    return response
