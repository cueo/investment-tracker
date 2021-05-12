from datetime import datetime


class CryptoTracker:
    def __init__(self, coin):
        self.coin = coin
        self.values = []
        self.times = []

    def times_str(self):
        return [time.strftime('%Y-%m-%d %H:%M:%S.%f') for time in self.times]

    def __repr__(self) -> str:
        return f'CryptoTracker(coin={self.coin},' \
               f'values={self.values},' \
               f'times={self.times_str()})'
