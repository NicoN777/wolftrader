"""
    Main wolftrade module.
"""

from .application import coinbase_user_key, coinbase_user_secret, indicators_graph, rsi_graph, report_table
from .entity import cbuser as cu
from .util.logger import *
from .dao import price_history_dao
from .dao import user_dao
from .util import email
from .dao import indicators_dao
import pandas as pd
import matplotlib.pyplot as plt


coinbase_user = cu.CoinbaseUser(coinbase_user_key, coinbase_user_secret)
price_history_dao = price_history_dao.PriceHistoryDAO()
user_dao = user_dao.UserDAO()
indicators_dao = indicators_dao.IndicatorsDAO()
email_util = email.EmailUtil()

def mine():
    log_info('Data Miner')
    price_history_dao.insert_price_record(coinbase_user.get_price_records)

def __calculate():
    log_info('Calculate Indicators')
    prices = price_history_dao.get_price_records()
    indicators = pd.DataFrame(data=prices['records'], columns=prices['column_names'])
    indicators.set_index(keys='EXTRACTION_DATE', inplace=True)
    indicators['MA24'] = indicators['SPOT_PRICE'].rolling(24).mean()
    indicators['UPPER_BOLLINGER'] = indicators['MA24'] + (2 * indicators['SPOT_PRICE'].rolling(24).std())
    indicators['LOWER_BOLLINGER'] = indicators['MA24'] - (2 * indicators['SPOT_PRICE'].rolling(24).std())
    indicators['DIFF'] = indicators['SPOT_PRICE'].diff()
    indicators['ADVA'] = indicators[indicators['DIFF'] >= 0]['DIFF']
    indicators['DECL'] = -1 * (indicators[indicators['DIFF'] <= 0]['DIFF'])
    indicators[['ADVA', 'DECL']] = indicators[['ADVA', 'DECL']].fillna(0)
    indicators['AVG_GAIN'] = indicators['ADVA'].rolling(14).mean()
    indicators['AVG_LOSS'] = indicators['DECL'].rolling(14).mean()
    indicators['RS'] = indicators['AVG_GAIN'] / indicators['AVG_LOSS']
    indicators['RSI'] = 100 - (100 / (1 + indicators['RS']))
    indicators['LOWER'] = 30
    indicators['UPPER'] = 70

    subset = indicators[['MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER', 'AVG_GAIN', 'AVG_LOSS']].fillna(0).tail(1)
    indicator_records = [tuple(record) for record in subset.values]
    print(indicator_records[0])
    indicators_dao.insert_indicator(indicator_records[0])
    print('done')

    with open(report_table, 'w') as table:
        table.write(indicators.tail(60).to_html(columns=['SPOT_PRICE', 'BUY_PRICE', 'SELL_PRICE', 'MA24',
                                                         'UPPER_BOLLINGER', 'LOWER_BOLLINGER', 'RSI'],
                                                header=True, index=True))

    indicators[['SPOT_PRICE', 'MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER']].tail(60).plot(figsize=(16, 5))
    plt.title("WolfiePE Indicators Bollinger")
    plt.tight_layout()
    plt.savefig(indicators_graph)

    indicators[['RSI', 'LOWER', 'UPPER']].tail(60).plot(figsize=(16, 5))
    plt.title("WolfiePE Indicators RSI")
    plt.tight_layout()
    plt.savefig(rsi_graph)


def process():
    log_info('Data Processing')
    __calculate()
    # email_util.send_email("indicators", ['nicolasnunezromay@gmail.com'], "hola", 'report')

def trade():
    log_info('Wolf Trader')
    prices = price_history_dao.get_price_records()
    indicators = pd.DataFrame(data=prices['records'], columns=prices['column_names'])
