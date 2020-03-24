from util.logger import *
from util.database import DBFactory


class IndicatorsDAO:
    class_name = __file__

    def __init__(self, kind=None):
        try:
            self.repository = DBFactory(kind=kind).get_db()
            log_info('{} | IndicatorsDAO has been initialized successfully.'.format(IndicatorsDAO.class_name))
        except Exception as indicators_dao_error:
            log_critical('{} | IndicatorsDAO initialization has failed, indicators_dao_error: {}.'.format(IndicatorsDAO.class_name, indicators_dao_error))

    def get_indicators(self):
        sql = 'SELECT CALCULATION_DATE, SPOT_PRICE, BUY_PRICE, ' \
              'SELL_PRICE, MA24, UPPER_BOLLINGER, LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI FROM INDICATORS ORDER BY CALCULATION_DATE ASC'
        return self.repository.read(sql, IndicatorsDAO.class_name)

    def insert_indicator(self, indicator):
        sql = 'INSERT INTO INDICATORS(CALCULATION_DATE, MA24, UPPER_BOLLINGER, ' \
              'LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI)' \
              'VALUES(?, ?, ?, ?, ?, ?, ?)'
        self.repository.write(sql, indicator, IndicatorsDAO.class_name)

    def insert_indicators(self, indicators):
        sql = 'MERGE INTO INDICATORS AS target ' \
              'USING(VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) ' \
              'AS source (CALCULATION_DATE, SPOT_PRICE, BUY_PRICE,SELL_PRICE, MA24, UPPER_BOLLINGER, LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI) ' \
              'ON target.calculation_date = source.calculation_date ' \
              'WHEN MATCHED THEN ' \
              'UPDATE SET ' \
              'SPOT_PRICE = source.SPOT_PRICE, ' \
              'BUY_PRICE = source.BUY_PRICE, ' \
              'SELL_PRICE = source.SELL_PRICE, ' \
              'MA24 = source.MA24, ' \
              'UPPER_BOLLINGER = source.UPPER_BOLLINGER, ' \
              'LOWER_BOLLINGER = source.LOWER_BOLLINGER, ' \
              'AVG_GAIN = source.AVG_GAIN, ' \
              'AVG_LOSS = source.AVG_LOSS, ' \
              'RSI = source.RSI ' \
              'WHEN NOT MATCHED THEN ' \
              'INSERT (CALCULATION_DATE, SPOT_PRICE, BUY_PRICE, ' \
              'SELL_PRICE, MA24, UPPER_BOLLINGER, LOWER_BOLLINGER, AVG_GAIN, AVG_LOSS, RSI) ' \
              'VALUES(source.CALCULATION_DATE, source.SPOT_PRICE, ' \
              'source.BUY_PRICE, source.SELL_PRICE, source.MA24, ' \
              'source.UPPER_BOLLINGER, source.LOWER_BOLLINGER, ' \
              'source.AVG_GAIN, source.AVG_LOSS, source.RSI);'
        self.repository.write_many(sql, indicators, IndicatorsDAO.class_name)