import yaml
import datetime
import pandas as pd
from yahoo_fin import stock_info as si
from multiprocessing import Pool

# Read the API keys from the config file
with open('config.yaml', 'r') as config_file:
    credentials = yaml.safe_load(config_file)

stocks_list = credentials['STOCKS']


def get_live_prices(stock, null_var = None):
    """
    Get the current price of a given stock.
    :param stocks:
    :return:
    """
    # Get live prices for each stock
    try:
        _live_data = si.get_live_price(stock)
    except ValueError:
        _live_data = None

    return _live_data


def get_closing_prices(stock, _days: int = 365):
    """
    Get the historical closing prices for a given stock.
    :param stock: Name of the stock to get prices for.
    :param _days: How many days in the past to pull stocks from (start date).
    :return: Historical closing prices for the given stock from the start date to present.
    """
    # Get current date
    current_date = datetime.datetime.now()
    # Set start date (length) days before current date
    _start = current_date - datetime.timedelta(days=_days)
    # Get previous close price
    try:
        _closing_data = si.get_data(stock, start_date=_start)['close']
    except ValueError:
        _closing_data = None

    return _closing_data


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
    stock[f'{length} Day MA'] = stock['Closing Prices'].rolling(window=length).mean()
    stock[f'{length} Day STD'] = stock['Closing Prices'].rolling(window=length).std()
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
        if dataframe['Live Price'][-1] > dataframe['Upper Band'][-1]:
            if dataframe['Previous Closing Price'][-1] < dataframe['Upper Band'][-1]:
                recently_started_uptrending.append(stock)
            else:
                uptrending.append(stock)
        # downtrending
        elif dataframe['Live Price'][-1] < dataframe['Lower Band'][-1]:
            if dataframe['Previous Closing Price'][-1] > dataframe['Lower Band'][-1]:
                recently_started_downtrending.append(stock)
            else:
                downtrending.append(stock)

    return uptrending, recently_started_uptrending, downtrending, recently_started_downtrending


def main():
    start = datetime.datetime.now()
    # Setup multi-threading pool with a worker for each stock
    with Pool(len(stocks_list) * 2) as p:
        # Get pool result objects asynchronously
        _live_workers = {
            stock: p.apply_async(get_live_prices, args=(stock, None)) for stock in stocks_list
        }
        _closing_workers = {
            stock: p.apply_async(get_closing_prices, args=(stock, 365)) for stock in stocks_list
        }
        # Get data from pool objects
        live_data = {
            stock: worker.get() for stock, worker in _live_workers.items()
        }
        closing_data = {
            stock: worker.get() for stock, worker in _closing_workers.items()
        }
        # Get yesterday's close
        # TODO: add check for date index to make sure previous close isn't the same day as the current date
        previous_closes = {
            stock: data[-1] if closing_data[stock] is not None else None for stock, data in closing_data.items()
        }
        # Create a dataframe for each stock
        dataframes = {
            stock: pd.DataFrame(data={
                'Live Price': live_data[stock] if live_data[stock] is not None else [None],
                'Closing Prices': closing_data[stock] if closing_data[stock] is not None else [None],
                'Previous Closing Price': previous_closes[stock] if previous_closes[stock] is not None else [None],
            })
            for stock in stocks_list
        }
        # Get bollinger bands
        bollinger_bands = {
            stock: get_bollinger_bands(dataframes[stock]) if dataframes[stock]['Closing Prices'] is not None else [None] for stock in stocks_list
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
        # FIXME!!!!!! ------> Find out why some stocks aren't being pulled properly from the yahoo finance API

main()
