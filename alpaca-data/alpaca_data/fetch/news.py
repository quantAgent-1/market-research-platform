"""Historical news (Benzinga via Alpaca), back to 2015.

Pulled in yearly chunks, partitioned by the article's created_at year/month. Pass
`symbols=None` to fetch the entire firehose, or a list to filter by ticker.
"""
from __future__ import annotations

import json
import logging
from datetime import date

import pandas as pd

from .. import catalog
from ..store import write_df
from ..utils import daterange_chunks, day_end, day_start, parse_date, to_rfc3339

log = logging.getLogger("alpaca_data.fetch.news")


def _news_df(items: list) -> pd.DataFrame:
    rows = [{
        "id": it.get("id"), "created_at": it.get("created_at"), "updated_at": it.get("updated_at"),
        "headline": it.get("headline"), "author": it.get("author"), "source": it.get("source"),
        "summary": it.get("summary"), "content": it.get("content"), "url": it.get("url"),
        "symbols": ",".join(it.get("symbols") or []),
        "images": json.dumps(it.get("images") or []),
    } for it in items]
    df = pd.DataFrame(rows)
    for c in ("created_at", "updated_at"):
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], utc=True, errors="coerce", format="ISO8601")
    return df


def fetch_news(client, symbols=None, start="2015-01-01", end=None,
               include_content=True, exclude_contentless=False, incremental=True):
    start0 = parse_date(start)
    end = parse_date(end) if end else date.today()
    symkey = "_".join(sorted(s.upper() for s in symbols)) if symbols else "ALL"
    sym_param = ",".join(s.upper() for s in symbols) if symbols else None
    key = f"news/{symkey}"
    lo = max(start0, parse_date(catalog.get_watermark(key))) if (
        incremental and catalog.get_watermark(key)) else start0

    for cs, ce in daterange_chunks(lo, end, "year"):
        items: list = []
        params = {
            "symbols": sym_param, "start": to_rfc3339(day_start(cs)), "end": to_rfc3339(day_end(ce)),
            "limit": 50, "sort": "asc",
            "include_content": str(include_content).lower(),
            "exclude_contentless": str(exclude_contentless).lower(),
        }
        for page in client.paginate("/v1beta1/news", params):
            items.extend(page.get("news") or [])
        df = _news_df(items)
        if len(df):
            df = df.dropna(subset=["created_at"])
            for (yr, mo), sub in df.groupby([df["created_at"].dt.year, df["created_at"].dt.month]):
                write_df(sub, "news", f"year={yr}", f"month={int(mo):02d}", filename=f"{symkey}.parquet")
        catalog.set_watermark(key, ce.isoformat())
        log.info("news %s %s..%s: %d items", symkey, cs, ce, len(df))
