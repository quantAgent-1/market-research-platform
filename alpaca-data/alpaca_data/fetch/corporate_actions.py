"""Corporate actions (splits, dividends, mergers, ...), back to 2016.

Essential for correct backtest adjustments. The API returns results grouped by
action type; we store one file per (type, year). Pulled in yearly chunks.
"""
from __future__ import annotations

import logging
from datetime import date

import pandas as pd

from .. import catalog
from ..store import write_df
from ..utils import daterange_chunks, parse_date

log = logging.getLogger("alpaca_data.fetch.corporate_actions")

DEFAULT_TYPES = [
    "reverse_split", "forward_split", "unit_split", "cash_dividend", "stock_dividend",
    "spin_off", "cash_merger", "stock_merger", "stock_and_cash_merger", "redemption",
    "name_change", "worthless_removal", "rights_distribution",
]


def fetch_corporate_actions(client, symbols, types=None, start="2016-01-01", end=None,
                            incremental=True):
    start0 = parse_date(start)
    end = parse_date(end) if end else date.today()
    types = types or DEFAULT_TYPES
    symkey = "_".join(sorted(s.upper() for s in symbols)) if symbols else "ALL"
    sym_param = ",".join(s.upper() for s in symbols) if symbols else None
    key = f"corporate_actions/{symkey}"
    lo = max(start0, parse_date(catalog.get_watermark(key))) if (
        incremental and catalog.get_watermark(key)) else start0

    for cs, ce in daterange_chunks(lo, end, "year"):
        by_type: dict[str, list] = {}
        params = {
            "symbols": sym_param, "types": ",".join(types),
            "start": cs.isoformat(), "end": ce.isoformat(), "limit": 1000, "sort": "asc",
        }
        for page in client.paginate("/v1/corporate-actions", params):
            for tname, arr in (page.get("corporate_actions") or {}).items():
                by_type.setdefault(tname, []).extend(arr)
        for tname, arr in by_type.items():
            if not arr:
                continue
            df = pd.DataFrame(arr)
            df["corporate_action_type"] = tname
            write_df(df, "corporate_actions", f"ctype={tname}", f"year={cs.year}", filename=f"{symkey}.parquet")
        total = sum(len(v) for v in by_type.values())
        catalog.set_watermark(key, ce.isoformat())
        log.info("corporate actions %s %s: %d rows across %d types", symkey, cs.year, total, len(by_type))
