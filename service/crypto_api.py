import os
from pprint import pprint

from requests import Session

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.getenv('API_KEY')
}

session = Session()
session.headers.update(headers)


def extract_quote(response):
    print('Simplifying API response')
    response = response['data']
    data = {}
    for coin, coin_data in response.items():
        quote = {}
        quote_response = coin_data['quote']
        for currency, currency_data in quote_response.items():
            quote[currency.upper()] = currency_data['price']
        data[coin.upper()] = quote
    print(f'Simplified API response={data}')
    return data


def get_quotes(symbols, currencies='USD'):
    symbols = ','.join(symbols)
    print(f'Fetching value of coins={symbols} in {currencies}')
    parameters = {
        'symbol': symbols,
        'convert': currencies
    }
    r = session.get(url, params=parameters)
    r.raise_for_status()
    return extract_quote(r.json())


if __name__ == '__main__':
    quotes = get_quotes(['XRP', 'BTC', 'ETH', 'DOGE'], 'USD')
    pprint(quotes)
