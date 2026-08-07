"""Capture real-time market data into the lake (Ctrl+C to stop).

    python -m alpaca_data.scripts.stream_live --asset stocks --universe default:ai_semis
    python -m alpaca_data.scripts.stream_live --asset options --symbols NVDA250620C00130000,NVDA250620P00130000

One process streams one asset class (each stream.run() blocks). Run two terminals
for stocks + options simultaneously. Markets must be open to see messages.
"""
from __future__ import annotations

import argparse
import sys

from ..stream import StreamRecorder
from ._common import add_symbol_args, load_universe, resolve_symbols, setup_logging


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--asset", choices=["stocks", "options"], default="stocks")
    add_symbol_args(p)
    p.add_argument("--kinds", default="bars,trades,quotes", help="comma list of channels")
    p.add_argument("--flush-interval", type=float, default=10.0)
    p.add_argument("--max-rows", type=int, default=5000)
    a = p.parse_args()
    setup_logging(a.log)

    kinds = tuple(x.strip() for x in a.kinds.split(",") if x.strip())
    rec = StreamRecorder(flush_interval=a.flush_interval, max_rows=a.max_rows)

    if a.asset == "stocks":
        rec.run_stocks(resolve_symbols(a), kinds)
    else:
        if not a.symbols:
            print("options streaming needs explicit OCC contract symbols via --symbols", file=sys.stderr)
            return 2
        rec.run_options(load_universe(a.symbols), kinds)
    return 0


if __name__ == "__main__":
    sys.exit(main())
