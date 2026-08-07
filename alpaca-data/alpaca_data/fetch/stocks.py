"""Historical stock data: bars, trades, quotes, auctions (SIP).

Bars chunk by year (daily/weekly/monthly) or month (intraday). Trades/quotes are
tick data and chunk by *day* (one file per symbol-day). All pulls are incremental
via the catalog watermark.
"""
from __future__ import annotations

import json
import logging
from datetime import date

import pandas as pd

from .. import catalog
from ..config import get_settings
from ..frames import normalize
from ..store import write_df
from ..utils import daterange_chunks, day_end, day_start, parse_date, to_rfc3339

log = logging.getLogger("alpaca_data.fetch.stocks")


def _chunk_for(timeframe: str) -> str:
    return "month" if ("Min" in timeframe or "Hour" in timeframe) else "year"


def _collect(client, path: str, params: dict, data_key: str, symbol: str) -> list:
    """Paginate `path`, accumulating records for one symbol across pages."""
    recs: list = []
    for page in client.paginate(path, params):
        recs.extend((page.get(data_key) or {}).get(symbol, []))
    return recs


def fetch_bars(client, symbols, timeframe="1Day", start="2016-01-01", end=None,
               adjustment="all", feed=None, incremental=True):
    """OHLCV bars. adjustment in {raw, split, dividend, all} (default all = backtest-safe)."""
    s = get_settings()
    feed = feed or s.stock_feed
    start0 = parse_date(start)
    end = parse_date(end) if end else date.today()
    chunk = _chunk_for(timeframe)

    for sym in (x.upper() for x in symbols):
        key = f"stocks/bars/{timeframe}/{sym}"
        lo = max(start0, parse_date(catalog.get_watermark(key))) if (
            incremental and catalog.get_watermark(key)) else start0
        total = 0
        for cs, ce in daterange_chunks(lo, end, chunk):
            params = {
                "symbols": sym, "timeframe": timeframe,
                "start": to_rfc3339(day_start(cs)), "end": to_rfc3339(day_end(ce)),
                "adjustment": adjustment, "feed": feed, "limit": 10000, "sort": "asc",
            }
            df = normalize(_collect(client, "/v2/stocks/bars", params, "bars", sym), "bars", symbol=sym)
            if len(df):
                df["timeframe"] = timeframe
                df["adjustment"] = adjustment
                parts = ["stocks", "bars", f"timeframe={timeframe}", f"symbol={sym}", f"year={cs.year}"]
                if chunk == "month":
                    parts.append(f"month={cs.month:02d}")
                write_df(df, *parts)
                total += len(df)
            catalog.set_watermark(key, ce.isoformat())
        log.info("stocks bars %s [%s]: %d rows (%s..%s)", sym, timeframe, total, lo, end)


def _fetch_tick(client, symbols, kind, path, start, end, feed, incremental):
    s = get_settings()
    feed = feed or s.stock_feed
    start0 = parse_date(start)
    end = parse_date(end) if end else date.today()

    for sym in (x.upper() for x in symbols):
        key = f"stocks/{kind}/{sym}"
        lo = max(start0, parse_date(catalog.get_watermark(key))) if (
            incremental and catalog.get_watermark(key)) else start0
        for cs, _ in daterange_chunks(lo, end, "day"):
            if cs.weekday() >= 5:  # skip weekends (no tape)
                continue
            params = {
                "symbols": sym, "start": to_rfc3339(day_start(cs)), "end": to_rfc3339(day_end(cs)),
                "feed": feed, "limit": 10000, "sort": "asc",
            }
            df = normalize(_collect(client, path, params, kind, sym), kind, symbol=sym)
            if len(df):
                write_df(df, "stocks", kind, f"symbol={sym}", f"date={cs.isoformat()}")
            catalog.set_watermark(key, cs.isoformat())
        log.info("stocks %s %s: done (%s..%s)", kind, sym, lo, end)


def fetch_trades(client, symbols, start, end=None, feed=None, incremental=True):
    """Tick trades (the tape). Large — one file per symbol-day."""
    _fetch_tick(client, symbols, "trades", "/v2/stocks/trades", start, end, feed, incremental)


def fetch_quotes(client, symbols, start, end=None, feed=None, incremental=True):
    """Tick NBBO quotes. Very large — one file per symbol-day."""
    _fetch_tick(client, symbols, "quotes", "/v2/stocks/quotes", start, end, feed, incremental)


def fetch_auctions(client, symbols, start="2016-01-01", end=None, incremental=True):
    """Daily opening/closing auction prices (SIP only). Stored as JSON per day."""
    start0 = parse_date(start)
    end = parse_date(end) if end else date.today()
    for sym in (x.upper() for x in symbols):
        key = f"stocks/auctions/{sym}"
        lo = max(start0, parse_date(catalog.get_watermark(key))) if (
            incremental and catalog.get_watermark(key)) else start0
        for cs, ce in daterange_chunks(lo, end, "year"):
            params = {
                "symbols": sym, "start": to_rfc3339(day_start(cs)), "end": to_rfc3339(day_end(ce)),
                "feed": "sip", "limit": 10000, "sort": "asc",
            }
            recs = _collect(client, "/v2/stocks/auctions", params, "auctions", sym)
            rows = [{"symbol": sym, "date": r.get("d"),
                     "opening": json.dumps(r.get("o")), "closing": json.dumps(r.get("c"))}
                    for r in recs]
            df = pd.DataFrame(rows)
            if len(df):
                write_df(df, "stocks", "auctions", f"symbol={sym}", f"year={cs.year}")
            catalog.set_watermark(key, ce.isoformat())
        log.info("stocks auctions %s: done (%s..%s)", sym, lo, end)
