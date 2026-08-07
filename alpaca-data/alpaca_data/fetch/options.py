"""Historical option data (OPRA): chain snapshots (greeks/IV), bars, trades, quotes.

Bars are pulled per *underlying* (batching its contracts ≤100/request) and stored
one file per underlying-year. Trades/quotes are tick data and are pulled per
*contract* per day. The chain endpoint returns point-in-time snapshots with greeks
+ implied vol — run it daily to accumulate a vol-surface history.

Discover contracts first (see fetch.contracts) so the historical/expired universe
is available on disk.
"""
from __future__ import annotations

import logging
from datetime import date

import pandas as pd

from .. import catalog
from ..config import get_settings
from ..frames import normalize
from ..store import write_df
from ..utils import (batched, daterange_chunks, day_end, day_start, is_occ,
                     parse_date, parse_occ, to_rfc3339)
from . import contracts as contracts_mod

log = logging.getLogger("alpaca_data.fetch.options")

OPT = "/v1beta1/options"


def _augment_occ(df: pd.DataFrame) -> pd.DataFrame:
    """Add underlying/expiration/opt_type/strike columns parsed from OCC symbols."""
    if "symbol" not in df.columns:
        return df
    parsed = df["symbol"].map(lambda x: parse_occ(x) if is_occ(str(x)) else None)
    df["underlying"] = parsed.map(lambda c: c.underlying if c else None)
    df["expiration"] = parsed.map(lambda c: c.expiration if c else None)
    df["opt_type"] = parsed.map(lambda c: c.type if c else None)
    df["strike"] = parsed.map(lambda c: c.strike if c else None)
    return df


def fetch_bars(client, underlyings, timeframe="1Day", start="2024-02-01", end=None,
               feed=None, incremental=True, contract_filter=None,
               expiration_gte=None, expiration_lte=None):
    """Option bars per underlying. Requires contracts discovered on disk first.

    expiration_gte/lte scope which contracts (by expiration date) are pulled —
    keep these tight to bound the request count and storage.
    """
    s = get_settings()
    feed = feed or s.options_feed
    start0 = parse_date(start)
    end = parse_date(end) if end else date.today()
    chunk = "month" if ("Min" in timeframe or "Hour" in timeframe) else "year"

    for u in (x.upper() for x in underlyings):
        syms = contracts_mod.load_contract_symbols(
            u, expiration_gte=expiration_gte, expiration_lte=expiration_lte)
        if contract_filter:
            syms = [x for x in syms if contract_filter(x)]
        if not syms:
            log.warning("options bars %s: no contracts on disk — run contract discovery first", u)
            continue
        key = f"options/bars/{timeframe}/{u}"
        lo = max(start0, parse_date(catalog.get_watermark(key))) if (
            incremental and catalog.get_watermark(key)) else start0
        for cs, ce in daterange_chunks(lo, end, chunk):
            merged: dict[str, list] = {}
            for batch in batched(syms, 100):
                params = {
                    "symbols": ",".join(batch), "timeframe": timeframe,
                    "start": to_rfc3339(day_start(cs)), "end": to_rfc3339(day_end(ce)),
                    "limit": 10000, "sort": "asc",
                }  # NOTE: options bars/trades/quotes do NOT accept a `feed` param
                for page in client.paginate(f"{OPT}/bars", params):
                    for sym, recs in (page.get("bars") or {}).items():
                        merged.setdefault(sym, []).extend(recs)
            frames = [normalize(r, "bars", symbol=sym) for sym, r in merged.items() if r]
            if frames:
                df = _augment_occ(pd.concat(frames, ignore_index=True))
                df["timeframe"] = timeframe
                parts = ["options", "bars", f"timeframe={timeframe}", f"underlying={u}", f"year={cs.year}"]
                if chunk == "month":
                    parts.append(f"month={cs.month:02d}")
                write_df(df, *parts)
            catalog.set_watermark(key, ce.isoformat())
        log.info("options bars %s [%s]: done (%s..%s)", u, timeframe, lo, end)


def _fetch_tick(client, contract_symbols, kind, start, end, feed, incremental):
    s = get_settings()
    feed = feed or s.options_feed
    start0 = parse_date(start)
    end = parse_date(end) if end else date.today()
    for sym in contract_symbols:
        u = parse_occ(sym).underlying
        key = f"options/{kind}/{sym}"
        lo = max(start0, parse_date(catalog.get_watermark(key))) if (
            incremental and catalog.get_watermark(key)) else start0
        for cs, _ in daterange_chunks(lo, end, "day"):
            if cs.weekday() >= 5:
                continue
            params = {
                "symbols": sym, "start": to_rfc3339(day_start(cs)), "end": to_rfc3339(day_end(cs)),
                "limit": 10000, "sort": "asc",
            }  # NOTE: options bars/trades/quotes do NOT accept a `feed` param
            recs: list = []
            for page in client.paginate(f"{OPT}/{kind}", params):
                recs.extend((page.get(kind) or {}).get(sym, []))
            df = normalize(recs, kind, symbol=sym)
            if len(df):
                write_df(df, "options", kind, f"underlying={u}", f"contract={sym}", f"date={cs.isoformat()}")
            catalog.set_watermark(key, cs.isoformat())
        log.info("options %s %s: done (%s..%s)", kind, sym, lo, end)


def fetch_trades(client, contract_symbols, start, end=None, feed=None, incremental=True):
    """Tick trades per contract. Pass an explicit list of OCC symbols."""
    _fetch_tick(client, contract_symbols, "trades", start, end, feed, incremental)


def fetch_quotes(client, contract_symbols, start, end=None, feed=None, incremental=True):
    """Unavailable: Alpaca offers no historical option-quotes time-series.

    Use fetch_chain() to snapshot NBBO + greeks/IV (run daily to accumulate a
    history), or the live OPRA WebSocket stream for real-time quotes.
    """
    log.warning("historical option quotes are not offered by Alpaca; use fetch_chain() "
                "snapshots (NBBO + greeks/IV) or the live stream instead. Skipping.")


def _snapshots_to_df(snaps: dict, underlying: str) -> pd.DataFrame:
    rows = []
    for sym, snap in snaps.items():
        row = {"symbol": sym, "underlying": underlying}
        if is_occ(sym):
            c = parse_occ(sym)
            row.update(expiration=c.expiration, opt_type=c.type, strike=c.strike)
        g = snap.get("greeks") or {}
        row.update(delta=g.get("delta"), gamma=g.get("gamma"), theta=g.get("theta"),
                   vega=g.get("vega"), rho=g.get("rho"),
                   implied_volatility=snap.get("impliedVolatility"))
        lq = snap.get("latestQuote") or {}
        row.update(quote_time=lq.get("t"), bid_price=lq.get("bp"), bid_size=lq.get("bs"),
                   ask_price=lq.get("ap"), ask_size=lq.get("as"))
        lt = snap.get("latestTrade") or {}
        row.update(trade_time=lt.get("t"), trade_price=lt.get("p"), trade_size=lt.get("s"))
        db = snap.get("dailyBar") or {}
        row.update(day_open=db.get("o"), day_high=db.get("h"), day_low=db.get("l"),
                   day_close=db.get("c"), day_volume=db.get("v"))
        rows.append(row)
    df = pd.DataFrame(rows)
    for col in ("quote_time", "trade_time"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], utc=True, errors="coerce", format="ISO8601")
    return df


def fetch_chain(client, underlying, *, feed=None, asof=None, **filters):
    """Current option chain snapshot (greeks + IV) for an underlying.

    Optional filters (Alpaca names): type, strike_price_gte, strike_price_lte,
    expiration_date, expiration_date_gte, expiration_date_lte, root_symbol,
    updated_since. Writes options/snapshots/underlying=<U>/asof=<date>/data.parquet.
    """
    s = get_settings()
    feed = feed or s.options_feed
    u = underlying.upper()
    params = {"feed": feed, "limit": 1000}
    params.update({k: v for k, v in filters.items() if v is not None})
    snaps: dict = {}
    for page in client.paginate(f"{OPT}/snapshots/{u}", params):
        snaps.update(page.get("snapshots") or {})
    df = _snapshots_to_df(snaps, u)
    asof = asof or date.today().isoformat()
    if len(df):
        df["asof"] = asof
        write_df(df, "options", "snapshots", f"underlying={u}", f"asof={asof}")
    log.info("options chain %s @ %s: %d contracts", u, asof, len(df))
    return df
