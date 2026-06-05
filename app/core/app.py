import logging

from aiohttp import web

from .middleware import http_logger_middleware
from .routes import routes
from .injection import inject

logging.basicConfig(level=logging.INFO)


def create_app():
    web_app = web.Application(middlewares=[http_logger_middleware])
    web_app.add_routes(routes)

    inject(web_app)

    return web_app
