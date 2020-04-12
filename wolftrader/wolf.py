"""
    Main wolftrade module.
"""

from application import coinbase_user_key, coinbase_user_secret, \
    indicators_graph, rsi_graph, report_table, \
    users, azure_store_account_name, azure_store_connstr, indicators_csv
from entity import cbuser as cu
from util.logger import *
from util.filestore import FileStore
from util.handler import exception
from dao.price_history import PriceHistoryDAO
from dao.transaction import TransactionDAO
from dao.user import UserDAO
from dao.indicators import IndicatorsDAO
from util import mailer
import pandas as pd
import matplotlib.pyplot as plt
from util.texter import Texter
from collections import namedtuple


def mine():
    log_info('Data Miner')
    user_dao = UserDAO(kind='AzureSQLServer')
    price_history_dao = PriceHistoryDAO(kind='AzureSQLServer')
    coinbase_user = cu.CoinbaseUser(coinbase_user_key, coinbase_user_secret)
    price_history_dao.insert_price_record(coinbase_user.get_price_records)


def __calculate():
    log_info('Calculate Indicators')
    price_history_dao = PriceHistoryDAO(kind='AzureSQLServer')
    indicators_dao = IndicatorsDAO(kind='AzureSQLServer')
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
    subset = subset.loc[~subset.index.duplicated(keep='first')]
    subset.reset_index(inplace=True)
    indicator_records = [tuple(record) for record in subset.values]
    indicators_dao.insert_indicators(indicator_records)


def __upload_files(files):
    import datetime
    import os
    now = datetime.datetime.now().strftime("%m-%d-%Y%H%M%S")
    file_names = [(name, f'{now}-{os.path.basename(name)}') for name in files]
    file_store = FileStore(azure_store_account_name, azure_store_connstr)
    for file in file_names:
        file_store.upload(*file)


def __get_indicators():
    indicators_dao = IndicatorsDAO(kind='AzureSQLServer')
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

    indicators.to_csv(indicators_csv, header=True, index=True)
    indicators[['SPOT_PRICE', 'MA24', 'UPPER_BOLLINGER', 'LOWER_BOLLINGER']].tail(200).plot(figsize=(16, 5))
    plt.title("WolfiePE Indicators Bollinger")
    plt.tight_layout()
    plt.savefig(indicators_graph)

    indicators[['RSI', 'LOWER', 'UPPER']].tail(200).plot(figsize=(16, 5))
    plt.title("WolfiePE Indicators RSI")
    plt.tight_layout()
    plt.savefig(rsi_graph)
    __upload_files([indicators_graph, rsi_graph, indicators_csv])


def process():
    log_info('Data Processing')
    __calculate()


def notify():
    __get_indicators()
    email_util = mailer.EmailUtil()
    email_util.send_email("indicators", users, "hola", 'report')


def trade():
    transaction_dao = TransactionDAO(kind='AzureSQLServer')
    Selector = namedtuple('Selector', ['value', 'band'])
    log_info('Wolf Trader')
    indicators_dao = IndicatorsDAO(kind='AzureSQLServer')
    data = indicators_dao.get_indicators()
    indicators = pd.DataFrame(data=data['records'], columns=data['column_names'])
    data_point = indicators.tail(1)
    spot_price = data_point['SPOT_PRICE'].iloc[0]
    buy_price = data_point['BUY_PRICE'].iloc[0]
    sell_price = data_point['SELL_PRICE'].iloc[0]
    upper = data_point['UPPER_BOLLINGER'].iloc[0]
    lower = data_point['LOWER_BOLLINGER'].iloc[0]
    rsi = data_point['RSI'].iloc[0]
    selectors = [Selector(abs(spot_price - upper), 'upper'),
                (Selector(abs(spot_price - lower), 'lower'))]
    closer = min(selectors, key=lambda s: s.value)
    oversold = rsi < 30
    overbought = rsi > 70
    buy_signal = oversold and closer.band == 'lower'
    sell_signal = overbought and closer.band == 'upper'
    pricing_info = f'SPOT: ${spot_price}' \
                   f'\nBUY: ${buy_price}' \
                   f'\nSELL: ${sell_price} ' \
                   f'\nSelector: {closer}'

    #Build record for insertion...
    #TYPE, AMOUNT, BOUGHT_AT, SPOT_PRICE, BUY_PRICE, SELL_PRICE
    if sell_signal:
        body = f'Signal --- A sell signal has been triggered\n{pricing_info}'
        __sms(body, 'sell', pricing_info)
        last_transaction = __get_last_transaction(transaction_dao, 'BUY')
        price_at = last_transaction['PRICE_AT'].iloc[0]
        gain = price_at - sell_price
        if price_at > sell_price:
            record = ('SELL', 1, sell_price, spot_price, buy_price, sell_price, gain)
        else:
            record = ('SSNONE', 0, sell_price, spot_price, buy_price, sell_price, gain)
        transaction_dao.insert_transaction(record)

    elif buy_signal:
        body = f'Signal --- A buy signal has been triggered\n{pricing_info}'
        __sms(body, 'buy', pricing_info)
        last_transaction = __get_last_transaction(transaction_dao, 'SELL')
        price_at = last_transaction['PRICE_AT'].iloc[0]
        gain = price_at - buy_price
        if buy_price < price_at:
            record = ('BUY', 1, buy_price, spot_price, buy_price, sell_price, gain)
        else:
            record = ('BSNONE', 0, buy_price, spot_price, buy_price, sell_price, gain)
        transaction_dao.insert_transaction(record)
    else:
        log_info(pricing_info)


def __get_last_transaction(transaction_dao, type):
    last_transaction_data = transaction_dao.get_n_transactions_of_type(type, 1)
    last_transaction = pd.DataFrame(data=last_transaction_data['records'],
                                    columns=last_transaction_data['column_names'])
    return last_transaction


def __sms(body, type, pricing_info):
    with Texter(body):
        log_info(f'{type} signal triggered, message sent. {pricing_info}')

if __name__ == '__main__':
    __get_indicators()