import pandas as pd
import scipy as sp
from signal_replication.returns import compute_returns
from signal_replication.returns import forward_returns


def rank_ic(signal, forward_ret):
    """Daily cross-sectional Spearman correlation between a signal and forward returns."""

    return signal.corrwith(forward_ret, axis=1, method="spearman")


def pearson_ic(signal, forward_ret):
    """Daily cross-sectional Pearson correlation between a signal and forward returns."""

    return signal.corrwith(forward_ret, axis=1, method="pearson")


def quantile_spread(signal, forward_ret, n_quantiles=5):
    """Quantile analysis for IC. Returns the difference between the mean of the forward returns highest and lowest quantile"""

    stacked_signal = signal.stack()
    stacked_forward_ret = forward_ret.stack()
    signal_forward_ret = (
        pd.DataFrame({"signal": stacked_signal, "forward": stacked_forward_ret})
        .dropna()
        .reset_index()
    )
    signal_forward_ret["quantile"] = signal_forward_ret.groupby(
        signal_forward_ret["Date"]
    )["signal"].transform(
        lambda x: pd.qcut(x, n_quantiles, labels=False, duplicates="drop")
    )
    quantile_means = (
        signal_forward_ret.groupby(["Date", "quantile"])["forward"]
        .mean()
        .unstack("quantile")
    )

    return quantile_means[n_quantiles - 1] - quantile_means[0]


def signal_summary(signal, forward_ret, n_quantiles=5):
    """A wrapper function returning a 'complete' analysis of a given signal."""

    rank = rank_ic(signal, forward_ret)
    rank_ic_mean = rank.mean()
    rank_ic_std = rank.std()
    rank_ic_ir = rank_ic_mean / rank_ic_std

    pearson = pearson_ic(signal, forward_ret)
    pearson_ic_mean = pearson.mean()
    pearson_ic_std = pearson.std()
    pearson_ic_ir = pearson_ic_mean / pearson_ic_std

    spread = quantile_spread(signal, forward_ret, n_quantiles)
    spread_mean = spread.mean()
    spread_std = spread.std()
    spread_ir = spread_mean / spread_std

    return pd.Series(
        {
            "rank_ic_mean": rank_ic_mean,
            "rank_ic_std": rank_ic_std,
            "rank_ic_ir": rank_ic_ir,
            "pearson_ic_mean": pearson_ic_mean,
            "pearson_ic_std": pearson_ic_std,
            "pearson_ic_ir": pearson_ic_ir,
            "spread_mean": spread_mean,
            "spread_std": spread_std,
            "spread_ir": spread_ir,
        }
    )
