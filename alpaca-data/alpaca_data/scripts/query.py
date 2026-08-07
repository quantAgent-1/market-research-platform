"""Run SQL against the lake, or list available views with row counts.

    python -m alpaca_data.scripts.query
    python -m alpaca_data.scripts.query "SELECT symbol, count(*) FROM stocks_bars GROUP BY 1"
"""
from __future__ import annotations

import argparse

import pandas as pd

from ..store import duckdb_store
from ._common import force_utf8


def main() -> None:
    force_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("sql", nargs="?", help="SQL over the lake views (omit to list views)")
    a = p.parse_args()

    if not a.sql:
        views = duckdb_store.available_views()
        if not views:
            print("No data in the lake yet. Run a backfill first.")
            return
        con = duckdb_store.connect()
        try:
            print("Available views:")
            for v in views:
                try:
                    n = con.execute(f"SELECT count(*) FROM {v}").fetchone()[0]
                except Exception as exc:  # noqa: BLE001
                    n = f"<error: {exc}>"
                print(f"  {v:22} {n:>14,}" if isinstance(n, int) else f"  {v:22} {n}")
        finally:
            con.close()
        return

    df = duckdb_store.query(a.sql)
    with pd.option_context("display.max_rows", 100, "display.max_columns", 50,
                           "display.width", 200):
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
