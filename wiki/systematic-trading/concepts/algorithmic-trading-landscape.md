---
type: concept
title: The Algorithmic-Trading Landscape & How Quants Actually Build
description: The industry map by horizon — market makers/HFT (Service payer, speed-gated, inaccessible), arbitrage HFT (the plumbing), stat-arb/equity-market-neutral (the methods a solo can copy at daily horizon), CTAs/trend (simple signals, sophisticated portfolio), factor funds, vol quants, execution algos (service, not alpha), retail bots (the junk tier), and the pod-shop-vs-single-book org models (breadth applied to people). What the algorithms actually are (sketches: Avellaneda-Stoikov, TSMOM, cross-sectional residual reversal, cointegration/OU, ML-as-combiner). The institutional research pipeline: mechanism → point-in-time data → signal → IC/quantile evaluation → combination → optimizer → cost model → backtest-as-integration-test → DSR/registry → incubation → monitored decay. The software stack at funds vs a solo Python stack.
tags: [systematic-trading, ml-stats, microstructure, process, alpha]
timestamp: 2026-07-02T00:00:00Z
status: active
sources: []
---

# The Algorithmic-Trading Landscape & How Quants Actually Build

Most modern volume is machine-intermediated: HFT is roughly half of US equity volume; ~70–80% of
institutional order flow is worked by execution algos; one wholesaler (Citadel Securities) prints
on the order of a quarter of US equity volume and ~40% of retail flow. But "algorithms dominate" is
not one business — it is **several different businesses on different clocks**, each mapping to a
different [payer](../../shared/concepts/who-pays-you.md). Knowing which is which tells you what is
copyable by an individual and what is physically gated.

## 1. The industry map (by horizon and payer)

| Segment | Who | Horizon | Edge / payer | Gated by | Solo-copyable? |
|---|---|---|---|---|---|
| **Market making** | Citadel Securities, Virtu, Jane Street, [XTX](../../shared/people-firms/xtx-markets.md), Optiver, IMC, SIG, HRT, Jump | μs–min | Spread + inventory mgmt (**Service**) | Co-location, microwave (~4ms Chicago↔NJ), FPGAs, flow access (PFOF), fee tiers | **No** — physical + flow moat |
| **Arbitrage HFT** | same firms + specialists | ms–hrs | Index/ETF/cross-venue basis (**plumbing**) | Speed, balance sheet | No |
| **Stat-arb / EMN** | RenTec, DE Shaw, Two Sigma, PDT, WorldQuant, pods | hrs–weeks | Cross-sectional **Mistake** + flow at scale; factor-neutral, 5–8× levered, book Sharpe ~2–4 | Data budgets, research platform, execution | **Methods yes** (daily horizon); scale no |
| **CTA / trend** | Man AHL, Winton, Aspect, AQR MF | wks–months | Underreaction + risk transfer (**Mistake/Service**) across ~50–150 futures | Breadth of markets | **Yes in spirit** (the regime/trend overlay) |
| **Factor / risk premia** | AQR, DFA, Robeco | months–yrs | **Premium** + slow Mistake | Scale economics, patience | Yes (long-only tilts) |
| **Vol quants** | SIG, Optiver, Capstone | days–months | VRP (**Service** — selling insurance), surface RV | Margin, greeks infra | No at a small retail account (and short-vol = ruin-shaped) |
| **Execution algos** | banks, agency brokers | intraday | **None — a service** (cost minimization) | — | Concepts yes ([optimal execution](../strategies/optimal-execution.md)) |
| **Retail bots** | Pine/MT4/grid/"AI" apps | any | Usually none — curve fits without validation | — | The tier to *not* join |

Reference points worth keeping: **Medallion** (RenTec) ≈ 66% gross / ~39% net annualized over ~30
years — capped ~$10–15B and closed, i.e. the best edges are **capacity-constrained** (why they
survive at all — [limits to arbitrage](../../shared/concepts/limits-to-arbitrage.md)). The **August
2007 quant quake** (Khandani–Lo): the canonical demonstration that crowded stat-arb unwinds
violently — same-signal + leverage = correlated forced selling. **The pod-shop model** (Millennium,
Citadel, Point72, Balyasny): hundreds of independent teams under iron risk limits (capital cut at
~−5%, fired ~−7–10%) with netted center books — the industry's answer to fragile alpha is
**Grinold breadth applied to people**, plus ruthless kill discipline. The individual's counter-
advantages are the mirror image: no career risk on drawdowns, no capacity pressure, freedom to hold
through what a pod cannot. One more reference point *inside* the market-making tier:
[XTX Markets](../../shared/people-firms/xtx-markets.md) is the instructive counterexample to the
speed framing — it wins on ML forecast quality and minutes-to-hours inventory holding rather than
the latency race (~300 staff, £1.71B net profit 2025), proof the MM moat can be compute + models
rather than co-location + purchased flow. Still not solo-copyable; the moat just lives in a
different budget line. The economics of that speed-vs-prediction split — and the full horizon
ladder from microsecond races to this desk's days-to-weeks corner — are worked out in
[speed vs prediction](speed-vs-prediction.md).

## 2. What the algorithms actually are (sketches)

- **Market making** ([page](../strategies/market-making.md)): quote both sides around a reservation
  price skewed against inventory (Avellaneda–Stoikov: r = mid − q·γ·σ²·(T−t)); widen/pull on
  toxicity signals (order-flow imbalance, sweeps). *Note: `enginev2`'s microprice/imbalance/OFI
  indicators are exactly this sensing layer — built without the speed or quoting rights to use it,
  which is one honest framing of why that space returned DEAD.*
- **Trend/CTA**: embarrassingly simple signal, sophisticated wrapper — position =
  sign(12-1 month return) × target_vol/realized_vol, blended across lookbacks, across many markets
  (Moskowitz–Ooi–Pedersen TSMOM). The sophistication is vol targeting + portfolio + execution, not
  the signal.
- **Cross-sectional stat-arb** ([page](../strategies/pairs-trading-statarb.md)) — *the* template a
  solo can adapt at daily horizon: (1) liquid universe; (2) regress the day's cross-section of
  returns on factors (beta/sector/size/momentum) → **residuals**; (3) alpha = −z(3–5-day cumulative
  residual) [reversal] ± slower momentum; (4) neutralize sector/vol; (5) optimizer: long losers /
  short winners, dollar/beta/sector-neutral, cost-penalized; (6) hold 2–10 days. Per-name IC is
  tiny (~0.02–0.05); breadth (hundreds of names × ~100 rebalances/yr) does the work — IR ≈ IC·√BR.
- **Pairs/cointegration**: Engle–Granger/Johansen → spread as an OU process (enter |z|>2, exit ~0,
  structural-break stop). *`enginev2` already has a calibrated OU MLE and a BreakDetector — both
  transfer.*
- **Daily mean reversion** (the [edge map](../../synthesis/retail-capital-edge-map.md) flagship):
  RSI(2)/IBS extremes on liquid ETFs/mega-caps, gated by 200-DMA trend + vol regime.
- **ML alphas — the honest version**: not "an LSTM predicts the price." Reality: gradient-boosted
  trees on cross-sectional tabular features predicting next-k-day **residual return rank**;
  purged/embargoed time-series CV; monthly retrains; the model is a **combiner of many weak
  signals, not an oracle** (Gu–Kelly–Xiu: ML adds modest but real IC over linear). Deep nets earn
  their keep mostly in NLP/unstructured extraction and short-horizon sequence models
  ([XTX-style](../../shared/people-firms/xtx-markets.md)). ML raises
  the silent-overfit risk precisely because it fits interactions — registry + DSR discipline
  matters *more*, not less.
- **Vol arb**: fit the surface (SVI), trade implied-vs-forecast RV (GARCH/HAR), delta-hedge; earn
  the [VRP](../../derivatives/concepts/volatility-risk-premium.md); dispersion = short index vol vs
  long single-name vol.
- **Execution** ([page](../strategies/optimal-execution.md)): Almgren–Chriss cost-vs-risk
  trajectories, child-order placement in the [LOB](limit-order-book.md) — the machinery behind the
  √-impact law in [price formation](../../shared/concepts/price-formation-and-the-float-identity.md).

## 3. How quants actually build (the pipeline)

The load-bearing surprise for outsiders: **the backtest is nearly the *last* step, not the first.**
The pipeline at a real shop:

0. **Mechanism first** — idea sourcing filtered by *who pays and why it persists* (this wiki's
   [who-pays-you](../../shared/concepts/who-pays-you.md) test). No mechanism → not researched.
1. **Data** — acquisition, cleaning, **point-in-time-ification** (as-reported with lags, delisted
   names kept, corporate actions). ~Half of all real quant work is data plumbing; survivorship and
   look-ahead are the career-ending bugs ([data integrity](../../ml-stats/concepts/data-integrity.md)).
2. **Signal construction** — raw data → one standardized per-name daily score (winsorize, z-score
   cross-sectionally, neutralize sector/size).
3. **Single-signal evaluation — the IC framework** (the institutional core):
   **IC** = corr(signal, k-day forward return) daily → mean IC, IC t-stat, **IC-decay curve** (sets
   the natural holding period); **quantile portfolios** (decile sort → Q10−Q1 spread, monotonicity);
   **turnover** (signal autocorrelation → cost hurdle); **factor regression** (is the "alpha" just
   momentum/beta/size in disguise? residualize and re-test); robustness by subperiod/sector/regime;
   parameter plateaus.
4. **Combination** — many weak alphas → composite (IC-weighted or ML combiner); watch inter-alpha
   correlation (effective breadth < nominal breadth).
5. **Portfolio construction** — maximize α′w − λ·w′Σw − costs(Δw) under constraints; a factor risk
   model supplies Σ. **The optimizer, not the signal, decides the trades.**
6. **Cost model** — spread + √-impact, calibrated to own fills; this is what sets capacity.
7. **Backtest** — the point-in-time *integration test* of the whole pipeline (walk-forward). "You
   learn from IC tables; the backtest confirms."
8. **Multiple-testing control** — trial registry → [deflated Sharpe](../../ml-stats/concepts/performance-metrics.md),
   sealed holdout, adversarial review (`enginev2`'s PROTOCOL is this stage, already built).
9. **Incubation** — 1–6 months paper on live data; compare **live IC vs backtest IC**; then small
   capital, scaled by realized capacity.
10. **Production monitoring** — live IC/decay dashboards, drawdown de-risking rules, post-mortems.
    Alphas retire on schedule; **the pipeline is the asset** ("alpha factory"), not any one signal.

**The software stack** at funds: Python/Jupyter + pandas/polars for research; kdb+/q for tick
stores; C++/Rust/Java execution cores; FPGAs at the speed tier; feature stores, backtest clusters,
experiment tracking; the **point-in-time database is the crown jewel**. A solo daily-horizon stack
needs none of the exotic parts: Python + parquet/SQLite + a nightly cron + a Numba kernel where
speed matters (all already proven in `enginev2`).

## Relationships
- Mechanics beneath it: [LOB](limit-order-book.md) · [market microstructure](market-microstructure.md) ·
  [price formation & the float identity](../../shared/concepts/price-formation-and-the-float-identity.md).
- Strategy pages this map indexes: [market making](../strategies/market-making.md) ·
  [pairs/stat-arb](../strategies/pairs-trading-statarb.md) · [optimal execution](../strategies/optimal-execution.md) ·
  [momentum](../factors-signals/momentum.md).
- Validation layer: [backtesting & overfitting](../../ml-stats/concepts/backtesting-overfitting.md) ·
  [performance metrics / DSR](../../ml-stats/concepts/performance-metrics.md).
- Why edges persist/decay: [limits to arbitrage](../../shared/concepts/limits-to-arbitrage.md) ·
  [factor premia & alpha decay](../../shared/concepts/factor-premia-and-alpha-decay.md).
- Applied to this project: [engine v3 design brief](../../synthesis/engine-v3/design-brief.md) ·
  [small-account edge map](../../synthesis/retail-capital-edge-map.md).

## Open questions
- Which Constraint flows (index recon, month-end, OpEx) have *published* solo-tradable calendars vs
  requiring paid positioning data — worth a `shared/datasets` observability page (already a
  graduation candidate).
- Where is the current crowding frontier in daily cross-sectional reversal (post-2018 IC decay
  estimates) for a 100–300-name liquid universe?
