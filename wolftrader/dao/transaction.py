from util.logger import *
from util.database import DBFactory


class TransactionDAO:
    class_name = __file__

    def __init__(self, kind=None):
        try:
            self.repository = DBFactory(kind=kind).get_db()
            log_info('{} | TransactionDAO has been initialized successfully.'.format(TransactionDAO.class_name))
        except Exception as transaction_history_dao_error:
                log_critical('{} | TransactionDAO initialization has failed, price_history_dao_error: {}.'
                             .format(TransactionDAO.class_name, transaction_history_dao_error))

    def insert_transaction(self, record):
        sql = 'INSERT INTO TRANSACTION_HISTORY' \
              '(TYPE, AMOUNT, PRICE_AT, SPOT_PRICE, BUY_PRICE, SELL_PRICE, GAIN) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?)'
        self.repository.write(sql, record, TransactionDAO.class_name)

    def get_transactions(self):
        sql = 'SELECT TRANSACTION_DATE, TYPE, AMOUNT, PRICE_AT, SPOT_PRICE, BUY_PRICE, SELL_PRICE ' \
              'FROM TRANSACTION_HISTORY ORDER BY TRANSACTION_DATE'
        return self.repository.read(sql, TransactionDAO.class_name)

    def get_n_transactions_of_type(self, type, num_records):
        sql = f"SELECT TOP {num_records} TRANSACTION_DATE, TYPE, AMOUNT, PRICE_AT, SPOT_PRICE, BUY_PRICE, SELL_PRICE " \
              f"FROM TRANSACTION_HISTORY WHERE TYPE = '{type}' ORDER BY TRANSACTION_DATE DESC, ID DESC"
        return self.repository.read(sql, TransactionDAO.class_name)
