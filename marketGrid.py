import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the symbols for the 4 stock indices
symbols = ['^GSPC', 'BTC-USD', '^GDAXI', '^HSI']

# Define the SMA periods
fast_sma = 20
slow_sma = 50
# Define the start date for the data based on the number of months
start_date_months = 36
start_date = (datetime.today() - timedelta(days=start_date_months * 30)).strftime('%Y-%m-%d')

# Download the data for each symbol
data = {}
for symbol in symbols:
    data[symbol] = yf.download(symbol, start=start_date)

# Define the color palette
price_color = 'darkgray'
sma_fast_color = 'darkred'
sma_slow_color = 'darkgreen'
last_close_color = 'blue'

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot the stock prices and moving averages for each symbol
for i, symbol in enumerate(symbols):
    row = i // 2
    col = i % 2
    ax = axs[row, col]

    ax.plot(data[symbol].index, data[symbol]['Close'], color=price_color, label='Price')
    ax.plot(data[symbol].index, data[symbol]['Close'].rolling(window=fast_sma).mean(), color=sma_fast_color,
            label=f'{fast_sma}-day SMA')
    ax.plot(data[symbol].index, data[symbol]['Close'].rolling(window=slow_sma).mean(), color=sma_slow_color,
            label=f'{slow_sma}-day SMA')

    # Set title and labels
    ax.set_title(symbol)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    # Add trend signal annotation to the chart
    fast_ma = data[symbol]['Close'].rolling(window=fast_sma).mean()
    slow_ma = data[symbol]['Close'].rolling(window=slow_sma).mean()
    trend_signal = ''
    if fast_ma.iloc[-1] > slow_ma.iloc[-1]:
        trend_signal = 'Trend Up'
    elif fast_ma.iloc[-1] < slow_ma.iloc[-1]:
        trend_signal = 'Trend Down'
    ax.annotate(trend_signal, xy=(data[symbol].index[-1], data[symbol]['Close'].iloc[-1]),
                xytext=(10, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', lw=1),
                fontsize=10, color='black')

    # Plot the last close value on each grid
    last_close = data[symbol]['Close'].iloc[-1]
    ax.scatter(data[symbol].index[-1], last_close, color=last_close_color, label='Last Close')

    # Print the value of the last close on the plot
    ax.text(data[symbol].index[-1], last_close, f'{last_close:.2f}', ha='right', va='bottom', color=last_close_color)

    # Print the value of the last close and trend in the console
    print(f"Symbol: {symbol}")
    print(f"Last Close: {last_close:.2f}")
    print(f"Trend: {trend_signal}")
    print()

    # Add legend
    ax.legend()

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()
