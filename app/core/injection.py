from dishka import make_async_container
from dishka.integrations.aiohttp import setup_dishka, AiohttpProvider

from aiohttp.web import Application

from app.providers import APIProvider, WSManagerProvider, HttpClientProvider


def inject(web_app: Application):
    container = make_async_container(
        HttpClientProvider(),
        APIProvider(),
        WSManagerProvider(),
        AiohttpProvider(),
    )

    setup_dishka(container, web_app, auto_inject=True)
