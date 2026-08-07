"""Demo: a simple momentum backtest on the AI-semi daily bars in the lake.

    python -m alpaca_data.scripts.demo_backtest

Strategy: rank by trailing 63-day return, hold the top 3 equal-weight, rebalance
weekly, 5 bps per-side cost. Benchmark: equal-weight buy & hold. Requires daily
bars (run: backfill_stocks --universe default:ai_semis --timeframe 1Day).
"""
from __future__ import annotations

import pandas as pd

from ..research import backtest, loaders
from ._common import force_utf8, load_universe


def _print_stats(title: str, stats: dict) -> None:
    print(title)
    if not stats:
        print("  (no data)")
        return
    for k, v in stats.items():
        print(f"  {k:13} {v:>10.4f}" if isinstance(v, float) else f"  {k:13} {v:>10}")


def main() -> None:
    force_utf8()
    syms = load_universe("default:ai_semis")
    px = loaders.get_bars(syms, start="2018-01-01", timeframe="1Day", field="close")
    if px.empty:
        print("No daily bars in the lake. Run:")
        print("  python -m alpaca_data.scripts.backfill_stocks --universe default:ai_semis --timeframe 1Day")
        return
    px = px.dropna(how="all")

    lookback, topk = 63, 3
    mom = px.pct_change(lookback)
    target = (mom.rank(axis=1, ascending=False) <= topk).astype(float)
    target = target.div(target.sum(axis=1).replace(0.0, pd.NA), axis=0).fillna(0.0)
    # rebalance weekly (Mondays), hold in between
    w = target.copy()
    w.loc[px.index.weekday != 0] = pd.NA
    w = w.ffill().fillna(0.0)

    strat = backtest.vector_backtest(px, w, cost_bps=5.0)
    bench_w = pd.DataFrame(1.0 / px.shape[1], index=px.index, columns=px.columns)
    bench = backtest.vector_backtest(px, bench_w, cost_bps=0.0)

    print(f"Backtest window: {px.index.min().date()} -> {px.index.max().date()} "
          f"({px.shape[1]} names)\n")
    _print_stats("Momentum (63d, top-3 EW, weekly, 5bps):",
                 backtest.performance_stats(strat["net_return"]))
    print()
    _print_stats("Benchmark (equal-weight buy & hold):",
                 backtest.performance_stats(bench["net_return"]))


if __name__ == "__main__":
    main()
