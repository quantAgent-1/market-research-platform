"""Research / backtest-helper layer over the lake.

Alpaca provides *data* and *forward* (live/paper) execution — it has no historical
backtester and none of the data-correctness plumbing a backtest needs. This package
supplies that bridge:

  * loaders   - look-ahead-safe wide/long bar panels, returns, dividends/splits,
                a joined feature frame (bars + news).
  * options   - point-in-time chain snapshots (greeks/IV), ATM/by-delta selection,
                option bar panels.
  * calendar  - trading days inferred from the lake.
  * backtest  - a small, dependency-free vectorized backtester + performance stats.

These return plain pandas, so they also feed external engines (vectorbt, backtrader).
"""
from . import backtest, calendar, loaders, options
from .backtest import performance_stats, vector_backtest
from .loaders import feature_frame, get_bars, get_bars_long, get_returns

__all__ = [
    "backtest", "calendar", "loaders", "options",
    "get_bars", "get_bars_long", "get_returns", "feature_frame",
    "vector_backtest", "performance_stats",
]
