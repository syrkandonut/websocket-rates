from app.core import create_app
from aiohttp import web

from app.config import get_settings


settings = get_settings()


if __name__ == '__main__':
    web.run_app(
        create_app(),
        host=settings.server.host,
        port=settings.server.port,
    )
