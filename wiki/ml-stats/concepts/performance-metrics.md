---
type: concept
title: Trading-System Performance Metrics
description: How to measure a trading system's strength — and which metrics separate a real edge from an overfit backtest. No single metric: a layered scorecard (risk-adjusted return + drawdown/tail + a deflation/robustness gate). Sharpe is standard but gameable; the Deflated Sharpe Ratio is the key edge-vs-overfit test.
tags: [ml-stats, systematic-trading, evaluation, risk, metrics]
timestamp: 2026-06-21T00:00:00Z
status: active
sources: [../../sources/deep-research-trading-system-metrics-2026.md]
---

# Trading-System Performance Metrics

**There is no single number for "system strength."** The evidence supports a **layered scorecard** — a
risk-adjusted-return measure, a drawdown/tail measure, and (most decisively) a **deflation/robustness
gate** — because the return ratios describe a *track record* but are individually gameable and say
nothing about whether the edge survives the *search process* that produced it. This is the evaluation
companion to [backtesting & overfitting](backtesting-overfitting.md), and the measurement layer of the
[trading-system fundamentals](../../synthesis/trading-system-fundamentals.md) thesis (Edge × Risk ×
Implementation).

## Layer A — risk-adjusted return (necessary, not sufficient; gameable)
**Sharpe ratio** = (return − rf) / σ is the lingua franca, but it has three documented failure modes:
- **Annualization is i.i.d.-only.** The √T rule (multiply by √12 monthly→annual, √252 daily→annual) holds
  *only* at zero serial correlation. Smoothed/illiquid (autocorrelated) returns inflate it — **up to 65%
  overstatement** in Lo's hedge-fund example, enough to reorder rankings (Lo 2002).
- **Inflatable with no skill.** Selling near-the-money options or applying leverage conditional on
  underperformance raises Sharpe *informationlessly* (Goetzmann-Ingersoll-Spiegel-Welch). The
  **Manipulation-Proof Performance Measure (MPPM)** is the gaming-resistant alternative.
- **Skew-blind → "peso problem."** Maximizing Sharpe for a fixed mean *mechanically* produces frequent
  small gains + rare large losses (negative skew). Two assets identical in mean/variance/kurtosis but
  opposite in skew are equal to Sharpe, yet differ ~5× in catastrophic-loss probability (Keating-Shadwick).

**Read alongside distribution-aware measures:** **Sortino** (volatility → downside deviation below a
target), **Omega** (probability-weighted gains/losses about a threshold; the full Omega *function*
encodes all moments), and **Calmar/MAR** (annual return ÷ max drawdown). *Heuristic thresholds (not
rigorously verified): Sharpe >1 good / >2 very good / >3 excellent; Calmar >0.5 acceptable / >1 good.*

## Layer B — trade-level: expectancy, not win rate
- **Expectancy is the metric to keep positive** — the mean **R-multiple** (each trade's P/L ÷ initial
  risk R): **E = win% × avgWin − loss% × avgLoss**. Compounding ≈ **expectancy × trade frequency**.
- **Win rate alone misleads:** a **1% win rate can be profitable** (99 × −$1 + 1 × $500 = **+$401**).
  Always pair win rate with the **payoff ratio** (avgWin/avgLoss). *(Van Tharp framework; practitioner
  heuristic — the ~30-trade "significance" floor is statistically weak for fat-tailed R-distributions.)*
- **Profit factor** = gross profit ÷ gross loss (>1 = profitable; ~1.5–2 often called healthy) — a
  positive expectancy ⇔ profit factor > 1.

## Layer C — drawdown & tail (use coherent measures, contextualize by regime)
- **Max drawdown is drift/regime-dependent, NOT cross-comparable.** Expected max drawdown grows
  **logarithmically (μ>0) / as √T (μ=0) / linearly (μ<0)** in horizon (Magdon-Ismail et al. 2004) — so
  comparing raw max-DDs across strategies of different drift/length is misleading; normalize first.
- **CVaR (expected shortfall) > VaR.** A **coherent** risk measure satisfies translation-invariance,
  **subadditivity**, positive homogeneity, monotonicity (Artzner-Delbaen-Eber-Heath). **VaR fails
  subadditivity** — it can penalize diversification and lets risk be hidden by splitting accounts — and
  it **ignores loss magnitude beyond the threshold** with an optimism bias. **CVaR ≥ VaR always** and is
  coherent (Rockafellar-Uryasev); Basel FRTB switched VaR→Expected Shortfall. Also report **skew,
  kurtosis, drawdown duration / time-to-recovery, Ulcer index**. Tail sizing ties to
  [risk of ruin](../../shared/concepts/risk-of-ruin.md) and the [Kelly criterion](../../shared/concepts/kelly-criterion.md).

## Layer D — the robustness / deflation gate (what actually separates edge from overfit)
This is the layer most people skip and the one that matters most. A high *backtested* Sharpe is the
expected outcome of **searching**, not evidence of skill.
- **★ Deflated Sharpe Ratio (DSR)** (Bailey & López de Prado 2014) corrects Sharpe for **(1) selection
  bias under multiple testing and (2) non-normality** at once. It sets the significance threshold to the
  **expected *maximum* Sharpe across N trials** — which is **strictly positive even when true skill is
  zero, and grows with N**. Deflates by skew, kurtosis, sample length T, the variance of the trial
  Sharpes, and N. **⇒ A backtest Sharpe reported without N (how many configurations were tried) is
  uninterpretable.** This is the same multiplicity logic behind [backtesting & overfitting](backtesting-overfitting.md).
- **Companion robustness checks** (named in the literature; cite primaries directly): the **t ≥ 3**
  factor hurdle under multiple testing (Harvey-Liu-Zhu); the **Probability of Backtest Overfitting (PBO)**
  and **Minimum Backtest Length** (Bailey-Borwein-López de Prado-Zhu, "Pseudo-Mathematics…", AMS 2014);
  **out-of-sample / walk-forward degradation**; **capacity & turnover**; **parameter stability**.

## The scorecard (synthesis)
Evaluate a system on all three+gate layers, never one number:
1. **Risk-adjusted return** — Sharpe as the common language, *read with* Sortino/Omega to expose skew.
2. **Drawdown/tail** — regime-contextualized max-DD + **CVaR** (coherent) + Calmar.
3. **Robustness/deflation gate** — **DSR / multiplicity awareness** — the layer that distinguishes a real
   edge from curve-fitting.

Academics weight (3) + coherence most; practitioners lean on Sharpe/Calmar/drawdown + trade-level
expectancy. **Six ways metrics mislead (all verified):** (i) annualizing Sharpe by √T under
autocorrelation; (ii) high Sharpe via negative-skew/option/leverage gaming; (iii) judging a backtest
Sharpe without N; (iv) reading win rate alone; (v) VaR instead of CVaR; (vi) comparing raw max-DDs
across different drift/horizon.

## Relationships
- The multiplicity gate is the quantitative core of [backtesting & overfitting](backtesting-overfitting.md).
- Tail metrics + sizing → [risk of ruin](../../shared/concepts/risk-of-ruin.md) / [Kelly](../../shared/concepts/kelly-criterion.md).
- Net-of-cost evaluation needs [transaction costs](../../shared/concepts/transaction-costs.md).
- The measurement layer of [trading-system fundamentals](../../synthesis/trading-system-fundamentals.md);
  applied when judging [stop-loss](../../shared/concepts/stop-losses-and-exits.md) overlays (most reported
  stop-loss Sharpe gains are gross & in-sample).

## Open questions
- Numerical relation between the **t≥3** hurdle and the DSR expected-max-Sharpe threshold for given N.
- **PBO** computation + the practical overfit cutoff; **Minimum Backtest Length** in practice.
- Primary formulas/thresholds for **Sortino, Calmar (Young 1991), Information ratio, Ulcer/Pain**.
- Whether **DSR/MPPM predict OOS skill** or merely detect in-sample gaming.

## Sources
- [Deep-research brief: trading-system strength metrics (2026)](../../sources/deep-research-trading-system-metrics-2026.md)
  — Lo 2002; Goetzmann-Ingersoll-Spiegel-Welch; Keating-Shadwick (Omega); Magdon-Ismail (drawdown);
  Rockafellar-Uryasev + Artzner-Delbaen-Eber-Heath (CVaR/coherence); Bailey & López de Prado (DSR); Van Tharp.
