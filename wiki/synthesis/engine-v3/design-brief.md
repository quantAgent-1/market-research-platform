---
type: overview
title: Engine v3 — Design Brief: a Cross-Sectional Daily Signal Platform (the Sensing Instrument)
description: The successor to enginev2's honest dead end. Mission reframed from profit-machine-on-one-name to sensing instrument — a cross-sectional daily-bar signal research platform + market-condition dashboard for the small-account/no-fee/no-holding-limit profile. Five layers (free daily data on a ~100-300-name liquid universe → registered features/signals → the NEW IC/quantile evaluation core + v2's protocol verbatim → long-only vol-targeted paper portfolio with a 1-3-position live sleeve → an evening-KST condition report). First registered hypotheses inherited from the Phase-1 edge map (overlay first, cross-sectional reversal flagship, momentum ballast). Deliverables = understanding + full-cross-section paper track record + adherence-measured live slice; dollars explicitly not the KPI at a small retail account.
tags: [systematic-trading, ml-stats, small-account, process, strategy]
timestamp: 2026-07-02T00:00:00Z
status: active
sources: []
---

# Engine v3 — Design Brief (2026-07-02)

> **Companion blueprint:** the full file-by-file repo outline (tree, stack, nightly DAG, PROTOCOL
> v3.0, weekly deliverables) lives at [project-outline.md](project-outline.md)
> (added 2026-07-03).

*The successor to `enginev2`, which closed its assigned space (manual intraday TSLA) as an honest,
five-way-verified negative. v3 keeps v2's rarest asset — the trustworthy verdict machine (frozen
protocol, pre-registered ledger, sealed holdout, adversarial gate, DSR) — and points it at the
space where two independent research lines (v2's null + the
[Phase-1 edge survey](../retail-capital-edge-map.md)) agree the payers are: **cross-sectional,
daily-bar, days-to-weeks.** Companion reading:
[the algorithmic-trading landscape & quant pipeline](../../systematic-trading/concepts/algorithmic-trading-landscape.md).*

## 1. Mission — a sensing instrument, not a profit machine

v2's mission was "find positive-EV intraday TSLA signals" — a profit machine aimed at one name.
v3's stated mission (user's words): **"present meaningful market signals to get a better
understanding of the stock market."** Take that seriously — it is the *right* mission at this
account size. v3 is a **cross-sectional daily signal research platform + condition-recognition
dashboard**, whose three products are:
1. a **full-cross-section paper track record** (the audition tape for future capital),
2. a **small live sleeve** (1–3 positions) with **adherence tracking** — attacking v2's one
   measured live leak (the operator, −$39.76 of a −$44 day),
3. a **daily condition report** (regime, breadth, dispersion, flow calendar) that plugs into the
   wiki's [monitoring philosophy](../semiconductor-monitoring-system.md).

Dollars are explicitly **not** the KPI (denominator honesty: even success ≈ $100–300/yr on a small retail account).

## 2. Constraint audit (the user's stated advantages, honestly assessed)

- **No fees until 2026-12-31** — real but temporal: a **free-turnover lab window**. Use it to
  measure live slippage/fill quality on small orders, not to churn. The Jan-1 cost cliff is the
  pre-registered re-validation gate ([edge map](../retail-capital-edge-map.md)).
- **No trade limits** (KR cash → no PDT) — mostly moot: Phase 1 showed the edge is not in
  frequency.
- **No holding-period constraint** — the *actual* structural advantage: days-to-weeks is where
  institutions face calendar/career constraints and HFT does not compete.
- **Small account** — zero market impact (√-law irrelevant) and capacity-free corners; **but**
  breadth-of-positions is capital-gated: ~a small retail account buys 1–5 whole-share US mega-cap positions (MU
  alone ≈ $1,000). Resolution: **the engine computes the full cross-section; paper trades all of
  it; live trades a top-N slice.** (a Korean retail broker fractional-share support = still-open Phase-0 question.)
- **KST fit** — daily cadence is ideal: compute signals from the 05:00-KST close during the Korean
  day; place next-open orders at 22:30 KST. v2's *signal-on-close → fill-next-open* convention
  carries over verbatim.
- **Long-only cash** — loses the short leg (most documented anomaly profit). Mitigations: long-only
  tilt vs cash, regime gates as the "synthetic short," inverse ETFs only as crude, decay-costed
  hedges.

## 3. Architecture — five layers (the institutional stack, sized to one person)

1. **Data** — free daily OHLCV (yfinance batch, Stooq fallback): ~100–300 liquid US names
   (S&P-100 + Nasdaq-100 + sector ETFs + the semis complex) + v2's ETF set; corporate-action
   adjusted; parquet/SQLite store; nightly job. **Point-in-time honesty:** current-membership
   universes carry survivorship bias — clean for *forward* use (re-select by liquidity at each
   rebalance), flagged as a caveat in any historical backtest
   ([data integrity](../../ml-stats/concepts/data-integrity.md)).
2. **Features/signals** — per-name (multi-horizon returns, vol, RSI/IBS, gaps, distance-to-MAs,
   sector-relative residual returns, 52-wk-high proximity) + market-level (breadth %>200DMA,
   advance/decline, cross-sectional dispersion, index trend, VIX if free). Every signal is a
   **registered object** (id, formula, params, hypothesis, *mechanism = named payer*).
3. **Evaluation — the NEW core + v2's protocol verbatim.** New: the **IC framework** — daily
   rank-IC vs 1/5/10/21-day forward returns, IC-decay curves, decile spreads net of assumed costs,
   turnover, **factor-neutralization** (vs beta/momentum/size — is it alpha or disguised beta?),
   subperiod/regime robustness, parameter plateaus. Carried from v2: pre-registration, append-only
   ledger, sealed holdout (new seal date, never consumed), fee-ladder & perturbation reruns,
   adversarial fresh-eyes gate (kill is final), [DSR](../../ml-stats/concepts/performance-metrics.md)
   with *v2 trial counts included* where families overlap.
4. **Portfolio/paper** — composite signal → long-only weights, vol-targeted gross, **regime gate
   scaling exposure 0–100%**; full portfolio paper-traded daily with the cost model attached; live
   sleeve = top-N (1–3 names, v2's 2%-risk caps), manual execution against a
   [checklist](../../systematic-trading/checklists/new-high-trade-checklist.md), **adherence-% logged
   as a first-class metric**.
5. **Dashboard/report** — the "meaningful market signals" deliverable, generated nightly for the
   Korean evening: regime state (trend/vol gates), breadth internals, dispersion (the MR fuel
   gauge), current signal readings + top/bottom names, the **flow calendar** (month/quarter-end,
   OpEx, index recon — the [Constraint-payer](../../shared/concepts/who-pays-you.md) schedule), and
   live+paper P&L, live-vs-backtest IC, adherence.

## 4. First registered hypotheses (inherited — do not restart idea generation)

| ID | Hypothesis | Source / mechanism | Role |
|---|---|---|---|
| H1 | Regime/vol + trend overlay (200-DMA class, slow, lagged) | Edge map #2; risk transfer/crash avoidance | **Build first — gates everything** |
| H2 | Cross-sectional short-term reversal, regime-gated, liquid universe | Edge map #1 generalized (RSI2/IBS → relative residual form); Constraint/Mistake payers | Flagship |
| H3 | Low-turnover momentum/trend (12-1, monthly) | Edge map #3; underreaction | Ballast |
| H4 | Overnight-vs-intraday return split as a *filter* | Edge map #5 residue | Cheap add-on |
| H5 | Flow-calendar condition flags (quarter-end, recon, OpEx) | The wiki's positioning research made systematic | **Dashboard-only** (flags, not trades) |

Each runs the full gauntlet: mechanism written first → IC analysis → quantiles → cost → DSR →
adversarial gate → ≥4 weeks paper. Kill fast; obituaries to the ledger.

## 5. Build order (evenings/weekends-realistic)

- **Wk 1–2:** data layer + universe + nightly job.
- **Wk 3–4:** IC evaluation harness; port v2's PROTOCOL as **v3.0** (amend: universe, horizon, new
  holdout seal date); open the v3 ledger with v2's trial counts referenced.
- **Wk 5–8:** H1 overlay + H2 reversal through the full gauntlet.
- **Wk 9–12:** portfolio + paper loop + dashboard v1; live sleeve **only after ≥4 clean paper
  weeks**.
- **Ongoing:** one registered hypothesis at a time; monthly post-mortem folded into the wiki.

**Deliberate exclusions:** no tick data / order-book features / intraday execution (the closed
space); no options; no ML combiner until ≥5 registered linear signals exist (ML combines alphas,
it doesn't conjure them); **no automated order routing** (v2's signal-only guardrail carries over).
*(Amended 2026-07-07: the routing exclusion is re-scoped as rung 0 of a gated promotion ladder —
see the [execution-layer design](execution-layer.md); tickets-only remains binding at every rung
below live-small.)*

## 6. Success metrics (pre-committed)

(a) ≥2 trustworthy verdicts/month once the harness is live; (b) live-sleeve **adherence ≥95%**;
(c) shipped-composite **paper IC > 0 out-of-registration** (measured, not asserted);
(d) the dashboard is actually read daily (the understanding goal); (e) dollars: **not a KPI** at
this size — the products are the process, the track record, and the understanding.

## 7. Canon (world-class-depth reading, in order)

1. **Grinold & Kahn, *Active Portfolio Management*** — the institutional framework (IC, IR,
   breadth) v3's evaluation layer implements.
2. **Qian, Hua & Sorensen, *Quantitative Equity Portfolio Management*** — the cross-sectional
   pipeline, step by step.
3. **López de Prado, *Advances in Financial Machine Learning*** — purged CV, DSR, backtest
   hygiene (v2 already lives this).
4. **Isichenko, *Quantitative Portfolio Management*** — modern stat-arb craft.
5. **Chan, *Algorithmic Trading*** — honest retail-scale implementation.
6. Papers: Moskowitz–Ooi–Pedersen (TSMOM) · Khandani–Lo 2007 (the quant quake) ·
   Avellaneda–Stoikov (MM) · Almgren–Chriss (execution) · Harvey–Liu–Zhu (multiple testing) ·
   Gu–Kelly–Xiu (what ML actually adds). [Cartea et al.](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md)
   already ingested.

## Relationships
- Supersedes-in-direction: `enginev2` (closed honest negative; apparatus reused). Program parent:
  small-account edge program — **v3 = its Phase-3 harness.**
- Evidence base: [edge map](../retail-capital-edge-map.md) · [who pays you](../../shared/concepts/who-pays-you.md) ·
  [price formation](../../shared/concepts/price-formation-and-the-float-identity.md) ·
  [algorithmic-trading landscape](../../systematic-trading/concepts/algorithmic-trading-landscape.md).
- Discipline: [backtesting & overfitting](../../ml-stats/concepts/backtesting-overfitting.md) ·
  [performance metrics/DSR](../../ml-stats/concepts/performance-metrics.md) ·
  [risk of ruin](../../shared/concepts/risk-of-ruin.md) ·
  robustness over prediction.

## Open questions / Phase-0 gates
- a Korean retail broker: fractional US shares? API access? order types (pre-placed GTC exits)? — carried open from
  the program page since Session 13.
- Free VIX/term-structure source reliability; free historical index-membership lists (to soften the
  survivorship caveat).
- Post-promo fee schedule (the Jan-1 cliff) — required for the DURABLE-vs-PROMO label, as in v2.
