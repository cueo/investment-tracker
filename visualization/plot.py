import matplotlib.pyplot as plt

from db import crypto

data = crypto.get_crypto_data()

for coin, tracker in data.items():
    plot_data = {}
    for i in range(len(tracker.values)):
        value = tracker.values[i]
        time = tracker.times[i]
        plot_data[time] = value
    x, y = zip(*sorted(plot_data.items()))
    plt.plot(x, y, label=coin)

plt.xlabel('Dates')
plt.ylabel('Value in USD')
plt.legend()

plt.show()
