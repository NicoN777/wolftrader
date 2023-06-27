import unittest
from unittest.mock import patch
from wolftrader.entity.cbuser import CoinbaseUser


class TestCoinbaseUser(unittest.TestCase):

    cb_user_patcher = None
    cb_user_magic_mock = None

    @classmethod
    def setUpClass(cls) -> None:
        pass
        cls.cb_user_patcher = patch('wolftrader.entity.cbuser.CoinbaseUser', spec=CoinbaseUser)
        cls.cb_user_magic_mock = cls.cb_user_patcher.start()
        cls.mocked_cb_user_instance = cls.cb_user_magic_mock.return_value

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cb_user_patcher.stop()

    def test_get_price_records(self):
        self.cb_user_magic_mock.get_buy_price.return_value = ('31371.89', 'USD')
        self.cb_user_magic_mock.get_spot_price.return_value = ('31190.165', 'USD')
        self.cb_user_magic_mock.get_sell_price.return_value =('31047.26', 'USD')
        price_records = CoinbaseUser('abc', 'xyz').get_price_records
        self.assertTrue(len(price_records) == 6)
        self.assertTrue(len(list(filter(lambda x: x == 'USD',price_records))) == 3)


if __name__ == '__main__':
    unittest.main()
