import yaml
import datetime
import pandas as pd
from yahoo_fin import stock_info as si
from multiprocessing import Pool

# Read the API keys from the config file
with open('config.yaml', 'r') as config_file:
    credentials = yaml.safe_load(config_file)

stocks_list = credentials['STOCKS']


def get_live_prices(stocks: list):
    """"""
    # Get live prices for each stock
    live_prices = {
        stock: si.get_live_price(stock) for stock in stocks
    }

    return live_prices


def get_closing_prices(stock, length: int = 200):
    """"""
    # Get current date
    current_date = datetime.datetime.now()
    # Set start date (length) days before current date
    _start = current_date - datetime.timedelta(days=length)
    # Get previous close price
    all_closing_data = si.get_data(stock, start_date=_start)['close']
    # yesterdays_closing_data = all_closing_data[-1]

    return all_closing_data#, yesterdays_closing_data


def get_bollinger_bands(closing_data, length: int = 200, deviation: int = 1):
    """"""
    # TODO
    for stock in closing_data:
        # Get rolling window of stock
        _rolling = stock.rolling(window=length)
        # Get moving average and standard deviation
        stock[f'{length} Day MA'] = _rolling.mean()
        stock[f'{length} Day STD'] = _rolling.std()
        # Calculate upper and lower bollinger bands
        stock['Upper Band'] = stock[f'{length} Day MA'] + (stock[f'{length} Day STD'] * deviation)
        stock['Lower Band'] = stock[f'{length} Day MA'] - (stock[f'{length} Day STD'] * deviation)
        # stock[f'{length} Day MA'] = stock.rolling(window=length).mean()
        #
        # stock[f'{length} Day STD'] = stock.rolling(window=length).std()

    return closing_data


def get_trends(stocks, live_prices, closing_prices, upper_band, lower_band):
    """"""
    uptrending = []
    recently_started_uptrending = []
    downtrending = []
    recently_started_downtrending = []

    for stock in stocks:
        # uptrending
        if live_prices[stock] > upper_band:
            if closing_prices[stock][-1] < upper_band:
                recently_started_uptrending.append(stock)
            else:
                uptrending.append(stock)
        # downtrending
        elif live_prices[stock] < lower_band:
            if closing_prices[stock][-1] > lower_band:
                recently_started_downtrending.append(stock)
            else:
                downtrending.append(stock)


# TODO: add threading or multiprocessing to speed up getting the stock data
# if __name__ == 'main':
# Thread(target=get_live_prices, args=credentials['STOCKS']).start()
# Thread(target=get_previous_close, args=credentials['STOCKS']).start()

start = datetime.datetime.now()
# live = get_live_prices(credentials['STOCKS'])

# Setup multi-threading pool with a worker for each stock
with Pool(len(stocks_list)) as p:
    workers = {
        stock: p.apply_async(get_closing_prices, args=(stock, 200)) for stock in stocks_list
    }
    closing_data = {
        stock: worker.get() for stock, worker in workers.items()
    }

    for stock, data in closing_data.items():
        print(f'\n{stock}\n{data}\n')

# bollinger_data = get_bollinger_bands(closing_data)

end = datetime.datetime.now()
diff = end - start
print(diff)

