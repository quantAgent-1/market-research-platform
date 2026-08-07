---
type: research-brief
title: "Trading-System Strength Metrics (Deep-Research Brief, June 2026)"
description: Verified evidence on the metrics that measure a trading system — and which separate a real edge from an overfit backtest. Sharpe is standard but provably gameable (annualization, skew, option/leverage gaming); CVaR is coherent, VaR is not; the Deflated Sharpe Ratio is the key edge-vs-overfit gate. No single metric — a layered scorecard.
tags: [ml-stats, systematic-trading, evaluation, risk, metrics, evidence]
timestamp: 2026-06-21T00:00:00Z
status: active
sources: []
---

# Trading-System Strength Metrics — Deep-Research Brief

**Source:** Claude Code `deep-research` run `wf_e98fa861-ce5` (2026-06-21). This was **Part B** of a
two-part request; an earlier pass **walled hard on the quota mid-fetch** (all verifiers abstained → a
spurious "all refuted") → **resumed past the 2:20pm KST reset** → clean.
**Method:** 5 angles → 24 sources → 102 claims → 25 adversarially verified → **23 confirmed, 2 refuted →
14 findings.** Primary-sourced: Lo 2002, Goetzmann-Ingersoll-Spiegel-Welch, Keating-Shadwick (Omega),
Magdon-Ismail et al. (drawdown), Rockafellar-Uryasev + Artzner-Delbaen-Eber-Heath (coherence), Bailey &
López de Prado (DSR). **Evidence/education, not investment advice.** Companion to the
[stop-loss brief](deep-research-stop-loss-optimization-2026.md) (Part A).

## The one-paragraph answer
**No single metric measures system strength** — the literature converges on a **layered scorecard**:
a risk-adjusted-return measure + a drawdown/tail measure + (most decisively) a **multiplicity/non-
normality deflation gate**. The **Sharpe ratio is the lingua franca but provably gameable** (bad
annualization, skew-blindness, informationless inflation). For tails, **CVaR is coherent and VaR is
not.** And the layer that actually **separates a genuine edge from an overfit backtest is the Deflated
Sharpe Ratio** — because the expected *maximum* Sharpe across N trials is strictly positive even with
zero skill, a backtested Sharpe is meaningless unless it clears that multiplicity-adjusted bar.

## Confirmed findings

### Risk-adjusted return — Sharpe is standard but gameable
- **Annualization is i.i.d.-only.** The √T rule (S_T = S₁·√T) is Sharpe's own and holds **only at zero
  serial correlation**; general case SR(q)=SR·q/√η(q), η(q)=q(1+2Σ(1−k/q)ρ_k). Autocorrelation/smoothing
  inflates annualized Sharpe; **up to 65% overstatement** in Lo's hedge-fund example, and rankings change
  materially. (Lo 2002; Sharpe 1994) [3-0]
- **Inflatable with NO skill** two ways (Goetzmann-Ingersoll-Spiegel-Welch): (1) **static option-like
  payoffs** — selling NTM options lifts Sharpe 0.631→0.731 with *one* contract (86% of the max gain);
  (2) **dynamic leverage** applied whenever performance-to-date is negative. Motivates the
  **Manipulation-Proof Performance Measure (MPPM)**. [3-0]
- **Sharpe-maximization mechanically manufactures negative skew** — frequent small gains, rare large
  loss (≈ short OTM puts+calls); a potentially "ubiquitous **peso problem**" wherever high Sharpe is
  rewarded. Screening on high Sharpe selects for hidden crash risk. *(Scoped: exact for fixed-mean
  Sharpe-max; trend-following can pair positive Sharpe with positive skew.)* [3-0]
- **Sharpe is skew-blind:** two assets with identical mean/variance/kurtosis but opposite skew are
  indistinguishable to mean-variance, yet the negatively-skewed one had **~5× the probability of a −4σ
  loss** (Keating-Shadwick's example, verbatim from the primary PDF; a secondary source cites ~3× for a
  related illustration). The case for downside/distribution-aware measures. [3-0]
- **Omega** = prob-weighted gains-above-threshold ÷ losses-below; the full Omega *function* encodes **all
  moments** (no distributional assumption). *(Nuance: equivalence holds for the whole function, not a
  single-threshold value; Omega-optimization has its own critiques.)* [3-0]

### Trade-level — expectancy, not win rate
- **Expectancy** (Van Tharp) = mean **R-multiple** of the trade distribution = total R ÷ #trades;
  **E = win%·avgWin − loss%·avgLoss**. Needs ~30 trades minimum, 100-200 for clarity. [3-0]
  *(Practitioner heuristic; the 30-trade floor is statistically weak for fat-tailed R-distributions.)*
- **Win rate alone misleads:** a **1% win rate can be +EV** (99×−$1 + 1×$500 = **+$401**). Profit is
  driven by **expectancy × frequency**, win rate combined with payoff ratio (avgWin/avgLoss). [3-0]

### Drawdown & tail
- **Max drawdown is drift/regime-dependent and not cross-comparable:** E[MDD] grows **logarithmically
  (μ>0) / as √T (μ=0) / linearly (μ<0)** in horizon (Magdon-Ismail et al. 2004). Comparing raw max-DDs
  across strategies of different drift/horizon is misleading. [3-0] *(Refuted: the collapsed
  single-scaling closed-form + zero-drift constants — use only the three asymptotic regimes.)*
- **CVaR is coherent; VaR is not.** A coherent measure satisfies translation-invariance, **subadditivity**,
  positive homogeneity, monotonicity (Artzner-Delbaen-Eber-Heath). **VaR fails subadditivity** → a merged
  portfolio can show *more* VaR than the sum of parts (penalizes diversification; lets a trader split
  accounts to lower margin). **CVaR ≥ VaR always**; VaR also ignores loss magnitude beyond the threshold
  and is "biased toward optimism" (Rockafellar-Uryasev). Basel FRTB switched VaR→Expected Shortfall. [3-0]

### Robustness / does-the-edge-survive — the decisive layer
- **★ Deflated Sharpe Ratio (Bailey & López de Prado 2014)** corrects Sharpe for **selection bias under
  multiple testing AND non-normality** at once. It's a Probabilistic Sharpe Ratio whose rejection
  threshold is the **expected MAXIMUM Sharpe across N trials** (False Strategy Theorem) — strictly
  **positive even at zero true skill, and growing with N**. Deflates by skewness, kurtosis, sample length
  T, variance of trial Sharpes, and N. **⇒ A backtest Sharpe reported without N is uninterpretable;
  screening thousands of variants reliably manufactures high-Sharpe flukes.** [3-0]

## What got refuted / NOT verified
- **Refuted (do NOT cite):** the collapsed closed-form E[MDD]=(2σ²/μ)·Q(γ) with γ=μ√(T/2σ²) (1-2); the
  zero-drift constants Q(x)=√(π/2)x, γ≈0.6267 (0-3). Use only Magdon-Ismail's three growth regimes.
- **Named but NOT independently verified this run (cite primaries directly, treat as lower-confidence):**
  the **t≥3** factor hurdle (Harvey-Liu-Zhu); **PBO** & **Minimum Backtest Length** (Bailey-Borwein-LdP-Zhu,
  AMS "Pseudo-Mathematics" 2014); **Sortino** (downside-deviation) & **Young 1991 Calmar/MAR** formulas;
  **Information ratio**; **Ulcer index / Pain ratio**; explicit **Kelly / risk-of-ruin** formulas;
  skew/kurtosis as standalone metrics.

## Caveats
- **Citation-provenance fixes:** the tandfonline DOI 10.2469/faj.v58.n4.2453 resolves to **Lo (2002)**,
  not Sharpe; the option/dynamic-leverage/"peso" examples are verbatim from **"Sharpening Sharpe Ratios"
  (NBER w9116, 2002)**, not the 2007 RFS "Manipulation-Proof" paper (same four authors, same line).
- **Forecast/heuristic vs theorem:** coherence axioms, Sharpe annualization, drawdown asymptotics,
  CVaR≥VaR, DSR construction are **theorems** (don't decay). The **thresholds** (Sharpe >1 good / >2 very
  good / >3 excellent; Calmar >0.5/>1; profit factor >1.5-2) are **practitioner heuristics**, not verified.
- **Source tiers:** risk-adjusted/tail/DSR rest on peer-reviewed primaries; trade-level (expectancy,
  R-multiples) rests on Van Tharp (practitioner-standard, not peer-reviewed).

## Open questions
1. Primary derivation of the **t≥3** hurdle and how Harvey-Liu-Zhu's multiple-testing adjustment relates
   numerically to the DSR's expected-max-Sharpe threshold.
2. **PBO** (combinatorially-symmetric CV) + **Minimum Backtest Length** computation and the practical
   overfit cutoff (is PBO>0.5 the line?).
3. Primary formulas/thresholds for **Sortino, Calmar (Young 1991), Information ratio, Ulcer/Pain**.
4. Quantitative link from **expectancy/R-multiples to Kelly / risk-of-ruin** (optimal-f, fractional Kelly)
   given fat-tailed R-distributions.
5. Do **MPPM/DSR actually predict OOS skill**, or merely detect in-sample gaming (Brown/Kang critiques)?

## Feeds into the wiki
- Creates: [Trading-system performance metrics](../ml-stats/concepts/performance-metrics.md)
- Connects: [Backtesting & overfitting](../ml-stats/concepts/backtesting-overfitting.md) (DSR/PBO is the
  same multiplicity logic) · [Risk of ruin](../shared/concepts/risk-of-ruin.md) ·
  [Kelly criterion](../shared/concepts/kelly-criterion.md) ·
  [Trading-system fundamentals](../synthesis/trading-system-fundamentals.md) ·
  [Transaction costs](../shared/concepts/transaction-costs.md) ·
  [Stop-loss optimization brief](deep-research-stop-loss-optimization-2026.md).

## Primary / key sources
- Lo (2002), "The Statistics of Sharpe Ratios," FAJ 58(4) — https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios
- Sharpe (1994), "The Sharpe Ratio," JPM 21(1) — https://web.stanford.edu/~wfsharpe/art/sr/sr.htm
- Goetzmann, Ingersoll, Spiegel & Welch, "Sharpening Sharpe Ratios" (NBER w9116, 2002) — https://www.nber.org/system/files/working_papers/w9116/w9116.pdf · RFS 2007 (Manipulation-Proof) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=302815
- Keating & Shadwick (2002), "A Universal Performance Measure" (Omega) — https://people.duke.edu/~charvey/Teaching/BA453_2004/Keating_A_universal_performance.pdf
- Magdon-Ismail, Atiya, Pratap & Abu-Mostafa (2004), "On the Maximum Drawdown of a Brownian Motion," J. Applied Probability 41(1) — https://www.cs.rpi.edu/~magdon/ps/journal/drawdown_journal.pdf
- Rockafellar & Uryasev (2002), "CVaR for General Loss Distributions," JBF 26 — https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf
- Artzner, Delbaen, Eber & Heath (1999), "Coherent Measures of Risk," Math. Finance 9(3) — https://www.researchgate.net/publication/227614132_Coherent_Measures_of_Risk
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio," JPM 40(5) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- Van Tharp, "Tharp Think" / "Trade Your Way to Financial Freedom" (expectancy, R-multiples) — https://vantharpinstitute.com/tharp-think-trading-concepts/
- (Unverified-this-run, cite directly) Harvey-Liu-Zhu (2016) t≥3; Bailey-Borwein-LdP-Zhu (2014) PBO/Min-Backtest-Length, AMS Notices 61(5).
