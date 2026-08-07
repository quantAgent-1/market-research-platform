"""A small, dependency-free vectorized backtester + performance stats.

Deliberately minimal and correct rather than feature-complete. The look-ahead
guard is the important part: weights decided at the close of day t earn day t+1's
return (we lag weights by one period). For richer needs, feed the loaders' panels
into vectorbt / backtrader instead.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def vector_backtest(prices: pd.DataFrame, weights: pd.DataFrame,
                    cost_bps: float = 1.0) -> pd.DataFrame:
    """Backtest target weights on a price panel.

    prices : wide [time x symbol] (e.g. close). weights : wide target weights,
    same axes; `weights.loc[t]` is the desired holding decided at close t. It earns
    the *next* period's return (weights are lagged one step — no look-ahead).
    `cost_bps` charges |turnover| * bps at each rebalance.

    Returns a frame with gross_return, cost, net_return, equity, turnover.
    """
    prices = prices.sort_index()
    rets = prices.pct_change().fillna(0.0)
    w = (weights.reindex(index=prices.index, columns=prices.columns)
         .astype(float).fillna(0.0))
    w_prev = w.shift(1).fillna(0.0)               # holdings earning today's return
    gross = (w_prev * rets).sum(axis=1)
    turnover = (w - w_prev).abs().sum(axis=1)     # traded to reach today's target
    cost = turnover * (cost_bps / 1e4)
    net = gross - cost
    return pd.DataFrame({
        "gross_return": gross,
        "cost": cost,
        "net_return": net,
        "equity": (1.0 + net).cumprod(),
        "turnover": turnover,
    })


def performance_stats(returns: pd.Series, periods_per_year: int = 252,
                      rf: float = 0.0) -> dict:
    """Standard summary stats for a return series."""
    r = pd.Series(returns).dropna()
    if r.empty:
        return {}
    n = len(r)
    total = float((1.0 + r).prod() - 1.0)
    cagr = float((1.0 + total) ** (periods_per_year / n) - 1.0)
    vol = float(r.std() * np.sqrt(periods_per_year))
    sd = r.std()
    sharpe = float((r.mean() - rf / periods_per_year) / sd * np.sqrt(periods_per_year)) if sd > 0 else float("nan")
    downside = r[r < 0].std()
    sortino = float(r.mean() / downside * np.sqrt(periods_per_year)) if downside > 0 else float("nan")
    eq = (1.0 + r).cumprod()
    max_dd = float((eq / eq.cummax() - 1.0).min())
    return {
        "total_return": total,
        "cagr": cagr,
        "ann_vol": vol,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": max_dd,
        "hit_rate": float((r > 0).mean()),
        "n_periods": n,
    }
