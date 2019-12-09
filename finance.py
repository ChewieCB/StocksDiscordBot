import yaml
import datetime
import pandas as pd
from yahoo_fin import stock_info as si
from threading import Thread

# Read the API keys from the config file
with open('config.yaml', 'r') as config_file:
    credentials = yaml.safe_load(config_file)


def get_live_prices(stocks: list):
    """"""
    # Get live prices for each stock
    live_prices = {
        stock: si.get_live_price(stock) for stock in stocks
    }

    return live_prices


def get_previous_close(stocks: list, length: int = 200):
    """"""
    # Get current date
    current_date = datetime.datetime.now()
    _start = current_date - datetime.timedelta(days=length)
    # Get previous close price
    closing_data = {
        stock: si.get_data(stock, start_date=_start)['close'] for stock in stocks
    }
    yesterdays_close_data = {
        stock: data[-1] for stock, data in closing_data.items()
    }

    return closing_data, yesterdays_close_data


def get_bollinger_bands(closing_data: list, length: int = 200, deviation: int = 1):
    """"""
    # TODO
    pass


# TODO: add threading or multiprocessing to speed up getting the stock data
# if __name__ == 'main':
# Thread(target=get_live_prices, args=credentials['STOCKS']).start()
# Thread(target=get_previous_close, args=credentials['STOCKS']).start()

start = datetime.datetime.now()
live = get_live_prices(credentials['STOCKS'])
closing, yesterdays_closing = get_previous_close(credentials['STOCKS'])

end = datetime.datetime.now()
diff = end - start

print()

