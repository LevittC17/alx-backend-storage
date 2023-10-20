#!/usr/bin/env python3

'''
Main file
'''


import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        '''
        Cache class to interact with Redis
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Store data in Redis and return the key
        '''
        key = str(uuid.uuid4())
        if isinstance(data, (str, bytes, int, float)):
            self._redis.set(key, data)
            return key
        else:
            raise ValueError('Data must be str, bytes, int, or float')
