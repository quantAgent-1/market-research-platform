"""Option-contract discovery via the Trading API (/v2/options/contracts).

This is the only way to enumerate *expired* contracts (the market-data chain
endpoint only returns currently-active ones), so it's required to backfill
historical option bars/quotes since Feb 2024. Reference data is written to
options/contracts/underlying=<U>/data.parquet and read back by the option fetcher.
"""
from __future__ import annotations

import logging

import pandas as pd

from ..config import get_settings
from ..store import partition_path, read_df, write_df

log = logging.getLogger("alpaca_data.fetch.contracts")

_NUMERIC = ("strike_price", "close_price", "size", "open_interest")


def fetch_contracts(client, underlyings, *, expiration_gte=None, expiration_lte=None,
                    statuses=("active", "inactive"), type=None,
                    strike_gte=None, strike_lte=None):
    """Discover and store option contracts for each underlying.

    `statuses` defaults to both active and inactive (inactive == expired/delisted)
    so the historical universe is complete.
    """
    s = get_settings()
    out: dict[str, pd.DataFrame] = {}
    for u in (x.upper() for x in underlyings):
        rows: list = []
        for status in statuses:
            params = {
                "underlying_symbols": u, "status": status, "limit": 10000,
                "expiration_date_gte": expiration_gte, "expiration_date_lte": expiration_lte,
                "type": type, "strike_price_gte": strike_gte, "strike_price_lte": strike_lte,
            }
            for page in client.paginate("/v2/options/contracts", params, base=s.trading_url):
                rows.extend(page.get("option_contracts") or [])
        if not rows:
            log.info("contracts %s: none", u)
            continue
        df = pd.DataFrame(rows).drop_duplicates(subset="symbol")
        for c in _NUMERIC:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        write_df(df, "options", "contracts", f"underlying={u}")
        out[u] = df
        log.info("contracts %s: %d (active+inactive)", u, len(df))
    return out


def load_contract_symbols(underlying, *, expiration_gte=None, expiration_lte=None,
                          type=None) -> list[str]:
    """Read previously-discovered contract symbols for an underlying from the lake."""
    path = partition_path("options", "contracts", f"underlying={underlying.upper()}")
    if not path.exists():
        return []
    df = read_df(path)
    if "expiration_date" in df.columns:
        if expiration_gte is not None:
            df = df[df["expiration_date"] >= str(expiration_gte)]
        if expiration_lte is not None:
            df = df[df["expiration_date"] <= str(expiration_lte)]
    if type and "type" in df.columns:
        df = df[df["type"] == type]
    return df["symbol"].astype(str).tolist()
