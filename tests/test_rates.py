import unittest
import os

from rates import Client
from rates.providers import FetchError
from rates.providers.alphavantage import Alphavantage


class RateTest(unittest.TestCase):
    def setUp(self):
        provider = Alphavantage({"api_key": os.environ.get("ALPHAVANTAGE_API_KEY", "")})
        self.cl = Client(provider)

    def test_btc_usd(self):
        rate = self.cl.get("btc", "usd")

        self.assertNotEqual(rate.rate, "")
        self.assertEqual(rate.error, "")

    def test_unknown_currency(self):
        with self.assertRaises(FetchError):
            self.cl.get("btc", "unknown")
