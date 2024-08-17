#!/usr/bin/env python3
""" API """
import requests
import redis
from typing import Callable
from functools import wraps


redis_store = redis.Redis()
""" Redis client """


def data_cacher(method: Callable) -> Callable:
    """ Caches the output of fetched data.
    """
    @wraps(method)
    def invoker(url) -> str:
        """ The wrapper function for caching the output.
        """
        redis_store.incr(f'count:{url}')

        """get the cached content"""
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')

        """fetch the content if not cached"""
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@Cache_count
def get_page(url: str) -> str:
    """ get the HTML """
    return requests.get(url).text
