"""
    Main wolftrade module.
"""

from .application import coinbase_user_key, coinbase_user_secret, indicators_graph, rsi_graph
from .entity import cbuser as cu
from .util.logger import *
from .dao import price_history_dao
from .dao import user_dao
from .util import email
import pandas as pd
import matplotlib.pyplot as plt


coinbase_user = cu.CoinbaseUser(coinbase_user_key, coinbase_user_secret)
price_history_dao = price_history_dao.PriceHistoryDAO()
user_dao = user_dao.UserDAO()
email_util = email.EmailUtil()

def mine():
    log_info('Data Miner')
    price_history_dao.insert_price_record(coinbase_user.get_price_records)



    # email_util.send_email('Subject Test', None, receivers, 'Body Test', 'sell')
    # while True:
    #     price_history_dao.insert_price_record(coinbase_user.get_price_records)
    #     time.sleep(600)

def __calculate():
    log_info('Calculate Indicators')
    prices = price_history_dao.get_price_records()
    prices_dataframe = pd.DataFrame(data=prices['records'], columns=prices['column_names'])
    prices_dataframe.set_index(keys='EXTRACTION_DATE', inplace=True)
    indicators = pd.DataFrame(index=prices_dataframe.index, data=prices_dataframe['SPOT_PRICE'])
    indicators['MA24'] = indicators['SPOT_PRICE'].rolling(24).mean()
    indicators['UPPER_BOLLINGER'] = indicators['MA24'] + (2 * indicators['SPOT_PRICE'].rolling(24).std())
    indicators['LOWER_BOLLINGER'] = indicators['MA24'] - (2 * indicators['SPOT_PRICE'].rolling(24).std())
    # print(prices_dataframe[['SPOT_PRICE', 'MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER']])

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

    indicators[['SPOT_PRICE', 'MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER']].plot(figsize=(16, 5))
    plt.title("WolfiePE Indicators Bollinger")
    plt.tight_layout()
    plt.savefig(indicators_graph)

    indicators[['RSI', 'LOWER', 'UPPER']].plot(figsize=(16,5))
    plt.title("WolfiePE Indicators RSI")
    plt.tight_layout()
    plt.savefig(rsi_graph)


def process():
    log_info('Data Processing')
    __calculate()
    email_util.send_email("indicators", ['nicolasnunezromay@gmail.com'], "hola", 'report')

def trade():
    log_info('Wolf Trader')
