#!/usr/bin/python3
""" API """
import requests
import redis
from typing import Callable
from functools import wraps


redis_store = redis.Redis()
""" Redis client """


def Cache_count(method: Callable) -> Callable:
    """ Decorator to cache the page content and count URL accesses """
    @wraps(method)
    def invoke(url) -> str:
        """ Wrapper function for caching the output data"""

        """ check for cached content """
        cached_page = redis_store.get(f"cached:{url}")
        if cached_page:
            return cached_page.decode('utf-8')

        html_content = method(url)
        """ get the content """

        redis_store.setex(f"cached:{url}", 10, html_content)
        """ Cache the content with expiration """

        redis_store.incr(f"count:{url}")
        """Incr the access count """

        return html_content
    return invoke


@Cache_count
def get_page(url: str) -> str:
    """ get the HTML """
    return requests.get(url).text
