from signal_replication.returns import compute_returns

def reversal_signal(prices, window=5, skip=0):
    """Returns the reversion to the mean signal based on the percentage
       change over 'windows' days, skipping 'skip' days from today."""

    return - compute_returns(prices, periods=window).shift(skip)