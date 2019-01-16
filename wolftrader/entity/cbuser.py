from coinbase.wallet.client import Client
from util.logger import *

class CoinbaseUser:

    class_name = __file__

    def __init__(self, key, secret):
        try:
            self.user = Client(key, secret, api_version='2016-02-18')
            self.info = self.user.get_current_user()
            self.user_email = self.info.email
            self.user_id = self.info.id
            self.user_name = self.info.name
            self.user_username = self.info.username
            log_debug('{} | {}'.format(CoinbaseUser.class_name, self.info))

            self.user_primary_account = self.user.get_primary_account()
            self.user_primary_account_balance = self.user_primary_account.balance.amount
            self.user_primary_account_currency = self.user_primary_account.balance.currency
            self.user_primary_account_name = self.user_primary_account.name
            self.user.primary_account_id = self.user_primary_account.id

            log_debug('{} | {}'.format(CoinbaseUser.class_name, self.user_primary_account))

            log_info('{}, success | CoinbaseUser has been initialized: {}'.format(CoinbaseUser.class_name, self.user_name))
        except Exception as error:
            log_critical('{}, there was an error | Failed to initialize a CoinbaseUser: {}'.format(CoinbaseUser.class_name, error))

    # Returns a tuple with buy price information(amount, currency)
    @property
    def get_buy_price(self):
        return self.user.get_buy_price(currency='USD')

    # Returns a tuple with buy price information(amount, currency)
    @property
    def get_sell_price(self):
        return self.user.get_sell_price(currency='USD')

    # Returns a tuple with buy price information(amount, currency)
    @property
    def get_spot_price(self):
        return self.user.get_spot_price(currency='USD')

    @property
    def get_price_records(self):
        buy_price = self.get_buy_price
        spot_price = self.get_spot_price
        sell_price = self.get_sell_price
        return(buy_price.amount, buy_price.currency,
               spot_price.amount, spot_price.currency,
               sell_price.amount, sell_price.currency)

    # Generates a unique transaction address
    @property
    def get_transaction_address(self):
        return str(self.user.create_address(self.user.id).address)

    @property
    def get_payment_methods(self):
        pass

    def __repr__(self):
        return 'CoinbaseUser('') keys are confidential yo'

    def __str__(self):
        return '----> User: {} {} {} {}'.format(self.user_name, self.user_email, self.user_username, self.user_id)