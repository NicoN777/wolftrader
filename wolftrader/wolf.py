"""
    Main wolftrade module.
"""

from .application import coinbase_user_key, coinbase_user_secret
from .entity import cbuser as cu
from .util.logger import *

coinbase_user = cu.CoinbaseUser(coinbase_user_key, coinbase_user_secret)

def mine():
    log_info('Data Miner')


def visualize():
    log_info('Data Visualizer')

def trade():
    log_info('Wolf Trader')
