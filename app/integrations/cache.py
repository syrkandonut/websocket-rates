import time

import asyncio

from functools import wraps


def ttl_rate(seconds: int = 100):
    def decorator(func):

        cache = {}
        lock = asyncio.Lock()

        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with lock:
                key = (args, frozenset(sorted(kwargs.items())))

                now = time.time()
                if key in cache:
                    value, timestamp = cache[key]
                    if now - timestamp < seconds:
                        return value

                value = await func(*args, **kwargs)

                cache[key] = (value, now)
                return value

        return wrapper

    return decorator
