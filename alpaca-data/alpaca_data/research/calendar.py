"""Trading calendar inferred from the lake (no external calendar dependency).

Uses the distinct dates present in daily bars, so it reflects exactly the sessions
your data covers (holidays/half-days included naturally).
"""
from __future__ import annotations

import pandas as pd

from ..store import duckdb_store


def trading_days(start=None, end=None) -> pd.DatetimeIndex:
    if "stocks_bars" not in duckdb_store.available_views():
        return pd.DatetimeIndex([])
    where = ["timeframe='1Day'"]
    if start:
        where.append(f"timestamp >= '{start}'")
    if end:
        where.append(f"timestamp <= '{end}'")
    sql = f"SELECT DISTINCT timestamp::date AS d FROM stocks_bars WHERE {' AND '.join(where)} ORDER BY d"
    df = duckdb_store.query(sql)
    return pd.DatetimeIndex(pd.to_datetime(df["d"])) if len(df) else pd.DatetimeIndex([])
