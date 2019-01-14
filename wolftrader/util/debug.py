import logging
from wolftrader.application import log_file, log_format, log_level
from functools import partial, wraps

logging.basicConfig(filename=log_file, format=log_format, level=log_level)

def debug(func=None, *, prefix=''):
    if func is None:
        return partial(debug, prefix=prefix)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func)
        logger.debug(f'{func.__qualname}, Arguments: {args}, KeywordArgs: {kwargs}')
        val = func(*args, **kwargs)
        return val
    return wrapper


def debugclassmethods(cls):
    for name, value in vars(cls).items():
        if callable(value):
            setattr(cls, name, debug(value))



