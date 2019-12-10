import os
import yaml
import pandas as pd

from stocks import get_trends


class TestCaseStocks:

    @classmethod
    def setup_class(cls):
        """Setup any test variables."""
        with open(os.path.abspath('config.yaml'), 'r') as config_file:
            cls.credentials = yaml.safe_load(config_file)
        cls.stocks_list = [stock.upper() for stock in cls.credentials['STOCKS']]
        cls.trends_test_dict = {
            'UPTRENDING': pd.DataFrame(data={
                'close': [37.81],
                'Live Price': [38.25],
                'Upper Band': [31.23],
                'Lower Band': [32.01]
            }),
            'RECENTLY_STARTED_UPTRENDING': pd.DataFrame(data={
                'close': [42.41],
                'Live Price': [49.88],
                'Upper Band': [46.35],
                'Lower Band': [40.93]
            }),
            'DOWNTRENDING': pd.DataFrame(data={
                'close': [23.14],
                'Live Price': [23.05],
                'Upper Band': [29.14],
                'Lower Band': [25.66]
            }),
            'RECENTLY_STARTED_DOWNTRENDING': pd.DataFrame(data={
                'close': [29.85],
                'Live Price': [28.91],
                'Upper Band': [41.52],
                'Lower Band': [29.83]
            })
        }

    def test_get_trends(self):
        """
        Pass a test dict with an example of each type of result returned by the function to test its functionality.
        :return:
        """
        assert get_trends(self.trends_test_dict) == (
            ['UPTRENDING'],
            ['RECENTLY_STARTED_UPTRENDING'],
            ['DOWNTRENDING'],
            ['RECENTLY_STARTED_DOWNTRENDING']
        )

