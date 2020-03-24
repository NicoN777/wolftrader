from util.logger import *
from util.database import DBFactory


class PriceHistoryDAO:
    class_name = __file__

    def __init__(self, kind=None):
        try:
            self.repository = DBFactory(kind=kind).get_db()
            log_info('{} | PriceHistoryDAO has been initialized successfully.'.format(PriceHistoryDAO.class_name))
        except Exception as price_history_dao_error:
                log_critical('{} | PriceHistory initialization has failed, price_history_dao_error: {}.'.format(PriceHistoryDAO.class_name, price_history_dao_error))

    def insert_price_record(self, record):
        sql = 'INSERT INTO PRICE_HISTORY' \
          '(BUY_PRICE, BUY_PRICE_CURRENCY, ' \
          'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
          'SELL_PRICE, SELL_PRICE_CURRENCY) ' \
          'VALUES(?,?,?,?,?,?)'
        self.repository.write(sql, record, PriceHistoryDAO.class_name)

    def get_price_records(self):
        sql = 'SELECT EXTRACTION_DATE, BUY_PRICE, BUY_PRICE_CURRENCY, ' \
              'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
              'SELL_PRICE, SELL_PRICE_CURRENCY ' \
              'FROM PRICE_HISTORY ORDER BY EXTRACTION_DATE'
        return self.repository.read(sql, PriceHistoryDAO.class_name)

    def get_price_records_param(self, num_records):
        sql = f'SELECT EXTRACTION_DATE, BUY_PRICE, BUY_PRICE_CURRENCY, ' \
              f'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
              f'SELL_PRICE, SELL_PRICE_CURRENCY ' \
              f'FROM PRICE_HISTORY ORDER BY EXTRACTION_DATE LIMIT {num_records}'
        return self.repository.read(sql, PriceHistoryDAO.class_name)
