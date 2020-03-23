from util.logger import *
from util.database import SQLiteUtil, SQLServerUtil


class IndicatorsDAO(SQLServerUtil):
    class_name = __file__

    def __init__(self):
        try:
            SQLServerUtil.__init__(self)
            log_info('{} | IndicatorsDAO has been initialized successfully.'.format(IndicatorsDAO.class_name))
        except Exception as indicators_dao_error:
            log_critical('{} | IndicatorsDAO initialization has failed, indicators_dao_error: {}.'.format(IndicatorsDAO.class_name, indicators_dao_error))

    def get_indicators(self):
        sql = 'SELECT CALCULATION_DATE, SPOT_PRICE, BUY_PRICE, ' \
              'SELL_PRICE, MA24, UPPER_BOLLINGER, LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI FROM INDICATORS ORDER BY CALCULATION_DATE ASC'
        return super().read(sql, IndicatorsDAO.class_name)

    def insert_indicator(self, indicator):
        sql = 'INSERT INTO INDICATORS(CALCULATION_DATE, MA24, UPPER_BOLLINGER, ' \
              'LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI)' \
              'VALUES(?, ?, ?, ?, ?, ?, ?)'
        super().write(sql, indicator, IndicatorsDAO.class_name)

    def insert_indicators(self, indicators):
        sql = 'INSERT OR IGNORE INTO INDICATORS(CALCULATION_DATE, SPOT_PRICE, BUY_PRICE, ' \
              'SELL_PRICE, MA24, UPPER_BOLLINGER, LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        super().write_many(sql, indicators, IndicatorsDAO.class_name)