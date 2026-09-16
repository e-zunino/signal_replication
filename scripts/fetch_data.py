import yfinance as yf
import pandas as pd

def main():
    fetch_raw()


def fetch_raw():
    sp500 = pd.read_csv('../data/reference/sp500.csv')
    tickers = list(sp500['Symbol'])
    data = yf.download(tickers[:50], start='2010-01-01', end='2026-01-01')
    data.to_csv('../data/raw/prices_10_25.csv')

if __name__ == '__main__':
    main()