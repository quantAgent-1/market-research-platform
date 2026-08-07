"""Verify credentials, SIP/OPRA entitlement, and the store/DuckDB round-trip.

Makes a handful of small requests (a real NVDA daily-bars pull into the store,
plus read-only probes of the option chain, contracts, news, and corporate
actions). Exits non-zero if the critical SIP + OPRA entitlements aren't available.

    python -m alpaca_data.scripts.smoke_test
"""
from __future__ import annotations

import sys
from datetime import date, timedelta

from ..config import get_settings
from ..fetch import stocks
from ..rest import AlpacaDataClient
from ..store import duckdb_store
from ._common import setup_logging


def _mask(k: str) -> str:
    return f"{k[:4]}...{k[-2:]}" if len(k) > 6 else "***"


def _probe(name: str, fn) -> bool:
    try:
        print(f"  [PASS] {name}: {fn()}")
        return True
    except Exception as exc:  # noqa: BLE001 - smoke test wants every failure reported
        print(f"  [FAIL] {name}: {type(exc).__name__}: {str(exc)[:300]}")
        return False


def main() -> int:
    setup_logging("WARNING")
    s = get_settings()
    c = AlpacaDataClient(s)
    end = date.today()
    start = end - timedelta(days=21)

    print("Alpaca data engine - smoke test")
    print(f"  key={_mask(s.api_key)} ({'paper' if s.is_paper_key else 'live'})  "
          f"stock_feed={s.stock_feed}  options_feed={s.options_feed}")
    print(f"  data_url={s.data_url}")
    print(f"  trading_url={s.trading_url}")
    print(f"  store={s.store_root}\n")

    def t_bars():
        stocks.fetch_bars(c, ["NVDA"], "1Day", start.isoformat(), end.isoformat(), incremental=False)
        if "stocks_bars" not in duckdb_store.available_views():
            raise RuntimeError("no bars landed in the store")
        df = duckdb_store.query(
            "SELECT count(*) AS n, max(timestamp) AS last_ts FROM stocks_bars WHERE symbol='NVDA'")
        return f"{int(df['n'][0])} NVDA daily bars in store; last={df['last_ts'][0]}"

    def t_chain():
        page = c.get(f"{s.data_url}/v1beta1/options/snapshots/NVDA",
                     {"feed": s.options_feed, "limit": 5})
        snaps = page.get("snapshots") or {}
        return f"{len(snaps)} contracts (e.g. {next(iter(snaps), None)})"

    def t_contracts():
        page = c.get(f"{s.trading_url}/v2/options/contracts",
                     {"underlying_symbols": "NVDA", "limit": 3})
        cs = page.get("option_contracts") or []
        return f"{len(cs)} contracts (e.g. {cs[0]['symbol'] if cs else None})"

    def t_news():
        page = c.get(f"{s.data_url}/v1beta1/news", {"symbols": "NVDA", "limit": 3})
        items = page.get("news") or []
        return f"{len(items)} items (e.g. {(items[0]['headline'][:60] + '...') if items else None})"

    def t_ca():
        page = c.get(f"{s.data_url}/v1/corporate-actions",
                     {"symbols": "AAPL", "types": "forward_split,cash_dividend",
                      "start": "2020-01-01", "end": "2022-12-31", "limit": 3})
        return f"types={list((page.get('corporate_actions') or {}).keys())}"

    crit_bars = _probe("stocks SIP bars -> store -> DuckDB", t_bars)
    crit_chain = _probe("options OPRA chain (greeks/IV)", t_chain)
    _probe("option contracts (trading API)", t_contracts)
    _probe("news", t_news)
    _probe("corporate actions", t_ca)

    print()
    if not (crit_bars and crit_chain):
        print("CRITICAL: SIP stocks and/or OPRA options are not accessible. "
              "Check the subscription on this account and the key/secret in .env.")
        return 1
    print("Core entitlements OK (SIP + OPRA). Store + DuckDB round-trip works. Ready to backfill.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
