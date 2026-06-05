import logging

logging.getLogger('aiohttp.access').setLevel(logging.WARNING)
logging.getLogger('aiohttp.server').setLevel(logging.WARNING)

http_logger = logging.getLogger('http_logger')
ws_logger = logging.getLogger('ws_logger')
