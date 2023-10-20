#!/usr/bin/env python3

'''
Main file
'''


import redis
import uuid
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    '''
    Decorator to store the history of inputs and outputs for
    a function

    :param method: The method to be decorated
    :return: Decorated method
    '''
    @wraps(method)
    def wrapper(self, *args, **Kwargs):
        '''Get the qualified name of the method'''
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
        '''Cache class to interact with Redis'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
            raise ValueError('Data must be str, bytes, int or float')


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store('first')
    print(s1)
    s2 = cache.store('second')
    print(s2)
    s3 = cache.store('third')
    print(s3)

    inputs = cache._redis.lrange(f'{cache.store.__qualnamr__}:inputs', 0, -1)
    outputs = cache._redis.lrange(f'{cache.store.__qualname__}:outputs', 0, -1)

    print('inputs: {}'.format(inputs))
    print('outputs: {}'.format(outputs))
