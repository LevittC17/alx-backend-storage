#!/usr/bin/env python3

'''
Main file
'''


import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Decorator to count how many times a method is called

    :param method: The method to be decorated
    :return: Decorated method
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Get the qualified name of the method as key'''
        key = method.__qualname__

        # Increment the count for the key in Redis
        self._redis.incr(key)

        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    def __init__(self):
        '''
        Cache class to interact with Redis
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Store data in Redis and return the key

        :param data: Data to be stored (str, bytes, int or float)
        :return: Randomly generated key used for storage
        '''
        key = str(uuid.uuid4())
        if isinstance(data, (str, bytes, int, float)):
            self._redis.set(key, data)
            return key
        else:
            raise ValueError('Data must be str, bytes, int, or float')

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float,
                                                          None]:
        '''
        Get data from Redis and optionally convert it using a callable

        :param key: Key to retrieve data from Redis
        :param fn: Callable to convert the data (optionally)
        :return: Retrieved and optionally converted data
        '''
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        '''
        Get a string from Redis

        :param key: Key to retrieve a string from Redis
        :return: Retrieved string or None
        '''
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        '''
        Get an intefer from Redis

        :param key: Key to retrieve an integer from Redis
        :return: Retrieved integer or None
        '''
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

    cache.store(b'first')
    print(cache.get(cache.store.__qualname__))

    cache.store(b'second')
    cache.store(b'third')
    print(cache.get(cache.store.__qualname__))
