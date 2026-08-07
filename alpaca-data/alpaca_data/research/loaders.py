"""Look-ahead-safe data loaders over the lake (stocks side).

All functions return plain pandas. Bar panels come back sorted by time with a
tz-aware UTC index; wide panels are pivoted symbol-by-symbol for easy alignment in
a backtest.
"""
from __future__ import annotations

import re

import pandas as pd

from ..store import duckdb_store

_SYM = re.compile(r"^[A-Z0-9.\-]+$")
_BAR_FIELDS = {"open", "high", "low", "close", "volume", "vwap", "trade_count"}


def _syms(symbols) -> list[str]:
    if isinstance(symbols, str):
        symbols = [symbols]
    out = [str(s).upper() for s in symbols]
    for s in out:
        if not _SYM.match(s):
            raise ValueError(f"invalid symbol {s!r}")
    return out


def _inlist(syms) -> str:
    return ",".join(f"'{s}'" for s in syms)


def _has(view: str) -> bool:
    return view in duckdb_store.available_views()


def get_bars_long(symbols, start=None, end=None, timeframe="1Day") -> pd.DataFrame:
    """Tidy OHLCV bars for the symbols/timeframe/date-range."""
    if not _has("stocks_bars"):
        return pd.DataFrame()
    where = [f"symbol IN ({_inlist(_syms(symbols))})", f"timeframe='{timeframe}'"]
    if start:
        where.append(f"timestamp >= '{start}'")
    if end:
        where.append(f"timestamp <= '{end}'")
    return duckdb_store.query(
        "SELECT symbol, timestamp, open, high, low, close, volume, vwap, trade_count "
        f"FROM stocks_bars WHERE {' AND '.join(where)} ORDER BY symbol, timestamp"
    )


def get_bars(symbols, start=None, end=None, timeframe="1Day", field="close") -> pd.DataFrame:
    """Wide panel: index=timestamp, columns=symbol, values=`field`."""
    if field not in _BAR_FIELDS:
        raise ValueError(f"field must be one of {sorted(_BAR_FIELDS)}")
    long = get_bars_long(symbols, start, end, timeframe)
    if long.empty:
        return pd.DataFrame()
    return long.pivot_table(index="timestamp", columns="symbol", values=field, aggfunc="last").sort_index()


def get_returns(symbols, start=None, end=None, timeframe="1Day", field="close") -> pd.DataFrame:
    """Simple period returns, wide. (pct_change of the price panel.)"""
    px = get_bars(symbols, start, end, timeframe, field)
    return px.pct_change().dropna(how="all") if not px.empty else px


def get_dividends(symbols=None, start=None, end=None) -> pd.DataFrame:
    """Cash dividends from the corporate-actions lake (tidy)."""
    return _corp_actions("cash_dividend", symbols, start, end)


def get_splits(symbols=None, start=None, end=None) -> pd.DataFrame:
    """Forward + reverse splits from the corporate-actions lake (tidy)."""
    fwd = _corp_actions("forward_split", symbols, start, end)
    rev = _corp_actions("reverse_split", symbols, start, end)
    return pd.concat([fwd, rev], ignore_index=True) if len(fwd) or len(rev) else fwd


def _corp_actions(type_prefix, symbols, start, end) -> pd.DataFrame:
    if not _has("corporate_actions"):
        return pd.DataFrame()
    where = [f"corporate_action_type LIKE '{type_prefix}%'"]
    if symbols:
        where.append(f"symbol IN ({_inlist(_syms(symbols))})")
    df = duckdb_store.query(f"SELECT * FROM corporate_actions WHERE {' AND '.join(where)}")
    if df.empty or "ex_date" not in df.columns:
        return df
    if start:
        df = df[df["ex_date"] >= str(start)]
    if end:
        df = df[df["ex_date"] <= str(end)]
    return df.sort_values("ex_date").reset_index(drop=True)


def daily_news_count(symbols, start=None, end=None) -> pd.DataFrame:
    """Per (symbol, date) article counts, from the news lake."""
    if not _has("news"):
        return pd.DataFrame(columns=["symbol", "date", "news_count"])
    want = set(_syms(symbols))
    where = ["symbols IS NOT NULL"]
    if start:
        where.append(f"created_at >= '{start}'")
    if end:
        where.append(f"created_at <= '{end}'")
    df = duckdb_store.query(f"SELECT created_at, symbols FROM news WHERE {' AND '.join(where)}")
    if df.empty:
        return pd.DataFrame(columns=["symbol", "date", "news_count"])
    df["date"] = pd.to_datetime(df["created_at"], utc=True).dt.date
    df = df.assign(symbol=df["symbols"].str.split(",")).explode("symbol")
    df = df[df["symbol"].isin(want)]
    return (df.groupby(["symbol", "date"]).size()
            .rename("news_count").reset_index())


def feature_frame(symbols, start=None, end=None) -> pd.DataFrame:
    """Daily bars joined with same-day news counts on (symbol, date) — a research panel."""
    bars = get_bars_long(symbols, start, end, "1Day")
    if bars.empty:
        return bars
    bars["date"] = pd.to_datetime(bars["timestamp"], utc=True).dt.date
    nc = daily_news_count(symbols, start, end)
    if nc.empty:
        bars["news_count"] = 0
        return bars
    out = bars.merge(nc, on=["symbol", "date"], how="left")
    out["news_count"] = out["news_count"].fillna(0).astype(int)
    return out
