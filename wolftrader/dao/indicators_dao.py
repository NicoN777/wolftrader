from wolftrader.util.logger import *
from wolftrader.util.database import DatabaseUtil

class IndicatorsDAO(DatabaseUtil):
    class_name = __file__

    def __init__(self):
        try:
            DatabaseUtil.__init__(self)
            log_info('{} | IndicatorsDAO has been initialized successfully.'.format(IndicatorsDAO.class_name))
        except Exception as indicators_dao_error:
            log_critical('{} | IndicatorsDAO initialization has failed, indicators_dao_error: {}.'.format(IndicatorsDAO.class_name, indicators_dao_error))

    def get_indicators(self):
        try:
            sql = 'SELECT CALCULATION_DATE, SPOT_PRICE, BUY_PRICE, ' \
                  'SELL_PRICE, MA24, UPPER_BOLLINGER, LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI FROM INDICATORS'
            cursor = DatabaseUtil.cursor.execute(sql)
            column_names = list(map(lambda x: x[0], cursor.description))
            data = {'column_names': column_names, 'records': cursor.fetchall()}
            log_info('{} | get_indicators(), SQL = {}, executed successfully'.format(IndicatorsDAO.class_name, sql))
            return data
        except Exception as indicators_dao_error:
            log_critical('{} error while executing {}\n Error: {}'.format(IndicatorsDAO.class_name, sql, indicators_dao_error))

    def insert_indicator(self, indicator):
        try:
            sql = 'INSERT INTO INDICATORS(CALCULATION_DATE, MA24, UPPER_BOLLINGER, ' \
                  'LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI)' \
                  'VALUES(?, ?, ?, ?, ?, ?, ?)'
            DatabaseUtil.cursor.execute(sql, indicator)
            log_info('{} successful, SQL = {} | record = {} '.format(IndicatorsDAO.class_name, sql, indicator))
            print('about to exit')
        except Exception as indicators_dao_error:
            log_critical('{}, indicators_dao_error while executing {}\n Error: {}'.format(IndicatorsDAO.class_name, sql, indicators_dao_error))
            print('I errored: {}'.format(indicators_dao_error))

    def insert_indicators(self, indicators):
        try:
            sql = 'INSERT OR IGNORE INTO INDICATORS(CALCULATION_DATE, SPOT_PRICE, BUY_PRICE, ' \
                  'SELL_PRICE, MA24, UPPER_BOLLINGER, LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI) ' \
                  'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            DatabaseUtil.cursor.executemany(sql, indicators)
            log_info('{} successful, SQL = {} '.format(IndicatorsDAO, sql))
        except Exception as indicators_dao_error:
            log_critical('{}, indicators_dao_error while executing {}\n Error: {}'.format(IndicatorsDAO.class_name, indicators_dao_error))
