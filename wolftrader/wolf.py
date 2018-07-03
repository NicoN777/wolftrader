"""
    Main wolftrade module.
"""

from .application import coinbase_user_key, coinbase_user_secret
from .entity import cbuser as cu
from .util.logger import *
from .dao import price_history_dao
import time

coinbase_user = cu.CoinbaseUser(coinbase_user_key, coinbase_user_secret)
price_history_dao = price_history_dao.PriceHistoryDAO()


def mine():
    log_info('Data Miner')
    while True:
        price_history_dao.insert_price_record(coinbase_user.get_price_records)
        time.sleep(600)



def visualize():
    log_info('Data Visualizer')

def trade():
    log_info('Wolf Trader')