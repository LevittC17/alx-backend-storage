#!/usr/bin/env python3

"""
Main file
"""


import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


class RedisCache:
    """
    A class for interacting with a Redis data storage.
    This class allows storing, retrieving, and replaying method calls.

    Attributes:
        _redis (redis.Redis): A Redis client to manage data storage.
    """

    def __init__(self):
        """
        Initialize a new RedisCache instance.
        It creates a connection to Redis and clears the existing database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return a unique key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: A unique key used for data retrieval.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            transform_fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis by key.

        Args:
            key (str): The key used to retrieve the data.
            transform_fn (Callable, optional): A transformation function
            to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float]: The retrieved data, optionally
            transformed by transform_fn.
        """
        data = self._redis.get(key)
        return transform_fn(data) if transform_fn is not None else data

    def get_string(self, key: str) -> str:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key used to retrieve the data.

        Returns:
            str: The retrieved string value.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_integer(self, key: str) -> int:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key used to retrieve the data.

        Returns:
            int: The retrieved integer value.
        """
        return self.get(key, lambda x: int(x))

    def _increment_call_count(self, method: Callable):
        """
        Increment the call count for a method in Redis.

        Args:
            method (Callable): The method being called.
        """
        self._redis.incr(method.__qualname__)

    def _store_input_history(self, method: Callable, args: tuple):
        """
        Store the input arguments for a method in Redis.

        Args:
            method (Callable): The method being called.
            args (tuple): The input arguments for the method.
        """
        in_key = f'{method.__qualname__}:inputs'
        self._redis.rpush(in_key, str(args))

    def _store_output_history(self, method: Callable, output: Any):
        """
        Store the output for a method in Redis.

        Args:
            method (Callable): The method being called.
            output (Any): The output of the method.
        """
        out_key = f'{method.__qualname__}:outputs'
        self._redis.rpush(out_key, output)


def count_calls(method: Callable) -> Callable:
    """
    A decorator that tracks the number of calls made to a method
    in a RedisCache class.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method that increments call count.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._increment_call_count(method)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that tracks the call details of a method in a
    RedisCache class.

    Args:
        method (Callable): The method to be decorated.

    Returns:
    Callable: The decorated method that stores input and output history.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._store_input_history(method, args)
        output = method(self, *args, **kwargs)
        self._store_output_history(method, output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
    Display the call history of a method in a RedisCache class.

    Args:
        fn (Callable): The method for which to display the call history.
    """
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return

    fxn_name = fn.__qualname__
    fxn_call_count = redis_store.get(fxn_name)
    if fxn_call_count is None:
        return

    fxn_call_count = int(fxn_call_count)
