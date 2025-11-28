import unittest 
import pandas as pd
"""need this package:  pip install yahooquery"""
"""if ncessary, upgrade numpy:  pip install --upgrade numpy"""
import yahooquery as yf 

def get_stock_data(ticker):
    """pull data from yahoo finance"""
    stock = yf.Ticker(ticker)
    df = stock.history(start="2025-01-21", end="2025-11-27")
    print(df)
    return df
 
class TestGetStockData(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """We only want to pull this data once for each TestCase since it is an expensive operation"""
        self.df = get_stock_data('TSLA')
 
    def test_columns_present(self):
        """ensures that the expected columns are all present"""
        self.assertIn("open", self.df.columns)
        self.assertIn("high", self.df.columns)
        self.assertIn("low", self.df.columns)
        self.assertIn("close", self.df.columns)
        self.assertIn("volume", self.df.columns)
 
    def test_non_empty(self):
        """ensures that there is more than one row of data"""
        self.assertNotEqual(len(self.df.index), 0)

    def test_at_least_n(self):
        """ensures at least n entries present in the data"""
        n = 200
        message = "Not greater than " + str(n) + " entries in this data set!"
        self.assertGreater(len(self.df.index), n, message)
 
    def test_high_low(self):
        """ensure high and low are the highest and lowest in the same row"""
        ohlc = self.df[["open","high","low","close"]]
        highest = ohlc.max(axis=1)
        lowest = ohlc.min(axis=1)
        self.assertTrue(ohlc.le(highest, axis=0).all(axis=None))
        self.assertTrue(ohlc.ge(lowest, axis=0).all(axis=None))

unittest.main()


