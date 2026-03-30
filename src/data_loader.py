import yfinance as yf
import pandas as pd


def load_prices(tickers, start="2020-01-01", end=None):
    data = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)

    if "Close" in data.columns:
        prices = data["Close"].copy()
    else:
        prices = data.copy()

    return prices.dropna()


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()