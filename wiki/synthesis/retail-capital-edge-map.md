---
type: overview
title: Retail-Capital Edge Map — Phase-1 Survey Results
description: Ranked, cost-verified map of eight candidate edges under retail capital constraints. Honest result — income-shaped edges are marginal; survivable tools are mostly risk-control; naive intraday is negative-EV.
tags: [systematic-trading, strategy, risk, retail, ml-stats]
timestamp: 2026-08-07T00:00:00Z
status: active
sources: [../sources/deep-research-retail-capital-edge-survey.md]
---

# Retail-Capital Edge Map — Phase-1 Survey Results

Output of Phase 1 of the [retail-capital edge program](retail-capital-edge-program.md): eight candidate edges, web-researched then **adversarially stress-tested** for cost survival and decay. Several popular claims were **re-tested on free OHLCV data** during verification. Provenance: [survey brief](../sources/deep-research-retail-capital-edge-survey.md).

**Not investment advice.** Figures below are research results under stated assumptions, not forecasts of personal returns.

## Headline

1. **No standalone edge in this set is a reliable “steady income machine” net of costs.** What cleanly survives — regime/vol gating and low-turnover momentum — is mostly **drawdown control**, not alpha.
2. **Best income-shaped candidate: regime-gated short-term mean reversion** on liquid names. Gross edge can be real in recent windows; **net-of-cost is marginal** (single-digit percent per year class under optimistic cost assumptions) and **regime-conditional** (pays in turmoil, quiet in melt-ups).
3. **Leveraged ETFs are a vehicle, not an edge.** No tactic on them survived as standalone alpha. Sound use is capital-efficient expression of a *validated host signal* with hard hold rules — never multi-day in chop. Drawdowns in tests reached multi-tens of percent (ruin territory if the whole book is levered beta).
4. **Naive high-frequency intraday is negative-EV** in the public empirical record (day-trader censuses: large majority lose; persistence does not reliably produce learning). Zero commission does not flip this by itself.

## Ranked shortlist

| Rank | Edge | Role | Net-of-cost | Verdict |
|---|---|---|---|---|
| **1** | Short-term mean reversion (regime-gated, liquid) | Income-shaped engine | Marginal-positive | **Test — flagship** |
| **2** | Regime / vol gate + trend overlay | Survival wrapper | Survives | **Test — not standalone** |
| 3 | Low-turnover dual-momentum / trend | Ballast | Survives | Test as ballast |
| ✓ | Leveraged ETF *as vehicle* | Expression of #1–3 | n/a | Vehicle only, hard rules |
| ✗ | PEAD / earnings drift | — | Costs eat most | Skip (thin residue) |
| ✗ | Calendar / seasonality | — | Mostly fails costs | Skip (overnight split as *filter* only) |
| ✗ | Overnight / gap tactics | — | Arbitraged / inaccessible | Skip |

## Per-edge notes (compressed)

**1. Mean reversion (flagship test).** Prefer regime-gated liquid versions (e.g. IBS / RSI-type / band signals + slow trend filter). Bare single-indicator versions have decayed in published windows. Guard against **filter-stacking overfit**. See [backtesting & overfitting](../ml-stats/concepts/backtesting-overfitting.md).

**2. Regime / vol gating.** Real-time “vol-managed portfolios beat unmanaged” is fragile OOS in broad studies; the **robust benefit is left-tail reduction**. Use as a slow risk overlay and as a governor on leveraged vehicles — not as a stand-alone money printer.

**3. Momentum / rotation.** Simple dual-momentum implementations often **decay post-publication**. Keep low-turnover absolute momentum as ballast, not as an income claim. See [momentum](../systematic-trading/factors-signals/momentum.md).

**4–6. PEAD, calendar, overnight/gap.** Academic edges in liquids are largely decayed or cost-eaten; dedicated overnight products have liquidated; gap-fill base rates often fail re-derivation. Keep only directional *filters*, not standalone strategies.

**7. Leveraged-ETF tactics.** Rebalance front-running and “decay harvest” fail as retail long-only edges. Leverage scales variance roughly with the square of the multiple and adds financing drag. See [leveraged-ETF decay](../shared/concepts/leveraged-etf-decay.md).

**8. Structural retail advantages.** Near-zero impact and freedom to hold cash are real **constraints**, not strategies. “Alpha hides only in microcaps” is largely refuted for implementable retail books once costs are honest.

## Program implications

- Reframe “steady income” as **regime-gated swing process + survival overlay**, not intraday churn.
- Model **post-promo** costs and local tax before declaring a pass.
- Carry leverage rules as **hard constraints**: no multi-day 3× in chop; size via the regime gate; never be the forced seller.

## Related

- [Retail-capital edge program](retail-capital-edge-program.md) · [Alpha map](alpha-map.md)
- [Risk of ruin](../shared/concepts/risk-of-ruin.md) · [Who wins](../shared/concepts/who-wins-empirical-record.md) · [Disposition effect](../shared/concepts/disposition-effect.md)
