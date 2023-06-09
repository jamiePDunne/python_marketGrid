import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Define the symbols for the 4 stock indices
symbols = ['^GSPC', '^DJI', '^GDAXI', '^HSI']

# Define the SMA periods
fast_sma = 20
slow_sma = 50
# Define the start date for the data based on the number of months
start_date_months = 36
start_date = (datetime.today() - timedelta(days=start_date_months*30)).strftime('%Y-%m-%d')

# Download the data for each symbol
data = {}
for symbol in symbols:
    data[symbol] = yf.download(symbol, start=start_date)

# Define the color palette
price_color = 'darkgray'
sma_fast_color = 'darkred'
sma_slow_color = 'darkgreen'

# Create a 2x2 subplot grid
fig = make_subplots(rows=2, cols=2, subplot_titles=symbols)

# Add the stock prices and moving averages for each symbol to the subplot grid
for i, symbol in enumerate(symbols):
    row = (i // 2) + 1
    col = (i % 2) + 1
    fig.add_trace(
        go.Scatter(
            x=data[symbol].index,
            y=data[symbol]['Close'],
            name='Price',
            line=dict(color=price_color, dash='solid')
        ),
        row=row,
        col=col
    )
    fig.add_trace(
        go.Scatter(
            x=data[symbol].index,
            y=data[symbol]['Close'].rolling(window=fast_sma).mean(),
            name=f'{fast_sma}-day SMA',
            line=dict(color=sma_fast_color, dash='solid')
        ),
        row=row,
        col=col
    )
    fig.add_trace(
        go.Scatter(
            x=data[symbol].index,
            y=data[symbol]['Close'].rolling(window=slow_sma).mean(),
            name=f'{slow_sma}-day SMA',
            line=dict(color=sma_slow_color, dash='solid')
        ),
        row=row,
        col=col
    )

    # Add trend signal annotation to the chart
    fast_ma = data[symbol]['Close'].rolling(window=fast_sma).mean()
    slow_ma = data[symbol]['Close'].rolling(window=slow_sma).mean()
    trend_signal = ''
    if fast_ma[-1] > slow_ma[-1]:
        trend_signal = 'Trend Up'
    elif fast_ma[-1] < slow_ma[-1]:
        trend_signal = 'Trend Down'
    fig.add_annotation(
        x=data[symbol].index[-1],
        y=data[symbol]['Close'][-1],
        text=trend_signal,
        showarrow=False,
        font=dict(
            size=12,
            color='black'
        ),
        row=row,
        col=col
    )

# Update the layout of the subplot grid
fig.update_layout(
    title='Stock Index Prices',
    height=800,
    width=1000,
)

# Show the plot
fig.show()
