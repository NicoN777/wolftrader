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
    print(user_dao.get_user_emails())
    print(user_dao.get_user_by_id('1'))
    prices = price_history_dao.get_price_records()
    prices_dataframe = pd.DataFrame(data=prices['records'], columns=prices['column_names'])
    prices_dataframe.set_index(keys='EXTRACTION_DATE', inplace=True)
    prices_dataframe['MA24'] = prices_dataframe['SPOT_PRICE'].rolling(24).mean()
    prices_dataframe['UPPER_BOLLINGER'] = prices_dataframe['MA24'] + (2 * prices_dataframe['SPOT_PRICE'].rolling(24).std())
    prices_dataframe['LOWER_BOLLINGER'] = prices_dataframe['MA24'] - (2 * prices_dataframe['SPOT_PRICE'].rolling(24).std())
    print(prices_dataframe[['SPOT_PRICE', 'MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER']])
    prices_dataframe[['SPOT_PRICE', 'MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER']].plot(figsize=(16, 5))
    plt.savefig(indicators_graph)

def process():
    log_info('Data Processing')
    __calculate()

def trade():
    log_info('Wolf Trader')
