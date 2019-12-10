import yaml
import datetime
import pandas as pd
from yahoofinancials import YahooFinancials
from multiprocessing import Pool

# Read the API keys from the config file
with open('config.yaml', 'r') as config_file:
    credentials = yaml.safe_load(config_file)

stocks_list = [stock.upper() for stock in credentials['STOCKS']]


def get_bollinger_bands(stock: pd.DataFrame, length: int = 200, deviations: int = 1):
    """
    Calculate the rolling average and standard deviation from stock closing prices data to calculate the upper and
        lower bolling bands for a stock.
    :param stock: A DataFrame containing the live, closing, and previous closing prices for a stock.
    :param length: The length (in days) of the window for the rolling average.
    :param deviations: The number of standard deviations to use.
    :return: An updated DataFrame containing the upper and lower bolling bands.
    """
    # Get moving average and standard deviation
    stock[f'{length} Day MA'] = stock['close'].rolling(window=length).mean()
    stock[f'{length} Day STD'] = stock['close'].rolling(window=length).std()
    # Calculate upper and lower bollinger bands
    stock['Upper Band'] = stock[f'{length} Day MA'] + (stock[f'{length} Day STD'] * deviations)
    stock['Lower Band'] = stock[f'{length} Day MA'] - (stock[f'{length} Day STD'] * deviations)

    return stock


def get_trends(data: dict):
    """
    Analyse the price data for each stock and assign any uptrending or downtrending stocks to a list to be
        outputted by the discord bot.
    :param data: A dictionary of stocks and their respective price data.
    :return: A list of each uptrending, recently started uptrending, downtrending, and recently started
        downtrending stocks.
    """
    uptrending = []
    recently_started_uptrending = []
    downtrending = []
    recently_started_downtrending = []

    for stock, dataframe in data.items():
        # uptrending
        if dataframe['Live Price'].iloc[-1] > dataframe['Upper Band'].iloc[-1]:
            if dataframe['close'].iloc[-1] < dataframe['Upper Band'].iloc[-1]:
                recently_started_uptrending.append(stock)
            else:
                uptrending.append(stock)
        # downtrending
        elif dataframe['Live Price'].iloc[-1] < dataframe['Lower Band'].iloc[-1]:
            if dataframe['close'].iloc[-1] > dataframe['Lower Band'].iloc[-1]:
                recently_started_downtrending.append(stock)
            else:
                downtrending.append(stock)

    return uptrending, recently_started_uptrending, downtrending, recently_started_downtrending


def main():
    start = datetime.datetime.now()
    # Get current date and start date (length) days before current date
    current_date = datetime.datetime.now()
    start_date = current_date - datetime.timedelta(days=365)
    # Convert into YMD for stocks api
    _start = f'{start_date.year}-{start_date.month}-{start_date.day}'
    _end = f'{current_date.year}-{current_date.month}-{current_date.day}'

    # Setup ticker objects
    tickers = [YahooFinancials(stock) for stock in stocks_list]

    # Setup multi-threading pool with a worker for each stock
    with Pool(len(stocks_list) * 4) as p:
        # Get pool result objects asynchronously
        _current_workers = {
            ticker.ticker: p.apply_async(ticker.get_current_price) for ticker in tickers
        }
        _historical_price_workers = {
            ticker.ticker: p.apply_async(ticker.get_historical_price_data, args=(_start, _end, 'daily')) for ticker in tickers
        }
        # Get data from pool objects
        current_data = {
            stock: worker.get() for stock, worker in _current_workers.items()
        }
        price_data = {
            stock: pd.DataFrame(worker.get()[stock]['prices']) for stock, worker in _historical_price_workers.items()
        }
        # Append current and previous closing prices to price_data df
        for stock in stocks_list:
            price_data[stock]['Live Price'] = current_data[stock]
            price_data[stock]['Previous Closing Price'] = price_data[stock]['close'].iloc[-1]
        # Get bollinger bands
        bollinger_bands = {
            stock: get_bollinger_bands(price_data[stock]) for stock in stocks_list
        }
    # Analyse the stock trends
    up, recently_up, down, recently_down = get_trends(bollinger_bands)
    print(f'UP:\t{up}')
    print(f'RECENTLY UP:\t{recently_up}')
    print(f'DOWN:\t{down}')
    print(f'RECENTLY DOWN:\t{recently_down}')
    end = datetime.datetime.now()
    diff = end - start
    print(f'Runtime: {diff}')


main()
