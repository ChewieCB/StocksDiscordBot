import yaml
import pytest
from multiprocessing import Pool

from stocks import get_live_prices, get_closing_prices, get_bollinger_bands, get_trends


class TestCaseStocks:

    @classmethod
    def setup_class(cls):
        """Setup any test variables."""
        with open('config.yaml', 'r') as config_file:
            cls.credentials = yaml.safe_load(config_file)
        cls.stocks_list = [stock.upper() for stock in cls.credentials['STOCKS']]

    @pytest.skip
    def test_live_prices(self):
        """"""
        data = {
            stock: get_live_prices(stock) for stock in self.stocks_list
        }
        assert data

    @pytest.skip
    def test_closing_prices(self):
        """"""
        data = {
            stock: get_closing_prices(stock) for stock in self.stocks_list
        }
        assert data

    @pytest.skip
    def test_bollinger_bands(self):
        """"""
        # TODO:

    @pytest.skip
    def test_get_trends(self):
        """"""
        # TODO:

    def test_multiprocessing_live_prices(self):
        """"""
        # TODO
        # with Pool(len(self.stocks_list)) as p:
        #     workers = {
        #         stock: p.apply_async(get_closing_prices, args=(stock, 365)) for stock in self.stocks_list
        #     }
        #     data = {
        #         stock: worker.get() for stock, worker in workers.items()
        #     }
        #     assert data

    def test_multiprocessing_closing_prices(self):
        """"""
        with Pool(len(self.stocks_list)) as p:
            workers = {
                stock: p.apply_async(get_closing_prices, args=(stock, 365)) for stock in self.stocks_list
            }
            data = {
                stock: worker.get() for stock, worker in workers.items()
            }
            assert data

