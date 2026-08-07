"""Backfill historical news (back to 2015).

    python -m alpaca_data.scripts.backfill_news --symbols NVDA,AMD --start 2023-01-01
    python -m alpaca_data.scripts.backfill_news            # entire firehose (no symbol filter)
"""
from __future__ import annotations

import argparse

from ..fetch import news
from ._common import load_universe, make_client, setup_logging


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--symbols", help="comma-separated tickers; omit for the full firehose")
    p.add_argument("--universe", help="universe file[:group]")
    p.add_argument("--start", default="2015-01-01")
    p.add_argument("--end", default=None)
    p.add_argument("--no-content", action="store_true", help="don't fetch full article bodies")
    p.add_argument("--exclude-contentless", action="store_true")
    p.add_argument("--log", default="INFO")
    a = p.parse_args()
    setup_logging(a.log)

    spec = a.symbols or a.universe
    syms = load_universe(spec) if spec else None
    c = make_client()
    print(f"Backfilling news for {syms or 'ALL symbols'} from {a.start}")
    news.fetch_news(c, syms, a.start, a.end,
                    include_content=not a.no_content,
                    exclude_contentless=a.exclude_contentless)
    print("Done.")


if __name__ == "__main__":
    main()
