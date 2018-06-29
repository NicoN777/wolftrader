from ..util.logger import *
from wolftrader.util.database import DatabaseUtil

class PriceHistoryDAO(DatabaseUtil):
    class_name = __file__
    def __init__(self):
        try:
            DatabaseUtil.__init__(self)
            log_info('{} | PriceHistoryDAO has been initialized successfully.'.format(PriceHistoryDAO.class_name))
        except Exception as error:
            log_critical('{} | PriceHistory initialization has failed, error: {}.'.format(PriceHistoryDAO.class_name, error))

    @property
    def insert_price_record(self, record):
        sql = 'INSERT INTO '