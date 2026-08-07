---
type: overview
title: Retail-Capital Edge Program — Discovery Roadmap
description: Research roadmap for finding cost-survivable edges under retail capital constraints — candidate families, validation gates, and a semi-automated signals→measure loop. Generalized; not account-specific.
tags: [systematic-trading, strategy, risk, retail, ml-stats]
timestamp: 2026-08-07T00:00:00Z
status: active
sources: [../sources/deep-research-retail-capital-edge-survey.md]
---

# Retail-Capital Edge Program — Discovery Roadmap

A structured research program for **low-AUM, long-only, cash-account operators** trading liquid US equities and ETFs (optional leveraged ETFs as *vehicles*, not edges). The goal is not a promised income stream; it is a **validated, cost-honest process** that can be measured and killed.

**Education / research only — not investment advice.**

## Problem framing

Retail operators face a different constraint set than institutions:

| Constraint | Implication |
|---|---|
| Tiny notional | Market impact ≈ 0; capacity is not the binding limit |
| Spreads + commissions + tax | Many “textbook” edges die after costs |
| Long-only cash (often) | No short leg; many anomaly profits live on the short side |
| Limited sample of live days | Overfitting and look-ahead are the main research risks |
| Behavioral load | Disposition effect and revenge sizing dominate process failure |

The honest research question: **which candidate edges survive costs and a pre-registered validation gate under these constraints?**

## Locked research profile (generalized)

- **Universe:** liquid US stocks/ETFs; optional 2×/3× ETFs only as expression vehicles for a *validated host signal*
- **Horizon:** swing (days–weeks) primary; intraday treated as hostile until proven otherwise
- **Data:** free/public first (OHLCV); paid feeds only when a design page says so
- **Execution model:** signals + discretionary or semi-auto execution; full auto-routing optional later
- **Cost model (must be explicit):** commission (incl. post-promo), half-spread, slippage, FX if applicable, local capital-gains tax

## Candidate edge families (Phase 1 survey set)

1. Regime-gated short-term mean reversion (liquid)
2. Regime / volatility gating + trend overlay (survival wrapper)
3. Low-turnover momentum / dual-momentum ballast
4. PEAD / earnings drift
5. Calendar / seasonality
6. Overnight / gap
7. Leveraged-ETF *tactics* (vs vehicle use)
8. Structural “retail advantages” (impact, cash freedom) as a *lens*, not a strategy

Results of the adversarial cost pass are on the [retail-capital edge map](retail-capital-edge-map.md).

## Validation gates (pre-committed)

1. **Cost-first:** model costs before looking at gross Sharpe.
2. **Deflated Sharpe / multiple-testing:** treat trial count honestly ([backtesting & overfitting](../ml-stats/concepts/backtesting-overfitting.md)).
3. **True OOS / walk-forward:** sealed holdout; no peeking.
4. **Risk-of-ruin / Kelly:** size so survival is not optional ([risk of ruin](../shared/concepts/risk-of-ruin.md), [Kelly](../shared/concepts/kelly-criterion.md)).
5. **Regime robustness:** edge must not only work in one calm decade.
6. **Live measurement:** paper or tiny size with process KPIs before any scale-up.

## Build order (suggested)

1. **Survival overlay** — regime/vol + trend gate (drawdown control).
2. **Flagship test** — regime-gated mean reversion on liquid names/ETFs.
3. **Ballast** — low-turnover trend, not as income.
4. **Vehicle rules** — if using leveraged ETFs, hard max hold, chop bans, size via the gate ([leveraged-ETF decay](../shared/concepts/leveraged-etf-decay.md)).
5. **Kill criteria** — fixed in advance: DSR fail, cost cliff, or live process breach rate.

## What “done” looks like

- A ranked map of what survived / died (Phase 1 complete on this wiki).
- A written cost model and evaluation harness.
- Zero reliance on “unlimited day trades” as an edge claim.
- Process metrics (pre-committed calls, adherence) outranking short-window P&L noise.

## Related

- [Retail-capital edge map](retail-capital-edge-map.md) · [survey brief](../sources/deep-research-retail-capital-edge-survey.md)
- [Alpha map](alpha-map.md) · [Trading system fundamentals](trading-system-fundamentals.md) · [Who wins — empirical record](../shared/concepts/who-wins-empirical-record.md)
