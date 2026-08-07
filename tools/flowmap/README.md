# flowmap — the five-question flow read

One integrated module + interactive dashboard answering, per name on the semis
complex, the five questions that precede any conviction entry:

1. **Who owned the recent move?** — cohort attribution. Korea (Naver investor
   trend, D+0) and Taiwan (TWSE T86 三大法人, D+0/D+1) are *measured*; US names
   get honest *inference* only (overnight/intraday split, FINRA short-volume mix).
2. **Whose shares am I buying?** — forced seller (cascade, margin clock — favorable)
   vs informed distributor (foreigners selling strength into retail absorption — adverse).
3. **Who is forced to trade next, which way?** — the ffcal calendar plus the
   leveraged-ETF arithmetic: rebalance $ = (L²−L) × AUM × day-return, netted across
   the suite, computable by ~15:00 ET — the one flow knowable before it trades.
   Plus the KR margin clock and a naive dealer-gamma state (LOW confidence).
4. **Where is the crowd?** — KOFIA margin balance (live), cohort accumulation,
   SI/P/C/IV-vs-RV, NAAIM/COT context; equal-weight pre-registered score.
5. **What's already priced?** — the expectations bar: straddle-implied vs realized
   reaction moves, run-up vs SMH, 30d EPS-estimate drift. A priced record is a sell.

Design spec: [`wiki/designs/semis-institutional-flow-map.md`](../../wiki/designs/semis-institutional-flow-map.md)
(this is the P1-live slice, §11). **Identification contract:** the tool detects
positioning and pressure, never intent — every attribution ships as
hypothesis + confidence + falsifier (the MU 2026-06-23 cascade lesson).

## Run

```
python tools/flowmap/flowmap.py                 # pull, compute, print brief, open dashboard
python tools/flowmap/flowmap.py read --quick    # shallow backfills (fast first run)
python tools/flowmap/flowmap.py read --offline  # caches + engine lake only
python tools/flowmap/flowmap.py selftest        # arithmetic anchors, no network
```

First run backfills ~60 T86 sessions + ~30 FINRA files (≈6 min); warm runs ≈10 s.
Dashboard: `store/dashboard.html` (self-contained; `?tab=NVDA`, `?theme=dark` work).
Each run also writes `store/snapshots/read-<ts>.json` — the grading substrate —
and appends the day's LETF AUM to `store/aum/` (own forward S5-style archive).

**Optional data lake:** if you maintain a separate research lake (KOFIA history, COT,
surveys), set environment variable `ENGINE_LAKE` to that directory. No absolute machine
paths are hardcoded; without the env var the tool runs on its free public pulls only.

## Data (all free)

| feed | source | freshness |
|---|---|---|
| KR cohort prints | Naver mobile trend API (engine-v3 S3's approved fallback basis: qty × close) | D+0 after Seoul close |
| KR margin | KOFIA freesis JSON (engine-v3 S10's endpoint, pulled live) | D+0/D+1 |
| TW cohort prints | TWSE T86 daily JSON, per-day cached | ~16:00 TST, falls back a day |
| US prices/options/earnings | yfinance (daily, 5m intraday, chains, eps_trend) | live-ish |
| US short volume | FINRA CNMS daily files, per-day cached | evening D+0 |
| calendar | `tools/calendar/ffcal.py` (imported) | deterministic |
| context | engine-v3 lake (NAAIM history, COT) if present | as-of lake |

## Pre-registered rules (no fitting until ≥60 graded days)

Anomaly flags: single-feed |z|≥3, or |z|≥2 on ≥2 feeds from *different* evidence
groups (asia-prints / etf-flows / options / short-borrow / off-exchange / filings),
or the divergence tells (price ±2σ without cohort confirmation; retail absorbing
what foreigners distribute into strength). Breadth: |ret5 − SMH| ≥ 3% →
idiosyncratic. Crowd/bar scores: equal-weight z means, thresholds ±0.75 / ±1.0.

## Honest limits

- US cohort identity is unobservable at any price — identity was traded for
  behavior; US panels are labeled INFERRED and never say "institutions bought".
- Naver values are quantity × close (documented approximation, consistent basis).
- Event straddles more than ~15d out are ambient-vol-dominated and labeled so.
- Dealer gamma uses the naive +call/−put convention — a state hint, LOW confidence.
- ETF-flow and options z-scores arm only as this tool's own archives accumulate
  (day one: 4/6 evidence groups armed).
- Reading the present, never racing it: second-level latency, state not speed.

Kill criteria and the grading loop (flag-level 8-week decision-use gate,
~90-flag flag-quality gate) are in the design page §8; snapshots exist so the
grading loop can be wired without re-architecture.
