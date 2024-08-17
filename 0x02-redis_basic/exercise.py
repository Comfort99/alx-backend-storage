#!/usr/bin/env python3
""" Redis Model """
import redis
import uuid
from typing import Any, Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorator to count the number of times Cache is called """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ Boolean function
         that increament the count for this method """
        key = method.__qualname__

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the input and output
     history of Cache """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ Get qualied name of the method """
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable) -> Callable:
    """ Displays the history of calls
     to a particular function """
    fx_name = method.__qualname__
    inputs_key = f"{fx_name}:inputs"
    outputs_key = f"{fx_name}:outputs"

    redis_instance = method.__self__._redis
    if not isinstance(redis_instance, redis.Redis):
        return

    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    """ Display the history of calls """
    print(f"{fx_name} was called {len(inputs)} times")
    for input_args, output in zip(inputs, outputs):
        print(f"{fx_name}(*{input_args.decode('utf-8')}) -> \
              {output.decode('utf-8')}")


class Cache:
    """ Cache Class  """

    def __init__(self) -> None:
        """ Method that initialize the Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate redom key using uuid and store the data
         in Redis using the geberated Key """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)

        return data_key

    def get(self, key, fn: Callable = None) -> Union[str, bytes, int, float]:
        """ Method to Retrieve data from Redis
        Storage and convert it readable format """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """ retrieve data as a string """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ retrieve data as a intiger """
        return self.get(key, lambda d: int(d))
