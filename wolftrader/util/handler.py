from functools import wraps, partial
from util.logger import *


def exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except Exception as e:
            print(f'Error while executing with {args}, {kwargs}\n Error: {e}')
            # raise e
    return wrapper


@exception
def add(a,b):
    return a + b

@exception
def divide(a,b):
    return a//b

@exception
def outter(a,b):
    aplusb = add(a,b)
    aplusbplus5 = add(aplusb, 5)
    nope = divide(aplusbplus5, 0)
    return nope
