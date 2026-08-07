"""Backfill corporate actions (splits, dividends, mergers, ...), back to 2016.

    python -m alpaca_data.scripts.backfill_corpactions --universe default:ai_semis
    python -m alpaca_data.scripts.backfill_corpactions --symbols AAPL --types forward_split,cash_dividend
"""
from __future__ import annotations

import argparse

from ..fetch import corporate_actions
from ._common import load_universe, make_client, setup_logging


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--symbols", help="comma-separated tickers; omit for all symbols")
    p.add_argument("--universe", help="universe file[:group]")
    p.add_argument("--types", default=None, help="comma list of action types (default: all common)")
    p.add_argument("--start", default="2016-01-01")
    p.add_argument("--end", default=None)
    p.add_argument("--no-incremental", action="store_true")
    p.add_argument("--log", default="INFO")
    a = p.parse_args()
    setup_logging(a.log)

    spec = a.symbols or a.universe
    syms = load_universe(spec) if spec else None
    types = [x.strip() for x in a.types.split(",")] if a.types else None
    c = make_client()
    print(f"Backfilling corporate actions for {syms or 'ALL symbols'}")
    corporate_actions.fetch_corporate_actions(
        c, syms, types=types, start=a.start, end=a.end, incremental=not a.no_incremental)
    print("Done.")


if __name__ == "__main__":
    main()
