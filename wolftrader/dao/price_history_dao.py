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

    def insert_price_record(self, record):
        try:
            sql = 'INSERT INTO PRICE_HISTORY' \
              '(BUY_PRICE, BUY_PRICE_CURRENCY, ' \
              'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
              'SELL_PRICE, SELL_PRICE_CURRENCY) ' \
              'VALUES(?,?,?,?,?,?)'
            DatabaseUtil.cursor.execute(sql, record)
            log_info('{} successful, SQL = {} | record = {} '.format(PriceHistoryDAO.class_name, sql, record))
        except Exception as error:
            log_critical('{} error while executing {}\n Error: {}'.format(PriceHistoryDAO.class_name, sql, error))

    def get_price_records(self):
        try:
            sql = 'SELECT BUY_PRICE, BUY_PRICE_CURRENCY, ' \
                  'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
                  'SELL_PRICE, SELL_PRICE_CURRENCY ' \
                  'FROM PRICE_HISTORY'
            cursor = DatabaseUtil.cursor.execute(sql)
            column_names = list(map(lambda x: x[0], cursor.description))
            data = {'column_names': column_names, 'records': cursor.fetchall()}
            return data
        except Exception as error:
            log_critical('{} error while executing {}\n Error: {}'.format(PriceHistoryDAO.class_name, sql, error))

