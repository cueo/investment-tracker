import json
from pprint import pprint

from db import crypto
from service import crypto_api


def add_values(data):
    print('Adding value of coins to data')
    currency = 'USD'
    keys = data.keys()
    quotes = crypto_api.get_quotes(keys, currency)
    for key in keys:
        coin = data[key]
        coin['value'] = quotes[key][currency]
    print(f'Added values to coin data={data}')
    return data


def read_data():
    print('Loading data from json')
    with open('data/crypto.json', 'r') as f:
        return json.load(f)


def store(data):
    print('Storing data in DB')
    for coin, quotes in data.items():
        quantity = quotes['quantity']
        value = quotes['value'] * quantity
        crypto.crypto_insert(coin, quantity, value)


def refresh_crypto_data():
    data = read_data()
    data = add_values(data)
    store(data)
    return data


def get_crypto_data():
    return crypto.get_crypto_data()


def main():
    data = refresh_crypto_data()
    # pprint(data)
    # data = get_crypto_data()
    # pprint(data)


if __name__ == '__main__':
    main()
