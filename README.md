# python_marketGrid

# Stock Index Prices README

This code is used to fetch stock index data using the `yfinance` library and visualize it using `plotly` library in Python. The code downloads historical data for four stock indices (`^GSPC`, `^DJI`, `^GDAXI`, `^HSI`) and calculates and plots the 20-day and 50-day Simple Moving Averages (SMA) for each index. It also adds trend signal annotations to the chart based on the relationship between the fast and slow moving averages.

![image](https://github.com/jamiePDunne/python_marketGrid/assets/83908748/75626203-a928-4899-acd1-2cebb66be348)


## Prerequisites

Make sure you have the following libraries installed before running the code:

- `yfinance`
- `plotly`

You can install them using `pip`:

```
pip install yfinance plotly
```

## Usage

1. Import the necessary libraries:

```python
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
```

2. Define the stock symbols and SMA periods:

```python
symbols = ['^GSPC', '^DJI', '^GDAXI', '^HSI']
fast_sma = 20
slow_sma = 50
```

3. Set the start date for the data:

```python
start_date_months = 36
start_date = (datetime.today() - timedelta(days=start_date_months*30)).strftime('%Y-%m-%d')
```

4. Download the data for each symbol:

```python
data = {}
for symbol in symbols:
    data[symbol] = yf.download(symbol, start=start_date)
```

5. Define the color palette:

```python
price_color = 'darkgray'
sma_fast_color = 'darkred'
sma_slow_color = 'darkgreen'
```

6. Create a 2x2 subplot grid:

```python
fig = make_subplots(rows=2, cols=2, subplot_titles=symbols)
```

7. Add the stock prices and moving averages for each symbol to the subplot grid:

```python
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
```

8. Add trend signal annotation to the chart:

```python
fast_ma = data[symbol]['Close'].rolling(window=fast_sma).mean()
slow_ma = data[symbol]['Close'].rolling(window=slow_sma).mean()
trend_signal = ''
if fast_ma[-1] > slow_ma[-1]:
    trend_signal = 'Trend Up'
elif fast_ma[-1] < slow_ma[-1]:
    trend_signal = 'Trend Down'
fig.add_annotation(
    x=data

[symbol].index[-1],
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
```

9. Update the layout of the subplot grid:

```python
fig.update_layout(
    title='Stock Index Prices',
    height=800,
    width=1000,
)
```

10. Show the plot:

```python
fig.show()
```

## License

This code is licensed under the [MIT License](LICENSE).
