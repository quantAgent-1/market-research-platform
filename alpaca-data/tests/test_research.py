"""Pure-logic tests for the research/backtest helpers (no network, no lake).

    python tests/test_research.py     # from the alpaca-data/ directory
"""
from __future__ import annotations

import sys

import pandas as pd

from alpaca_data.research.backtest import performance_stats, vector_backtest
from alpaca_data.research.loaders import _syms


def _idx(n):
    return pd.date_range("2024-01-01", periods=n, freq="D")


def test_syms_sanitize():
    assert _syms("nvda") == ["NVDA"]
    assert _syms(["a", "BRK.B"]) == ["A", "BRK.B"]
    try:
        _syms("DROP TABLE")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for an invalid symbol")


def test_perf_stats_basic():
    assert performance_stats(pd.Series([], dtype=float)) == {}
    # all-positive constant series: no drawdown, perfect hit rate
    # (Sharpe is nan here by design — zero volatility — so we don't assert on it)
    pos = pd.Series([0.01] * 252, index=_idx(252))
    sp = performance_stats(pos)
    assert sp["cagr"] > 0
    assert sp["max_drawdown"] == 0.0
    assert sp["hit_rate"] == 1.0
    # noisy but upward-drifting: finite positive Sharpe, some drawdown
    noisy = pd.Series([0.02, -0.01] * 126, index=_idx(252))
    sn = performance_stats(noisy)
    assert sn["sharpe"] > 0
    assert sn["max_drawdown"] < 0.0


def test_backtest_buy_and_hold():
    px = pd.DataFrame({"A": [100, 101, 102, 103, 104]}, index=_idx(5))
    w = pd.DataFrame({"A": [1.0] * 5}, index=_idx(5))
    res = vector_backtest(px, w, cost_bps=0.0)
    assert abs(res["equity"].iloc[-1] - 1.04) < 1e-9


def test_backtest_no_lookahead():
    # +10% spike at t2 (known only at close t2); a weight set at t2 must NOT capture it
    px = pd.DataFrame({"A": [100, 100, 110, 100, 100]}, index=_idx(5))
    w = pd.DataFrame({"A": [0.0, 0.0, 1.0, 0.0, 0.0]}, index=_idx(5))
    res = vector_backtest(px, w, cost_bps=0.0)
    assert res["gross_return"].iloc[2] == 0.0    # no same-day capture of the spike
    assert res["gross_return"].iloc[3] < 0.0     # holds into t3's drop instead


def test_backtest_costs_drag():
    px = pd.DataFrame({"A": [100.0] * 5, "B": [100.0] * 5}, index=_idx(5))
    w = pd.DataFrame({"A": [1.0, 0.0, 1.0, 0.0, 1.0],
                      "B": [0.0, 1.0, 0.0, 1.0, 0.0]}, index=_idx(5))
    res = vector_backtest(px, w, cost_bps=100.0)  # flat prices => only costs move equity
    assert res["equity"].iloc[-1] < 1.0
    assert res["turnover"].sum() > 0


def _run() -> int:
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS {t.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {t.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run())
