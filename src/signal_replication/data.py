import pandas as pd

def load_prices(path="~/signal_replication/data/raw/prices_10_25.csv"):
    """Load raw price CSV and return a Close-price DataFrame (dates x tickers)."""

    raw = pd.read_csv(path, header=[0,1], index_col=0, parse_dates=True, date_format="%Y-%m-%d")
    return raw["Close"]