from functools import wraps, partial
from util.logger import *


def exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except Exception as e:
            log_error(f'Error while executing with {args}, {kwargs}\n Error: {e}')
    return wrapper

