import yaml
import datetime
from yahoo_fin import stock_info as si

# Read the API keys from the config file
with open('config.yaml', 'r') as config_file:
    credentials = yaml.safe_load(config_file)


def get_live_prices(stocks: list):
    """"""
    live_prices = {
        stock: si.get_live_price(stock) for stock in stocks
    }


def get_previous_close(stocks: list):
    """"""
    # Get current date
    current_date = datetime.datetime.now()
    previous_day = current_date - datetime.timedelta(days=1)
    # Get previous close price
    previous_closing_prices = {
        stock: si.get_data(stock, start_date=previous_day)['close'][0] for stock in stocks
    }

    return previous_closing_prices


# if __name__ == 'main':
get_live_prices(credentials['STOCKS'])
get_previous_close(credentials['STOCKS'])

print()

