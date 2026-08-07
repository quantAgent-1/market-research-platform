"""Backfill historical stock data into the lake.

    python -m alpaca_data.scripts.backfill_stocks --universe default:ai_semis --timeframe 1Day
    python -m alpaca_data.scripts.backfill_stocks --symbols NVDA --data trades,quotes --start 2025-01-02 --end 2025-01-03
"""
from __future__ import annotations

import argparse

from ..fetch import stocks
from ._common import add_symbol_args, make_client, resolve_symbols, setup_logging


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    add_symbol_args(p)
    p.add_argument("--data", default="bars", help="comma list: bars,trades,quotes,auctions")
    p.add_argument("--timeframe", default="1Day", help="bar timeframe, e.g. 1Day, 1Hour, 5Min")
    p.add_argument("--start", default="2016-01-01")
    p.add_argument("--end", default=None, help="default: today")
    p.add_argument("--no-incremental", action="store_true",
                   help="ignore catalog watermark and refetch the whole range")
    a = p.parse_args()
    setup_logging(a.log)

    syms = resolve_symbols(a)
    inc = not a.no_incremental
    kinds = [x.strip() for x in a.data.split(",") if x.strip()]
    c = make_client()
    print(f"Backfilling stock {kinds} for {len(syms)} symbols: {syms}")
    if {"trades", "quotes"} & set(kinds):
        print("  NOTE: trades/quotes are tick data - large. Use a narrow --start/--end.")

    if "bars" in kinds:
        stocks.fetch_bars(c, syms, a.timeframe, a.start, a.end, incremental=inc)
    if "trades" in kinds:
        stocks.fetch_trades(c, syms, a.start, a.end, incremental=inc)
    if "quotes" in kinds:
        stocks.fetch_quotes(c, syms, a.start, a.end, incremental=inc)
    if "auctions" in kinds:
        stocks.fetch_auctions(c, syms, a.start, a.end, incremental=inc)
    print("Done.")


if __name__ == "__main__":
    main()
