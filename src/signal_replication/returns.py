import pandas as pd

def compute_returns(prices, periods=1):
    """Returns percentage change over the desired period."""
    
    return prices.pct_change(periods=periods)

def forward_returns(prices, horizon=1):
    """Returns percentage change return from day t to day t + 'horizon', aligned to day t."""

    return compute_returns(prices, periods=horizon).shift(-horizon)