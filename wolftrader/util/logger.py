import logging
from ..application import log_format, log_level, log_file

try:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    def log_debug(message):
        logger.debug(message)

    def log_info(message):
        logger.info(message)

    def log_warning(message):
        logger.warning(message)

    def log_error(message):
        logger.error(message)

    def log_critical(message):
        logger.critical(message)
except Exception as error:
    print('There was an exception in logger.py, Error: {}'.format(error))