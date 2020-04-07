from util.logger import *
from util.database import DBFactory


class TransactionDAO:
    class_name = __file__

    def __init__(self, kind=None):
        try:
            self.repository = DBFactory(kind=kind).get_db()
            log_info('{} | TransactionDAO has been initialized successfully.'.format(TransactionDAO.class_name))
        except Exception as price_history_dao_error:
                log_critical('{} | TransactionDAO initialization has failed, price_history_dao_error: {}.'.format(TransactionDAO.class_name, price_history_dao_error))

    def insert_transaction(self, record):
        sql = 'INSERT INTO PRICE_HISTORY' \
          '(BUY_PRICE, BUY_PRICE_CURRENCY, ' \
          'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
          'SELL_PRICE, SELL_PRICE_CURRENCY) ' \
          'VALUES(?,?,?,?,?,?)'
        self.repository.write(sql, record, TransactionDAO.class_name)

    def get_transactions(self):
        sql = 'SELECT EXTRACTION_DATE, BUY_PRICE, BUY_PRICE_CURRENCY, ' \
              'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
              'SELL_PRICE, SELL_PRICE_CURRENCY ' \
              'FROM PRICE_HISTORY ORDER BY EXTRACTION_DATE'
        return self.repository.read(sql, TransactionDAO.class_name)

    def get_n_transactions(self, num_records):
        sql = f'SELECT EXTRACTION_DATE, BUY_PRICE, BUY_PRICE_CURRENCY, ' \
              f'SPOT_PRICE, SPOT_PRICE_CURRENCY, ' \
              f'SELL_PRICE, SELL_PRICE_CURRENCY ' \
              f'FROM PRICE_HISTORY ORDER BY EXTRACTION_DATE LIMIT {num_records}'
        return self.repository.read(sql, TransactionDAO.class_name)
