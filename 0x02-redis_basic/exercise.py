#!/usr/bin/env python3

"""
Main file
"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called

    :param method: The method to be Decorated
    :return: The decorated method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Get the qualified name of the method as key"""
        key = method.__qualname__

        # Increment the count for the key in Redis
        self._redis.incr(key)

        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


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


def replay(func: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    key = func.__qualname__
    inputs = cache._redis.lrange(f'{key}:inputs', 0, -1)
    outputs = cache._redis.lrange(f'{key}:outputs', 0, -1)

    if inputs:
        print(f'{key} was called {len(inputs)} times:')
        for input_args, output in zip(inputs, outputs):
            # Convert the string back to a tuple
            input_args = eval(input_args.decode('utf-8'))
            print(f"{key}(*{input_args}) -> {output.decode('utf-8')}")


class Cache:
    def __init__(self):
        """
        Cache class to interact with Redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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
            raise ValueError('Data must be str, bytes, int, or float')

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float,
                                                          None]:
        """
        Get data from Redis and optionally convert it using a callable

        :param key: Key to retrieve data from Redis
        :param fn: Callable to convert the data (optionally)
        :return: Retrieved and optionally converted data
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Get a string from Redis

        :param key: Key to retrieve a string from Redis
        :return: Retrieved string or None
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Get an integer from Redis

        :param key: Key to retrieve an integer from Redis
        :return: Retrieved integer or None
        """
        return self.get(key, fn=int)
