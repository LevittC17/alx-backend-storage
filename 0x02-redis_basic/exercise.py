#!/usr/bin/env python3

"""
Main file
"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for
    a function

    :param method: The method to be Decorated
    :return: The decorated method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Get the qualified name of the method"""
        key = method.__qualname__

        # Store the input arguments as a string in Redis
        input_key = f'{key}:inputs'
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        output_key = f'{key}:output'
        self._redis.rpush(output_key, output)

        return output

    return wrapper


class Cache:
    def __init__(self):
        """Cache class to interact with Redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key

        :param data: Data to be stored (str, bytes, int or float)
        :return: Randomly generated key used for storage
        """
        key = str(uuid.uuid4())
        if isinstance(data, (str, bytes, int, float)):
            self._redis.set(key, data)
            return key
        else:
            raise ValueError('Data must be str, bytes, int or float')

    @property
    def redis(self):
        return self._redis


def replay(func: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    key = func.__qualname__
    inputs = cache.redis.lrange(f'{key}:inputs', 0, -1)
    outputs = cache.redis.lrange(f'{key}:outputs', 0, -1)

    if inputs:
        print(f'{key} was called {len(inputs)} times:')
        for input_args, output in zip(inputs, outputs):
            # Convert the string back to a tuple
            input_args = eval(input_args.decode('utf-8'))
            print(f"{key}(*{input_args}) -> {output.decode('utf-8')}")


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store('foo')
    s2 = cache.store('bar')
    s3 = cache.store(42)

    replay(cache.store)
