"""Point-in-time option helpers over the lake.

`get_chain`/`atm_contract` read the stored chain *snapshots* (greeks + IV captured
as-of a date — run `backfill_options --data chain` daily to accumulate history).
`get_option_bars` returns option price bars with parsed strike/expiry/type columns.
"""
from __future__ import annotations

import pandas as pd

from ..store import duckdb_store
from .loaders import _inlist, _syms


def _has(view: str) -> bool:
    return view in duckdb_store.available_views()


def snapshot_dates(underlying: str) -> list[str]:
    """As-of dates available for an underlying's chain snapshots."""
    if not _has("options_snapshots"):
        return []
    df = _with_asof(duckdb_store.query(
        f"SELECT * FROM options_snapshots WHERE underlying='{underlying.upper()}'"))
    return sorted(df["asof"].dropna().unique().tolist()) if not df.empty else []


def _with_asof(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    if "asof" not in df.columns or df["asof"].isna().all():
        # fall back to parsing the partition path (snapshots written before the asof column)
        df = df.copy()
        df["asof"] = df["filename"].str.extract(r"asof=([0-9-]+)")[0] if "filename" in df.columns else None
    return df


def get_chain(underlying: str, asof=None) -> pd.DataFrame:
    """Chain snapshot (greeks/IV) for an underlying as-of a date (latest if None)."""
    if not _has("options_snapshots"):
        return pd.DataFrame()
    df = _with_asof(duckdb_store.query(
        f"SELECT * FROM options_snapshots WHERE underlying='{underlying.upper()}'"))
    if df.empty:
        return df
    asof = str(asof) if asof is not None else df["asof"].max()
    return df[df["asof"] == asof].reset_index(drop=True)


def atm_contract(underlying, asof=None, right="call", by="delta", target=0.5):
    """Pick the contract closest to `target` on column `by` (delta or strike).

    Returns a one-row Series (the contract snapshot) or None. Defaults to the
    ~50-delta call. For ATM-by-moneyness use by="strike", target=<spot>.
    """
    chain = get_chain(underlying, asof)
    if chain.empty or "opt_type" not in chain.columns:
        return None
    chain = chain[chain["opt_type"] == right]
    if by not in chain.columns:
        return None
    chain = chain.dropna(subset=[by])
    if chain.empty:
        return None
    return chain.assign(_dist=(chain[by] - target).abs()).sort_values("_dist").iloc[0]


def get_option_bars(underlying=None, contracts=None, start=None, end=None,
                    timeframe="1Day") -> pd.DataFrame:
    """Option price bars (long) with parsed underlying/expiration/opt_type/strike."""
    if not _has("options_bars"):
        return pd.DataFrame()
    where = [f"timeframe='{timeframe}'"]
    if underlying:
        where.append(f"underlying='{underlying.upper()}'")
    if contracts:
        where.append(f"symbol IN ({_inlist(_syms(contracts))})")
    if start:
        where.append(f"timestamp >= '{start}'")
    if end:
        where.append(f"timestamp <= '{end}'")
    return duckdb_store.query(
        "SELECT symbol, underlying, expiration, opt_type, strike, timestamp, "
        "open, high, low, close, volume, vwap "
        f"FROM options_bars WHERE {' AND '.join(where)} ORDER BY symbol, timestamp"
    )
