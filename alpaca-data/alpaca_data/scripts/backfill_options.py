"""Backfill historical option data into the lake.

Discover contracts first (so expired contracts are on disk), then pull bars /
chain snapshots / tick. Options history starts Feb 2024.

    python -m alpaca_data.scripts.backfill_options --universe default:ai_semis --data contracts,bars,chain
    python -m alpaca_data.scripts.backfill_options --symbols NVDA --data trades,quotes \
        --exp-gte 2025-01-01 --exp-lte 2025-03-31 --start 2025-01-02 --end 2025-01-03
"""
from __future__ import annotations

import argparse

from ..fetch import contracts, options
from ._common import add_symbol_args, make_client, resolve_symbols, setup_logging


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    add_symbol_args(p)
    p.add_argument("--data", default="contracts,chain",
                   help="comma list: contracts,bars,chain,trades,quotes")
    p.add_argument("--timeframe", default="1Day")
    p.add_argument("--start", default="2024-02-01")
    p.add_argument("--end", default=None)
    p.add_argument("--exp-gte", default=None, help="expiration_date >= (YYYY-MM-DD) filter")
    p.add_argument("--exp-lte", default=None, help="expiration_date <= (YYYY-MM-DD) filter")
    p.add_argument("--no-incremental", action="store_true")
    a = p.parse_args()
    setup_logging(a.log)

    unders = resolve_symbols(a)
    inc = not a.no_incremental
    kinds = [x.strip() for x in a.data.split(",") if x.strip()]
    c = make_client()
    print(f"Backfilling option {kinds} for underlyings: {unders}")

    if "contracts" in kinds:
        contracts.fetch_contracts(c, unders, expiration_gte=a.exp_gte, expiration_lte=a.exp_lte)
    if "bars" in kinds:
        options.fetch_bars(c, unders, a.timeframe, a.start, a.end, incremental=inc,
                           expiration_gte=a.exp_gte, expiration_lte=a.exp_lte)
    if "chain" in kinds:
        for u in unders:
            options.fetch_chain(c, u, expiration_date_gte=a.exp_gte, expiration_date_lte=a.exp_lte)
    if "quotes" in kinds:
        print("  NOTE: Alpaca has no historical option-quotes endpoint. Use --data chain "
              "(snapshots with NBBO + greeks/IV) or the live stream. Skipping quotes.")
    if "trades" in kinds:
        for u in unders:
            syms = contracts.load_contract_symbols(u, expiration_gte=a.exp_gte, expiration_lte=a.exp_lte)
            if not syms:
                print(f"  {u}: no contracts on disk - run with --data contracts first. Skipping.")
                continue
            print(f"  {u}: {len(syms)} contracts for trades pull (this is MANY requests).")
            options.fetch_trades(c, syms, a.start, a.end, incremental=inc)
    print("Done.")


if __name__ == "__main__":
    main()
