---
type: concept
title: Volatility / Variance Risk Premium (VRP)
description: Equity-index option-implied variance systematically exceeds realized — a large, well-evidenced premium to option sellers that is an index (correlation) phenomenon, mostly crash-risk compensation, and only modestly profitable net of costs.
tags: [derivatives, volatility, options, variance-risk-premium, factor]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: [../../sources/deep-research-volatility-risk-premium.md]
---

# Volatility / Variance Risk Premium (VRP)

The **VRP** is the systematic gap by which option-**implied** (risk-neutral) variance exceeds the
variance the underlying subsequently **realizes** — the structural margin earned, on average, by
option *sellers*. It is the academic backbone of the
[implied-vs-realized vol edge](implied-vs-realized-volatility.md) and
[volatility arbitrage](../strategies/volatility-arbitrage.md). The
[2026 deep-research brief](../../sources/deep-research-volatility-risk-premium.md) verified its
existence and structure against top-tier journals while flagging hard limits on its tradability.

## 1. Magnitude (large, and well-replicated for the index)
For the S&P 500, implied variance averages **roughly 2× realized** (e.g. 33.23 vs 14.93, "almost
always positive"; Bollerslev-Tauchen-Zhou 2009). Carr-Wu (2009) find a log VRP of −0.594 (t≈−9.5)
with long variance-swap excess returns below −50%/month. One of the most-replicated facts in
empirical option pricing.

## 2. It's an INDEX phenomenon — single names barely have it
Strongly significant for SPX/OEX/DJX but small and mostly *insignificant* for individual stocks
(significant for ~21 of 35 in Carr-Wu). So the IV-RV "edge" is largely **absent in single-name
options**.

## 3. Why: a correlation risk premium
Implied equity correlation (~46.7%) far exceeds realized (~28.9%) — a large **correlation risk
premium** (Driessen-Maenhout-Vilkov 2009). Because single-name variance is barely priced, the index
VRP is essentially the price of **correlation / lost-diversification risk**. *Their caveat:* this
premium "cannot be exploited with realistic trading frictions."

## 4. Risk or mispricing? Both — but mostly crash-risk compensation
- **Risk (dominant):** standard factors explain ~none of it (CAPM alpha −0.577, t≈−12); **>half
  (~70%)** is compensation for **jump / crash-tail** risk, concentrated in the left tail
  (Bollerslev-Todorov 2011). You are *paid to bear crash risk*, not handed a free lunch.
- **Demand / behavioural (real, secondary):** end users are net-long index puts (protective-put
  demand bids up index IV; Gârleanu-Pedersen-Poteshman 2009, Bollen-Whaley 2004), and investors
  chronically *overestimate* crash odds (~⅔ expect a >10% crash within 6 months vs a ~1% base rate;
  AQR). The exact risk-vs-mispricing split is unresolved.

## 5. Does it survive costs? Yes, but modestly — and with ugly skew
AQR's delta-hedged 5%-OTM SPX put-writing earns ~**0.68 Sharpe** net of estimated costs (vs 0.32 for
the S&P), with a −10% max drawdown *in that hedged backtest*. Raw "information ratios > 3" for
shorting variance are explicitly unreliable because the payoff is **nonlinear and strongly
negatively skewed** — Sharpe understates the tail. This is the empirical anchor for Sinclair's
"short vol harvests the premium but carries negative skew / tail risk."

## What is NOT established (open)
- **Post-2010 / post-Volmageddon** magnitude — the strong evidence ends ~2007; present-day live size
  is unverified.
- **Unhedged** short-vol crash profile (2008, Feb-2018 XIV collapse, March 2020), and the
  [geometric-growth / Kelly / risk-of-ruin](../../shared/concepts/risk-of-ruin.md) cost of the skew.
- **Crowding / capacity** decay; the **long-vol / tail-hedge** (negative-carry) side.

## Relationships
- Realized via [volatility arbitrage](../strategies/volatility-arbitrage.md) /
  [dynamic hedging](dynamic-hedging.md); sized against
  [risk of ruin](../../shared/concepts/risk-of-ruin.md) and the
  [Kelly criterion](../../shared/concepts/kelly-criterion.md) because of the negative skew; bounded
  by [transaction costs](../../shared/concepts/transaction-costs.md). A textbook
  [risk premium that may decay](../../shared/concepts/factor-premia-and-alpha-decay.md) as it crowds.

## Sources
- [Deep-research brief: the equity volatility risk premium (2026)](../../sources/deep-research-volatility-risk-premium.md)
  — Carr-Wu (2009); Bollerslev-Tauchen-Zhou (2009); Bollerslev-Todorov (2011);
  Driessen-Maenhout-Vilkov (2009); Gârleanu-Pedersen-Poteshman (2009); Bakshi-Kapadia (2003);
  AQR (2018).
