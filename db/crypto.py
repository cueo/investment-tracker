import datetime
import sqlite3

from model.crypto import CryptoTracker

con = sqlite3.connect('identifier.sqlite')
con.row_factory = sqlite3.Row
cur = con.cursor()

coin_map = {}


def add_coin(coin, quantity):
    print(f'Adding coin={coin} in DB')
    query = 'INSERT INTO crypto (coin, quantity) VALUES (?, ?)'
    cur.execute(query, (coin, quantity))
    con.commit()
    row_id = cur.lastrowid
    coin_map[row_id] = coin
    return row_id


def get_coin_id(coin):
    _id = None
    query = 'SELECT id FROM crypto WHERE coin=:coin'
    cur.execute(query, {'coin': coin})
    row = cur.fetchone()
    return row and row['id']


def get_coin(coin_id):
    if coin_id in coin_map:
        return coin_map[coin_id]
    query = 'SELECT coin FROM crypto WHERE id=:id'
    cur.execute(query, {'id': coin_id})
    row = cur.fetchone()
    coin = None
    if row:
        coin = row['coin']
        coin_map[coin_id] = coin
    return coin


def crypto_insert(coin, quantity, value):
    print(f'Storing coin={coin} with quantity={quantity} and value={value} in DB')
    query = 'INSERT INTO crypto_tracker (value, time, coin_id) VALUES (?, ?, ?)'
    time = datetime.datetime.now()
    coin_id = get_coin_id(coin)
    if coin_id is None:
        coin_id = add_coin(coin, quantity)
    cur.execute(query, (value, time, coin_id))
    con.commit()


def build_trackers(rows):
    trackers = {}
    for row in rows:
        coin = get_coin(row['coin_id'])
        if coin not in trackers:
            crypto_tracker = CryptoTracker(coin)
            trackers[coin] = crypto_tracker
        crypto_tracker = trackers[coin]
        crypto_tracker.values.append(row['value'])
        time = datetime.datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S.%f')
        crypto_tracker.times.append(time)
    return trackers


def get_crypto_data(days=7):
    print(f'Reading crypto data for last {days} days')
    query = f"SELECT * FROM crypto_tracker WHERE time > (SELECT DATETIME('now', '-{days} day'))"
    cur.execute(query)
    rows = cur.fetchall()
    return build_trackers(rows)
