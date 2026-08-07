"""Convert raw Alpaca JSON records into tidy, schema-stable pandas DataFrames.

Alpaca returns terse field names (t, o, h, l, c, v, ...). We rename to readable
columns and force a *canonical, stable* column set per record kind so every
partition file shares one schema (important for DuckDB's union reads). Shared by
both the stock and option fetchers — the field names match across asset classes.
"""
from __future__ import annotations

import pandas as pd

_RENAME = {
    "bars": {
        "t": "timestamp", "o": "open", "h": "high", "l": "low", "c": "close",
        "v": "volume", "n": "trade_count", "vw": "vwap",
    },
    "trades": {
        "t": "timestamp", "x": "exchange", "p": "price", "s": "size",
        "c": "conditions", "i": "id", "z": "tape", "u": "update",
    },
    "quotes": {
        "t": "timestamp", "ax": "ask_exchange", "ap": "ask_price", "as": "ask_size",
        "bx": "bid_exchange", "bp": "bid_price", "bs": "bid_size",
        "c": "conditions", "z": "tape",
    },
}

_COLUMNS = {
    "bars": ["symbol", "timestamp", "open", "high", "low", "close",
             "volume", "trade_count", "vwap"],
    "trades": ["symbol", "timestamp", "exchange", "price", "size",
               "conditions", "id", "tape"],
    "quotes": ["symbol", "timestamp", "ask_exchange", "ask_price", "ask_size",
               "bid_exchange", "bid_price", "bid_size", "conditions", "tape"],
}


def _join_conditions(v):
    if isinstance(v, list):
        return ",".join(str(x) for x in v)
    return v if (v is not None and not (isinstance(v, float) and pd.isna(v))) else None


def normalize(records: list[dict], kind: str, symbol: str | None = None) -> pd.DataFrame:
    """records -> DataFrame with the canonical columns for `kind`.

    `kind` in {"bars", "trades", "quotes"}. `symbol` is stamped onto every row.
    """
    cols = _COLUMNS[kind]
    if not records:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(records).rename(columns=_RENAME[kind])
    if symbol is not None:
        df["symbol"] = symbol
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="ISO8601")
    if "conditions" in df.columns:
        df["conditions"] = df["conditions"].map(_join_conditions)
    return df.reindex(columns=cols)
