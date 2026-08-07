# alpaca-data — market-data engine for backtesting & theory verification

Pulls Alpaca **historical** and **real-time** market data — stocks, options, news,
corporate actions — into a local **DuckDB + Parquet** research lake. Built for a
paid **Algo Trader Plus** subscriber (SIP stocks + OPRA options).

- **Raw REST** core for historical pulls — manual pagination streams pages to disk
  with bounded memory (safe for tick data); a token-bucket limiter stays under the
  10,000 req/min account cap; retries with backoff on 429/5xx.
- **alpaca-py** for the WebSocket streams (auth, reconnection, msgpack handled).
- **Parquet lake** (the "store folder") = canonical storage; **DuckDB** = the query
  engine that reads it directly with SQL — no server, no import step.

## What it fetches

| Family | Data | History | Notes |
|---|---|---|---|
| Stocks | bars, trades, quotes, auctions | bars to **2016** | tick = trades/quotes (large) |
| Options | chain snapshots (greeks/IV), bars, trades | since **Feb 2024** | discover contracts first; no historical *quotes* (snapshot/live only) |
| News | headlines + full content | to **2015** | Benzinga |
| Corporate actions | splits, dividends, mergers, … | — | needed for backtest adjustments |
| Live | SIP stocks + OPRA options streams | real-time | rotating Parquet |

## Setup

```powershell
# from this alpaca-data/ folder
python -m venv .venv
.venv\Scripts\python -m pip install -U pip
.venv\Scripts\python -m pip install -e .      # installs deps + the alpaca_data package

# credentials: .env already exists here (gitignored). Otherwise:
#   copy .env.example .env   and fill in ALPACA_API_KEY / ALPACA_API_SECRET
```

Verify creds + SIP/OPRA entitlement + the store round-trip:

```powershell
.venv\Scripts\python -m alpaca_data.scripts.smoke_test
```

## Backfilling

```powershell
# Daily bars for the AI-semi universe, 2016->today (incremental on re-run)
python -m alpaca_data.scripts.backfill_stocks --universe default:ai_semis --timeframe 1Day

# Intraday bars
python -m alpaca_data.scripts.backfill_stocks --symbols NVDA,AMD --timeframe 5Min --start 2024-01-01

# Tick tape (LARGE — keep the window narrow)
python -m alpaca_data.scripts.backfill_stocks --symbols NVDA --data trades,quotes --start 2025-06-02 --end 2025-06-06

# Options: discover contracts (incl. expired), then bars + chain snapshots
python -m alpaca_data.scripts.backfill_options --universe default:ai_semis --data contracts,bars,chain
# Option trades (tick) for a specific expiry window. (No historical option quotes
# exist at Alpaca — use --data chain for NBBO+greeks snapshots, or the live stream.)
python -m alpaca_data.scripts.backfill_options --symbols NVDA --data trades \
    --exp-gte 2025-06-01 --exp-lte 2025-06-30 --start 2025-06-02 --end 2025-06-06

# News + corporate actions
python -m alpaca_data.scripts.backfill_news --universe default:ai_semis --start 2023-01-01
python -m alpaca_data.scripts.backfill_corpactions --universe default:ai_semis
```

Everything is **incremental**: a JSON watermark (`store/_catalog.json`) records how
far each dataset is fetched, so re-running only pulls new data. Use
`--no-incremental` to force a full refetch. (The watermark tracks the *latest*
fetched date per series; if you first pulled a recent window and later want older
history, run once with `--no-incremental` to backfill the gap.)

## Querying (DuckDB)

```powershell
python -m alpaca_data.scripts.query                       # list views + row counts
python -m alpaca_data.scripts.query "SELECT symbol, count(*) FROM stocks_bars GROUP BY 1"
```

In Python / a notebook:

```python
from alpaca_data.store import duckdb_store
df = duckdb_store.query("""
    SELECT symbol, timestamp, close
    FROM stocks_bars
    WHERE symbol IN ('NVDA','AMD') AND timestamp >= '2024-01-01'
    ORDER BY symbol, timestamp
""")
```

Views: `stocks_bars`, `stocks_trades`, `stocks_quotes`, `stocks_auctions`,
`options_bars`, `options_trades`, `options_quotes`, `options_snapshots`,
`options_contracts`, `news`, `corporate_actions`, plus `*_stream` for live capture.

## Research / backtest helpers

Alpaca gives you data + *forward* (live/paper) execution — **not** a historical
backtester. The `alpaca_data.research` package bridges the lake to a backtest with
the correctness plumbing you'd otherwise hand-roll (look-ahead-safe panels,
corp-action tables, point-in-time option chains):

```python
from alpaca_data.research import loaders, backtest
from alpaca_data.research import options as opt

px   = loaders.get_bars(["NVDA","AMD","AVGO"], start="2020-01-01")  # wide close panel
rets = loaders.get_returns(["NVDA","AMD"])                          # period returns
feat = loaders.feature_frame(["NVDA"], start="2025-01-01")          # bars + daily news count
divs = loaders.get_dividends(["AVGO"])                              # corp-action tables

chain = opt.get_chain("NVDA")                 # latest stored snapshot (greeks/IV)
atm   = opt.atm_contract("NVDA", target=0.5)  # ~50-delta call

# weights decided at close t earn t+1's return (lagged internally => no look-ahead)
res = backtest.vector_backtest(px, weights, cost_bps=5)
print(backtest.performance_stats(res["net_return"]))   # cagr, sharpe, max_drawdown, ...
```

Worked example (momentum on the AI-semi names):

```powershell
python -m alpaca_data.scripts.demo_backtest
```

Intentionally *not* here: a full execution/PnL engine. The loaders return plain
pandas, so feed them into vectorbt / backtrader if you outgrow the built-in
vectorized backtester.

## Live streaming (markets must be open)

```powershell
python -m alpaca_data.scripts.stream_live --asset stocks --universe default:ai_semis
python -m alpaca_data.scripts.stream_live --asset options --symbols NVDA250620C00130000
```

One process streams one asset class (each stream blocks); run two terminals for both.

## Store layout

```
store/
  stocks/bars/timeframe=1Day/symbol=NVDA/year=2024/data.parquet
  stocks/quotes/symbol=NVDA/date=2025-06-03/data.parquet
  options/contracts/underlying=NVDA/data.parquet
  options/bars/timeframe=1Day/underlying=NVDA/year=2024/data.parquet
  options/snapshots/underlying=NVDA/asof=2026-06-13/data.parquet   # greeks + IV
  news/year=2024/month=01/NVDA_AMD.parquet
  corporate_actions/ctype=cash_dividends/year=2024/ALL.parquet
  _catalog.json
```

All fields live inside the Parquet files (including `symbol`), so DuckDB prunes via
row-group statistics. `store/` is gitignored.

## Notes & limits

- **Rate limit**: paid cap is a hard **10,000 req/min** (account-wide). Default
  headroom is 9,000 — tune `ALPACA_MAX_REQUESTS_PER_MIN` in `.env`.
- **Adjustments**: stock bars default to `adjustment=all` (split + dividend) so
  backtests don't see split jumps. Pull corporate actions for exact adjustment math.
- **Option quotes**: Alpaca exposes no *historical* option-quote series — option
  history is bars + trades. For NBBO/greeks over time, run `--data chain` daily
  (snapshots are stored); for real-time, use the stream.
- **Tick memory**: one symbol-day of quotes is accumulated then written. For the
  most active names (SPY/QQQ), narrow the date range.
- **Security**: `.env` holds your keys and is gitignored. The provided key is a
  *paper* key (`PK…`); rotate it since it was shared in chat.
- **Tests**: `python tests/test_units.py` (or `pytest`) — pure logic, no network.
