"""
    Main wolftrade module.
"""

from .application import coinbase_user_key, coinbase_user_secret, indicators_graph, rsi_graph, report_table
from .entity import cbuser as cu
from .util.logger import *
from .dao.price_history_dao import PriceHistoryDAO
from .dao.user_dao import UserDAO
from .dao.indicators_dao import IndicatorsDAO
from .util import mailer
import pandas as pd
import matplotlib.pyplot as plt


def mine():
    log_info('Data Miner')
    user_dao = UserDAO()
    price_history_dao = PriceHistoryDAO()
    coinbase_user = cu.CoinbaseUser(coinbase_user_key, coinbase_user_secret)
    price_history_dao.insert_price_record(coinbase_user.get_price_records)

def __calculate():
    log_info('Calculate Indicators')
    price_history_dao = PriceHistoryDAO()
    indicators_dao = IndicatorsDAO()
    data = price_history_dao.get_price_records()
    indicators = pd.DataFrame(data=data['records'], columns=data['column_names'])
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


    subset = indicators[['SPOT_PRICE', 'BUY_PRICE', 'SELL_PRICE', 'MA24', 'UPPER_BOLLINGER',
                         'LOWER_BOLLINGER', 'AVG_GAIN', 'AVG_LOSS', 'RSI']].fillna(0)
    subset.reset_index(inplace=True)

    indicator_records = [tuple(record) for record in subset.values]
    indicators_dao.insert_indicators(indicator_records)



def process():
    log_info('Data Processing')
    __calculate()

def notify():
    indicators_dao = IndicatorsDAO()
    email_util = mailer.EmailUtil()
    data = indicators_dao.get_indicators()
    indicators = pd.DataFrame(data=data['records'], columns=data['column_names'])
    indicators.set_index(keys='CALCULATION_DATE', inplace=True)
    indicators['LOWER'] = 30
    indicators['UPPER'] = 70

    with open(report_table, 'w') as table:
        table.write(indicators.tail(200).to_html(columns=['SPOT_PRICE', 'BUY_PRICE', 'SELL_PRICE', 'MA24',
                                                         'UPPER_BOLLINGER', 'LOWER_BOLLINGER', 'AVG_GAIN',
                                                         'AVG_LOSS', 'RSI'],
                                                header=True, index=True))

    indicators[['SPOT_PRICE', 'MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER']].tail(200).plot(figsize=(16, 5))
    plt.title("WolfiePE Indicators Bollinger")
    plt.tight_layout()
    plt.savefig(indicators_graph)

    indicators[['RSI', 'LOWER', 'UPPER']].tail(200).plot(figsize=(16, 5))
    plt.title("WolfiePE Indicators RSI")
    plt.tight_layout()
    plt.savefig(rsi_graph)
    email_util.send_email("indicators", ['nicolasnunezromay@gmail.com'], "hola", 'report')


def trade():
    log_info('Wolf Trader')
    indicators_dao = IndicatorsDAO()
    data = indicators_dao.get_indicators()
    indicators = pd.DataFrame(data=data['records'], columns=data['column_names'])
    signal = indicators.tail(1)['RSI']
    sell_signal= (signal < 30).bool()
    buy_signal = (signal > 70).bool()
    if sell_signal:
        print('Selling')
    elif buy_signal:
        print('Buying')
    else:
        print(signal)

