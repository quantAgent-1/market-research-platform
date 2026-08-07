---
type: research-brief
title: "The Equity Volatility Risk Premium (Deep-Research Brief, 2026)"
description: Fact-checked evidence on the equity-index volatility/variance risk premium — its magnitude, why it is an index (not single-name) phenomenon, risk vs mispricing, and only-modest net-of-cost survival.
tags: [derivatives, volatility, options, variance-risk-premium, evidence]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: []
---

# The Equity Volatility Risk Premium — Deep-Research Brief

**Source:** Claude Code `deep-research` workflow, run `wf_5605782f-ec1` (launched 2026-06-13;
verification + synthesis completed 2026-06-14 after a session-quota pause and **resume**).
**Method:** 5 angles → 23 sources → 111 claims → 25 adversarially verified (3-vote) →
**22 confirmed, 3 refuted → 7 synthesized findings.** Magnitude/structure findings rest on top-tier
peer-reviewed journals (RFS, *Journal of Finance*, JFE) + NBER; the one concrete net-of-cost figure
is from an AQR white paper (flagged below).
**Why this brief exists:** the [first brief](deep-research-long-term-profitability.md) found *no*
verifiable claim on the options VRP edge — this focused follow-up closes that gap.

## The one-paragraph answer
There **is** a large, robust **equity-index** volatility/variance risk premium: S&P 500
option-implied variance averages **roughly double** subsequently realized variance, the result is
highly significant across four independent top-tier studies, and standard risk factors explain
almost none of it. But three caveats define how usable it is: (1) it is an **index** phenomenon —
for **single-name** equity options the premium is small and mostly insignificant, because the index
premium is largely a **correlation** risk premium; (2) the bulk of it is **compensation for
jump/crash-tail risk** (with a genuine behavioural/demand component on top), i.e. you are paid to
*bear* crash risk, not handed a free mispricing; (3) **net of costs the edge is modest** — AQR's
delta-hedged put-writing backtest earns ~0.68 Sharpe (vs 0.32 for the S&P) with severe negative
skew, and the raw "information ratios > 3" are explicitly unreliable for such skewed payoffs.

## Confirmed findings (synthesized; each verified ≥2/3)

### 1. Magnitude — the index VRP is large, positive, and highly significant
S&P 500 mean implied variance **33.23 vs realized 14.93** (spread +18.30 pct², "almost always
positive"; [Bollerslev-Tauchen-Zhou 2009, RFS](https://public.econ.duke.edu/~boller/Published_Papers/rfs_09.pdf)).
Log VRP ln(RV/SW) = **−0.594 (t = −9.5)**, long variance-swap excess returns **< −50%/month**
([Carr-Wu 2009, RFS](https://engineering.nyu.edu/sites/default/files/2019-01/CarrReviewofFinStudiesMarch2009-a.pdf)).
Annualized pre-crisis premium **0.030** (risk-neutral 0.0576 − objective 0.0276;
[Bollerslev-Todorov 2011, JF](https://www2.nber.org/conferences/2010/APf10/Bollerslev_Todorov.pdf)).
Delta-hedged *long* SPX options "underperform zero"
([Bakshi-Kapadia 2003, RFS](https://academic.oup.com/rfs/article-abstract/16/2/527/1579962)).
Among the most-replicated stylized facts in empirical option pricing.

### 2. It's an index phenomenon — single names barely have it
Carr-Wu: NDX log VRP −0.207, but individual stocks only ~−0.02 to −0.05, significant for just
**21 of 35** (level premium significant for **3 of 35**). Index PUT excess returns far more negative
than single-name puts — the index-minus-individual difference runs **−7%/mo (ITM) to −39%/mo (OTM)**
([Driessen-Maenhout-Vilkov 2009, JF](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2009.01467.x)).
The market prices *systematic/index* variance, not idiosyncratic single-name variance.

### 3. Why the index? A correlation risk premium
Option-implied average equity correlation **46.7% vs realized 28.9%** (~17.8-pt gap) — "the first
evidence for a large correlation risk premium" (Driessen-Maenhout-Vilkov 2009, JF). Because
single-name options carry little variance premium, the index premium is essentially the **price of
correlation / lost-diversification risk.** *Caveat from the same paper:* this correlation premium
**"cannot be exploited with realistic trading frictions."**

### 4. Risk side — mostly compensation for jump/crash-tail risk
Factors don't explain it: CAPM alpha **−0.577 (t = −12.3)**, FF alpha −0.561 vs raw −0.594 (Carr-Wu).
Nonparametrically, **>half (≈69.8%: 59.8% left tail + 10% right)** of the index VRP is jump-tail
compensation — far above the ~20-24% in earlier parametric models — and the left/right asymmetry
implies much of it is **crash-fear** compensation
([Bollerslev-Todorov 2011, JF](https://www2.nber.org/conferences/2010/APf10/Bollerslev_Todorov.pdf)).
Most VRP return-predictability comes from the jump-tail component
([Bollerslev-Todorov-Xu 2015, JFE](https://public.econ.duke.edu/~boller/Published_Papers/jfe_15.pdf)).

### 5. Mispricing / demand side — also real
End users are **net long index options, especially OTM puts** — protective-put demand helps explain
index expensiveness and the smirk; for single stocks it's *call* demand that dominates
([Gârleanu-Pedersen-Poteshman 2009, RFS](https://academic.oup.com/rfs/article-abstract/22/10/4259/1590158);
[Bollen-Whaley 2004, JF](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2004.00647.x)).
Demand pressure moves option prices ∝ the variance of the unhedgeable part. AQR: ~**two-thirds of
investors** since 1989 believed in a >10% crash within 6 months vs a **~1% actual** base rate (Yale
survey). *Risk and demand/behavioural channels coexist; no verified claim pins the exact split, and
two stronger "demand-causes-it" claims were refuted.*

### 6. Net-of-cost survival — real but modest, and skew-laden
AQR's **delta-hedged 5%-OTM SPX put-writing** (1996-2016): **Sharpe 0.68** net of estimated
transaction costs (1.5% return, 2.2% vol, **−10% max drawdown**, 0.04 beta) vs **0.32** for passive
S&P 500 ([AQR 2018](https://www.aqr.com/Insights/Research/White-Papers/Understanding-the-Volatility-Risk-Premium)).
Carr-Wu's raw in-sample IRs **> 3** are flagged *by the authors themselves* as unreliable for
nonlinear, negatively-skewed payoffs. **Net edge exists but is modest and cost/skew-sensitive.**

### 7. Predictability — a real, time-varying wedge
The index VRP predicts aggregate market returns above traditional predictors, peaking
quarterly-to-annual: 3-month slope on (IV−RV) = **0.47 (t = 2.86), Adj R² 6.82%**
(Bollerslev-Tauchen-Zhou 2009). Even the skeptical Bekaert-Hoerova (2014) confirm "the variance
premium predicts stock returns."

## What got refuted (did NOT survive)
- "Single-stock options embed **no** VRP at all" — killed 0-3 (overstated; the *correlation
  decomposition* stands, but single names aren't strictly zero).
- "IV changes are directly driven by net public buying pressure" — killed 1-2 (directional
  demand-causality too strong).
- "Delta-neutral option-writing harvests abnormal returns equal to the IV-RV gap" — killed 0-3
  (overstates harvestability).

## Caveats (critical)
- **Sample vintage:** the strong magnitudes are from **old samples (1990-2007)**; they establish the
  *existence, size, and structure* of the index VRP as historical stylized facts, but **post-2010 /
  post-Volmageddon live-edge size is not established here** (AQR's 2016 endpoint is the most recent).
- **Four sub-questions NOT answered by verified evidence:** (1) the drawdown/crash profile in 2008 /
  Feb-2018 *Volmageddon*-XIV / March 2020 (AQR's −10% is a *delta-hedged, 5%-OTM* backtest that
  excludes the worst tail); (2) the geometric-growth / Kelly / risk-of-ruin cost of negative skew;
  (3) crowding/capacity decay and the short-vol-ETP blow-up; (4) the long-vol / tail-hedge
  (negative-carry) side. **Treat these as open.**
- **The one tradable number talks its book:** the 0.68 Sharpe is an AQR *illustrative, unit-levered,
  gross-of-fees* backtest on internal cost assumptions the disclosure admits "may not be realized."
  Sharpe is a poor risk measure for these payoffs.
- **Sign conventions differ** across papers (Carr-Wu VRP = RV − SW, so *negative* log VRP = realized
  < implied = premium to *sellers*; consistent in direction with BTZ's *positive* IV−RV). Not a
  contradiction.

## Open questions (a third run could target)
1. Post-2010 / post-Volmageddon magnitude & net-of-cost Sharpe — has the premium decayed as
   vol-selling crowded?
2. Drawdown / Kelly / risk-of-ruin cost of **unhedged** short-vol (straddles, CBOE PUT/WPUT,
   short-vol ETPs) in 2008 / 2018 / 2020.
3. Direct evidence of crowding & capacity limits (XIV/SVXY blow-up).
4. When does **buying** options / tail hedges pay despite negative carry?

## Feeds into the wiki
- New concept: [Volatility / Variance Risk Premium](../derivatives/concepts/volatility-risk-premium.md)
- Resolves the options-VRP open item in:
  [Implied vs realized volatility](../derivatives/concepts/implied-vs-realized-volatility.md) ·
  [Volatility arbitrage](../derivatives/strategies/volatility-arbitrage.md) ·
  [Trading-system fundamentals](../synthesis/trading-system-fundamentals.md)
- Connects to: [Risk of ruin](../shared/concepts/risk-of-ruin.md) (negative skew),
  [Transaction costs](../shared/concepts/transaction-costs.md),
  [Kelly criterion](../shared/concepts/kelly-criterion.md).

## Primary sources (verified)
- Carr & Wu (2009, RFS) — https://engineering.nyu.edu/sites/default/files/2019-01/CarrReviewofFinStudiesMarch2009-a.pdf
- Bollerslev, Tauchen & Zhou (2009, RFS) — https://public.econ.duke.edu/~boller/Published_Papers/rfs_09.pdf
- Bollerslev & Todorov (2011, JF) — https://www2.nber.org/conferences/2010/APf10/Bollerslev_Todorov.pdf
- Bollerslev, Todorov & Xu (2015, JFE) — https://public.econ.duke.edu/~boller/Published_Papers/jfe_15.pdf
- Bakshi & Kapadia (2003, RFS) — https://academic.oup.com/rfs/article-abstract/16/2/527/1579962
- Driessen, Maenhout & Vilkov (2009, JF) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2009.01467.x
- Gârleanu, Pedersen & Poteshman (2009, RFS) — https://academic.oup.com/rfs/article-abstract/22/10/4259/1590158
- Bollen & Whaley (2004, JF) — https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2004.00647.x
- AQR, "Understanding the Volatility Risk Premium" (2018) — https://www.aqr.com/Insights/Research/White-Papers/Understanding-the-Volatility-Risk-Premium
