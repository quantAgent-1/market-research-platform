---
type: overview
title: The Alpha Model Book — the Actual Mathematics Run at Quant Shops
description: The rigorous model catalog behind the landscape page's sketches — full mathematical specifications with estimators, closed-form solutions, decision rules, and calibration constants. Avellaneda–Lee eigenportfolio stat-arb (the rigorous H2), OU/cointegration pairs with optimal bands, Avellaneda–Stoikov market making (HJB solution), microstructure alpha (Kyle λ, OFI, microprice, VPIN), TSMOM/EWMAC with vol-targeting math, GARCH/HAR-RV/VRP/SVI, Almgren–Chriss and the square-root law, Grinold's law with transfer coefficient, shrinkage and multivariate Kelly, the Hamilton regime filter, PBO/CSCV validation, and lead-lag estimators. Each model: who runs it, who pays, and whether this desk can use it.
tags: [systematic-trading, derivatives, ml-stats, model, microstructure]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: []
---

# The Alpha Model Book — the Actual Mathematics

> The [landscape page](../concepts/algorithmic-trading-landscape.md) sketched these models; this
> page writes them down properly — the level of rigor of enginev2's OU-MLE and order-imbalance
> work, extended across the industry's model families. Notation is plain-text on purpose (renders
> everywhere). ⚠️ Everything here is from-training: formulas are standard published results, the
> calibration constants are practitioner conventions — verify any number before it becomes
> load-bearing. Each section ends with **[who runs it · who pays · desk-usable?]**.

---

## 1. Eigenportfolio stat-arb — Avellaneda–Lee (2010): the rigorous form of H2

The canonical mid-frequency US stat-arb pipeline, and the mathematically complete version of the
engine's H2 cross-sectional reversal.

**Step 1 — factor extraction by PCA with Random Matrix Theory cleaning.**
Standardize returns `Y_it = (r_it − r̄_i)/σ_i`, form the empirical correlation matrix
`ρ = (1/T)·Y'Y`. Pure noise eigenvalues follow the Marchenko–Pastur law with upper edge:

```
λ+ = (1 + √(N/T))²        # for standardized returns, unit variance
```

Keep only eigenvalues above λ+ (US equities: typically ~10–20 "signal" factors out of N≈500).
The j-th **eigenportfolio** holds `Q_ij = v_ij / σ_i` (eigenvector components deflated by each
name's vol), with factor return `F_jt = Σ_i Q_ij · r_it`.

**Step 2 — residual extraction.** Regress each name on the kept factors:
`r_it = β_i0 + Σ_j β_ij·F_jt + ε_it`; the residual ε is the idiosyncratic return.

**Step 3 — OU model on the cumulative residual.** Let `X_it = Σ_{s≤t} ε_is`. Model
`dX = κ(m − X)dt + σ dW`. The exact discretization is an AR(1) — this is the same mapping v2's
OU MLE used:

```
X_{t+1} = a + b·X_t + ζ_t,   b = e^(−κΔt),  a = m(1−b),  Var(ζ) = σ²(1−b²)/(2κ)
```

OLS on the AR(1) gives `κ = −ln(b)/Δt`, half-life `= ln2/κ`, equilibrium volatility
`σ_eq = √(Var(ζ)/(1−b²))`.

**Step 4 — the s-score and the trading rule.**

```
s_it = (X_it − m_i) / σ_eq,i
open short  s > +1.25       close short  s < +0.75
open long   s < −1.25       close long   s > −0.50
```

(the paper's calibrated thresholds), trading **only names whose estimated half-life is short
relative to the estimation window** (the paper required mean reversion faster than ~1/2 the
60-day window — κ implying half-lives under ~30 days; slower fits are statistically unreliable).
Positions are held factor-hedged (short the eigenportfolio exposures), so P&L is the residual's
mean reversion, not market direction.

**Honest record:** in-paper Sharpe ≈ 1.4 (2003–07); the strategy famously degraded through
Aug-2007 (the Khandani–Lo quant quake *is* this trade crowding) and gross returns compressed
after 2008. The **payer is liquidity provision** — the same as simple reversal, with better
hedging. **[stat-arb pods, EMN funds · Service payer · YES at daily horizon — this is H2's
upgrade path once the PIT lake exists]**

---

## 2. Cointegration pairs with optimal bands

**Finding the spread.** Engle–Granger: regress `P1 = c + γ·P2 + u`, ADF-test û for stationarity.
Johansen (multivariate, the institutional standard): in the VECM

```
ΔY_t = Π·Y_{t−1} + Σ_{i=1..p−1} Γ_i·ΔY_{t−i} + ε_t
```

the rank r of Π equals the number of cointegrating relations (`Π = αβ'`; β = the cointegrating
vectors, α = adjustment speeds), tested with the trace statistic `−T·Σ_{i>r} ln(1−λ̂_i)`.

**Trading the spread.** Fit `S_t = β'Y_t` to the OU/AR(1) machinery of §1. The *optimal*
entry/exit levels solve a free-boundary problem (Leung–Li 2015 give the ODE system); the
practitioner shortcut is to choose the band z* maximizing **expected profit per unit time**:

```
g(z) = (2z·σ_eq − round-trip cost) / E[τ_cycle(z)]
```

with E[τ] from OU first-passage times — numerically z* lands around **0.75–1.5·σ_eq** for costs
in the 5–20%-of-σ_eq range. Wider costs → wider bands, fewer cycles. A structural-break monitor
(v2's BreakDetector: CUSUM on the spread's innovations, or a rolling Johansen re-test) is
mandatory: **the fat tail of pairs trading is cointegration death**, not noise.
**[EMN/relative-value desks · Service + Mistake · YES — v2's OU code transfers directly]**

---

## 3. Market making — Avellaneda–Stoikov (2008), the HJB solution

Mid-price `dS = σ dW`; the MM controls bid/ask offsets δ_b, δ_a; fills arrive Poisson with
intensity `λ(δ) = A·e^(−kδ)`; exponential utility with risk aversion γ. Solving the
Hamilton–Jacobi–Bellman equation yields two famous closed forms — the **reservation price**
(inventory-skewed fair value) and the **optimal total spread**:

```
r(s, q, t) = s − q·γ·σ²·(T−t)                       # q = signed inventory
δ_a + δ_b  = γ·σ²·(T−t) + (2/γ)·ln(1 + γ/k)
```

Quotes are placed symmetric around r, not around mid — inventory risk literally *moves your
fair value*. Calibration: k from regressing ln(fill rate) on quote distance; A from baseline
arrival counts; σ from realized vol. The Guéant–Lehalle–Tapia extension adds hard inventory
bounds and gives stationary asymptotics where the skew is linear in q with slope
`∝ √(γσ²/(2kA))` ⚠️ (structure right, constant from memory). **[Citadel Sec/Virtu/Optiver tier,
with speed and queue models on top · Service payer (the spread) · NO — quoting rights + latency
gated; v2's microprice/imbalance features were the *sensing* half of this model]**

---

## 4. Microstructure alpha — impact, imbalance, toxicity

**Kyle (1985) — why impact IS information.** Informed trader with signal v ~ N(μ, Σ₀), noise
flow u ~ N(0, σ_u²); the market maker prices linearly `P = μ + λ(x+u)` and the insider trades
`x = (v−μ)/(2λ)`. Equilibrium:

```
λ = √Σ₀ / (2σ_u)      # price impact per unit net flow
```

Impact is the market's Bayesian update on flow — the theoretical foundation for "trades move
price by changing beliefs," already encoded in the [price-formation page](../../shared/concepts/price-formation-and-the-float-identity.md).

**Order Flow Imbalance (Cont–Kukanov–Stoikov 2014) — the tradeable version.** At the best
quotes, each event n contributes

```
e_n = 1{P_n^b ≥ P_{n−1}^b}·q_n^b − 1{P_n^b ≤ P_{n−1}^b}·q_{n−1}^b
    − 1{P_n^a ≤ P_{n−1}^a}·q_n^a + 1{P_n^a ≥ P_{n−1}^a}·q_{n−1}^a
```

and `OFI_k = Σ e_n` over window k. The regression `ΔP_k = β·OFI_k + ε` explains **~65% of
10-second price variance**, with β inversely proportional to depth — one of the cleanest
empirical relations in market data. This is the rigorous ancestor of v2's imbalance tracker.

**Microprice (Stoikov 2018).** The martingale-fair price given imbalance
`I = q_b/(q_b + q_a)` and spread s: `P^micro = E[mid_∞ | I, s]`, computed as the fixed point of
a Markov chain over (I, s) states; first-order behavior ≈ `mid + (s/2)·(2I−1)` with the exact
adjustment estimated from data. Better short-horizon predictor than mid or weighted-mid.

**VPIN (Easley–López de Prado–O'Hara).** Volume-bucketed toxicity:
`VPIN = Σ_buckets |V_buy − V_sell| / (n·V)` with buy/sell classified in bulk via
`V_buy = V·Φ(ΔP/σ_ΔP)`. **Contested** — Andersen–Bondarenko and Duarte–Hu–Young show much of its
predictive content is volatility in disguise; the wiki's informed-flow page already carries this
caveat. **[HFT/execution desks · Service/adverse-selection avoidance · partially — the daily-bar
cousins (signed turnover imbalance, and Korea's *published cohort flows*, which are OFI-like
information handed to you for free at daily frequency) are exactly lanes 1–2 of the alpha map]**

---

## 5. Trend following — TSMOM / EWMAC with the vol-targeting arithmetic

**TSMOM (Moskowitz–Ooi–Pedersen 2012).** Per market m:

```
position_mt = sign(r_m, t−252:t) · (σ_target / σ̂_mt)
σ̂ (exp-weighted, ~60-day center of mass);  portfolio = equal risk across ~50–150 markets
```

Documented t-stats 3–5 across 58 futures markets 1985–2009; diversified Sharpe ≈ 1 pre-cost —
the signal is trivial, the wrapper (vol targeting + breadth across assets) is the product.

**EWMAC (the AHL/Carver form).** `raw = (EWMA_16(P) − EWMA_64(P)) / σ_P`, scaled to a forecast
`f = 10·raw/E|raw|` capped at ±20, then

```
position = f/10 · (capital·σ_target) / (σ_instrument·price·point_value)
```

Multiple speeds (2/8, 4/16, … 64/256) are combined with a correlation-aware weighting — same
Grinold logic, applied to speeds. Why it persists: the payers are slow-rebalancing constraint
flow and behavioral anchoring, and the strategy's crisis convexity (12-month-horizon payoff
resembles a long straddle) makes it *hedge-like*, so holders tolerate its long flat stretches.
**[CTAs: AHL/Winton/Aspect · Constraint + Mistake · YES conceptually — but futures access is the
gate; the ETF long-only version is H3's ballast]**

---

## 6. Volatility models — forecasting and the premium

**GARCH(1,1):** `σ²_t = ω + α·ε²_{t−1} + β·σ²_{t−1}`; equity-index persistence α+β ≈ 0.98;
h-step forecast mean-reverts geometrically: `σ²_{t+h} − σ̄² = (α+β)^h·(σ²_t − σ̄²)`.

**HAR-RV (Corsi 2009) — the industry forecasting default.** With RV from 5-minute returns
(`RV_t = Σ r²_5min`, two-scale corrected for noise):

```
RV_{t+1} = β0 + βD·RV_t + βW·(1/5)Σ_{i=0..4}RV_{t−i} + βM·(1/22)Σ_{i=0..21}RV_{t−i} + ε
```

Three horizons of memory (day/week/month) capture the volatility cascade; one-day-ahead R² ≈
0.5–0.7 — it beats GARCH out of sample and takes five minutes to estimate by OLS.

**The variance risk premium.** `VRP_t = IV²_t − E_t[RV²]` averages ~2–3 vol points on the S&P —
the price of crash insurance, harvested by delta-hedged short options/variance swaps. The payer
is genuine (insurance demand), the payoff is short-tail — the desk's exclusion (ruin-shaped at
this size) stands.

**SVI (Gatheral) — the surface parameterization.** Total implied variance per expiry:

```
w(k) = a + b·(ρ·(k−m) + √((k−m)² + σ²))     # k = log-moneyness
```

five parameters per slice, with no-arbitrage constraints (butterfly: g(k) ≥ 0; calendar: w
non-decreasing in T). Vol desks fit SVI, then trade violations and relative-value across the
surface. **[vol funds/dealer desks · Premium (insurance) · surface math YES for *reading*
(S2′ archive), harvesting NO]**

---

## 7. Optimal execution — Almgren–Chriss and the square-root law

**Almgren–Chriss.** Sell X over [0,T] minimizing `E[cost] + λ·Var[cost]`, temporary impact η·v,
permanent γ·v, vol σ. Optimal trajectory:

```
x(t) = X · sinh(κ(T−t)) / sinh(κT),    κ = √(λσ²/η)
```

λ→0 gives VWAP-like linear; higher risk aversion front-loads. This machine *prices the
urgency/impact tradeoff* — it is why unwinds take days and why the [liquidity-cascade page's](../../shared/concepts/liquidity-cascades-and-v-reversals.md)
"flow moves end at a quantity" clock exists.

**The empirical square-root law (Bouchaud et al.):**

```
impact ≈ Y · σ_daily · √(Q / ADV),   Y ≈ 0.5–1   (universal across venues, decades, asset classes)
```

Concave — the 10th percent of an order costs less than the 1st. The **propagator model** explains
how autocorrelated order flow (sign autocorrelation decaying like τ^−γ, γ≈0.5) coexists with
diffusive prices: `P_t = Σ_{s<t} G(t−s)·ξ_s`, with the decay kernel G(τ) ∝ τ^−β tuned such that
predictable flow is exactly offset by decaying impact. **[every execution desk · you pay this;
TCA measures your share · YES — the √-law belongs in the cost model now]**

---

## 8. Portfolio mathematics — the laws that size everything

**Grinold's Fundamental Law, complete form:**

```
IR = TC · IC · √BR
```

IC = corr(forecast, outcome); BR = *independent* bets/year; **TC = transfer coefficient** =
corr(actual positions, unconstrained optimal) — the term everyone forgets. Long-only with caps
runs TC ≈ 0.3–0.6: **the long-only constraint costs 40–70% of the achievable IR before anything
else goes wrong.** (This is the mathematically honest statement of the desk's "no short leg"
handicap.)

**Combining alphas (Qian–Hua).** Treat each signal's IC time series as a return stream; optimal
combination weights `w ∝ Σ_IC⁻¹ · μ_IC` (mean-variance on ICs). Two signals with equal IC and
IC-correlation ρ deliver combined `IC_c = IC·√(2/(1+ρ))` — the whole diversification argument in
one line.

**Covariance shrinkage (Ledoit–Wolf):** `Σ̂ = δ·F + (1−δ)·S`, S = sample, F = structured target
(constant-correlation), δ* = (estimation error of S)/(dispersion between S and F), both computable
in closed form. At N=200, T=500, raw S is near-singular; shrinkage is not optional.

**Multivariate Kelly:** `f* = Σ⁻¹μ` (log-utility, unconstrained), growth
`g = r + f'μ − ½f'Σf`. Estimation error makes full Kelly explosive — hence fractional (the
campaign's 0.37× convention is exactly this shrinkage applied to an assumed edge).

**Black–Litterman (view combination):**
`μ_post = [(τΣ)⁻¹ + P'Ω⁻¹P]⁻¹ · [(τΣ)⁻¹π + P'Ω⁻¹q]` — Bayesian blend of equilibrium (π) and
views (q); at shops it's the machinery for mixing discretionary views into quant books without
letting either dominate. **[everyone above retail · n/a (risk math) · YES — Grinold/LW/Kelly are
load-bearing for v3 already]**

---

## 9. Regime detection — the Hamilton filter

Two-state Markov switching, `r_t | S_t=j ~ N(μ_j, σ_j²)`, transition matrix P. The filter is two
lines, run forward:

```
predict:  ξ_{t|t−1} = P' · ξ_{t−1|t−1}
update:   ξ_{t|t}   = (ξ_{t|t−1} ⊙ η_t) / 1'(ξ_{t|t−1} ⊙ η_t),   η_t = state likelihoods of r_t
```

Parameters by EM (Baum–Welch). Run on (daily return, log RV) pairs it produces
P(high-vol regime) — the probabilistic upgrade of H1's binary 200-DMA gate, and the standard
"regime overlay" at funds. Two states are robust; five states are a curve fit.
**[macro/multi-strat overlays · risk shaping, not alpha · YES]**

---

## 10. Validation mathematics — DSR's companion, PBO

The [solution sheet](../../synthesis/institution-grade-solution-sheet.md) carries the deflated
Sharpe formula. Its companion at shops is **PBO via CSCV** (Bailey–Borwein–López de Prado–Zhu):
split the sample into S blocks; for every one of C(S, S/2) in-sample/out-of-sample combinations,
pick the best strategy in-sample and record its **relative rank** out-of-sample;

```
PBO = fraction of combinations where the IS-winner ranks below median OOS
```

PBO near 50% = your selection process is pure noise. Report DSR and PBO together: DSR asks "is
this Sharpe real given how many things I tried," PBO asks "does my *selection procedure* pick
skill at all." **[research governance everywhere · self-defense · YES — cheap to add to the
harness]**

---

## 11. Lead–lag estimation (lane 4's mathematics)

For the Asia→US chain, two tools: the **controlled lagged regression**

```
gap_US,t = a + Σ_l b_l·x_KR,t−l + c·ES_move_since_Seoul_close + ε     # Newey–West errors
```

where the ES-futures control is the whole game (if futures already moved, there is no edge — the
alpha-map's kill test, made precise); and the **Hayashi–Yoshida estimator** for correlation
between asynchronously-traded series (sum of return products over *overlapping* intervals —
consistent without synchronization, unlike naive resampling which biases toward zero).
**[cross-asset/ADR desks · Mistake/attention · YES — natively]**

---

## 12. The honest map: model → payer → tier → this desk

| model | payer | who runs it | desk-usable? |
|---|---|---|---|
| Avellaneda–Lee eigen stat-arb | Service (liquidity) | EMN/pods | **yes** — H2's rigorous form (needs PIT lake) |
| OU/cointegration pairs | Service + Mistake | EMN | **yes** — v2 code transfers |
| Avellaneda–Stoikov MM | Service (spread) | HFT MMs | no — speed/quoting gated; sensing only |
| OFI / microprice | adverse-selection avoidance | HFT/exec | daily-bar cousins only → **Korea cohort flows** |
| TSMOM / EWMAC | Constraint + Mistake | CTAs | ballast form (H3); futures gate the full version |
| HAR-RV / GARCH | n/a (forecasting) | everyone | **yes** — feeds H1 and sizing |
| VRP harvest / SVI | Premium (insurance) | vol funds | read yes, harvest no (ruin-shaped here) |
| Almgren–Chriss / √-law | you pay it | exec desks | **yes** — cost model + TCA |
| Grinold/Qian/LW/Kelly | n/a (sizing) | everyone | **yes** — already load-bearing |
| Hamilton filter | n/a (regime) | overlays | **yes** — H1 upgrade |
| DSR + PBO | n/a (governance) | good shops | **yes** — harness add |
| Lead–lag (HY, controlled lag) | Mistake/attention | cross-asset | **yes** — lane 4 |

The pattern: **the mathematics is public; the moats are data, speed, and discipline.** Every
"yes" above is a model whose equations this page just handed you; what converts them into alpha
is the PIT lake, the IC harness, and the kill tests — which is why the
[alpha map](../../synthesis/alpha-map.md) and the
[solution sheet](../../synthesis/institution-grade-solution-sheet.md) are this page's two
required companions.

## Same-day verification note (2026-07-07) — "are these production-grade or academic examples?"

Challenged by the user on filing day. Honest per-family grading, from training knowledge of what
shops actually deploy. Three grades: **production-as-is** (deployed in recognizable form),
**production-skeleton** (the concept ships, every component gets replaced), **teaching-level**
(the language of the field, not running code). Walk-backs recorded; the original sections above
stand unedited.

**Production-as-is (survives the challenge):**
- **TSMOM / EWMAC** — the strongest claim in the book. Carver's spec *is* an ex-AHL production
  description; AQR's managed-futures funds implement MOP-style TSMOM. Production adds carry,
  more horizons, correlation-weighted combination, capacity management — but the core is
  genuinely this simple.
- **SVI** — written *at Merrill for production*; SSVI/eSSVI descendants are standard desk
  surface fitters today.
- **√-impact law** — the production cost model at CFM/AQR-class shops, stable across decades;
  production-real as *cost*, never as alpha.
- **Grinold–Kahn + Barra-style factor models + Ledoit–Wolf** — the literal operating system of
  long-only systematic equity (the BGI→BlackRock lineage). The most production-faithful block on
  the page.
- **HAR-RV** — standard desk RV forecaster; production versions add implied-vol inputs
  (HAR-RV-IV), which beat pure realized models.
- **OFI / microprice** — real HFT/execution feature classes in active use; production versions
  are richer (multi-level, queue-aware), but these objects are deployed, not decorative.

**Production-skeleton (concept ships, textbook form doesn't):**
- **Avellaneda–Stoikov** — the inventory-skew + intensity *framework* is the shared language,
  and near-production in crypto MM and mid-tier desks (GLT came from practitioner work). But
  nobody at the Optiver tier quotes `γσ²(T−t)`: production replaces exponential intensities with
  empirical fill curves, adds queue-position value, adverse-selection alphas, fee/rebate
  optimization, and speed. Walk-back: my section implied closer production status than is true
  at the top tier.
- **Almgren–Chriss** — the optimizer skeleton inside broker algo suites, but η/γ are unstable to
  estimate, so production schedules are VWAP/POV/IS shells with TCA-regressed impact curves and
  a signal-driven child-order layer. Use it as *vocabulary* for the urgency/impact tradeoff.
- **Avellaneda–Lee eigen stat-arb** — honest status: a faithful *reconstruction of 2000s desk
  practice* (that's what the paper is), whose specific alpha (5-day residual reversal at ±1.25)
  is heavily decayed and whose parameters are illustrative. Modern pods keep the **shape**
  (residualize against a risk model, mean-revert/forecast the residual, factor-hedge, optimize)
  but: commercial risk models instead of raw PCA, an **ensemble of 50+ weak features** instead
  of one reversal signal, continuous sizing via expected-return-vs-cost instead of thresholds.
  The shape is production; the worked example is a museum piece with a working engine.
- **Kyle / Glosten–Milgrom** — conceptual foundations (why impact exists, what adverse selection
  is). Nobody "runs Kyle"; it prices nothing directly.
- **Johansen pairs on arbitrary stocks** — mostly dead/retail as written. Production relative
  value trades **structurally linked** instruments (dual listings, ADR/local, ETF/NAV, index
  arb, holdcos) where cointegration is contractual, then applies exactly the OU band math for
  entry/exit. The math survives; the universe choice is what changed.

**Teaching-level as trading rules (use with lowered priors):**
- **Hamilton 2-state filter as an exposure gate** — used as *one input* at macro shops; fragile
  out-of-sample. Production regime handling is usually either simpler (vol/drawdown rules — i.e.
  what H1 already is) or absorbed into feature sets. Keep as an H1 *candidate*, not an upgrade
  promise. Walk-back: "the standard regime overlay at funds" oversold it.
- **Raw/multivariate Kelly** — no production book runs `f* = Σ⁻¹μ`; vol targeting + risk limits
  are the deployed approximation. (Which is what the solution sheet specifies anyway.)
- **VPIN** — contested academically, tried and largely shelved in production.
- **Black–Litterman** — production in asset allocation/private-bank contexts; rare inside
  stat-arb.
- **PBO/CSCV** — best-practice governance advocated by López de Prado, adopted unevenly;
  most shops enforce the same goal through culture + holdouts. Still right for *this* harness.

**Where production alpha actually lives (the delta the question exposes):** at real shops the
published models are mostly **infrastructure** — execution, risk, sizing, market-making
mechanics. The *alpha* is: (1) **data advantage** — flow, positioning, transactions, NLP over
filings/calls; the formulas applied to it are often mundane (ranks, z-scores, event drift) —
*simple math on private data beats clever math on public data*; (2) **feature ensembles** —
50–500 weak signals combined by regularized ML under strict CV, no single named model;
(3) risk-model and optimizer quality; (4) execution cost edge; (5) capacity/turnover
engineering; (6) governance. The RenTec irony belongs here: its heritage is literally the
"academic" HMM/Baum–Welch family — applied with monstrous data work, engineering, and a single
integrated model. The model was never the moat; the operation was.

**Implication for this desk (why this verdict is good news):** the production formula — *public
mathematics × differentiated data × governance* — is exactly the wiki's build: the model book
supplies the public math, the [alpha map's](../../synthesis/alpha-map.md) Korea lanes supply the
differentiated data, the [solution sheet](../../synthesis/institution-grade-solution-sheet.md)
supplies the governance. Copy the shape, never the parameters; expect the worked examples'
specific numbers to be decayed; let the IC harness set every constant.

## Relationships

- **Vol. 2 — [The Production Model Book](production-model-book.md)**: the teaching tier discarded, the confirmed production track taken one level deeper (alpha-pool architecture, Barra construction, Gârleanu–Pedersen, the surviving factor library, ML-combiner spec, impact estimation, vol-desk stack, governance tools).
- Sketch-level map this page deepens: [Algorithmic-Trading Landscape](../concepts/algorithmic-trading-landscape.md)
- Where each model plugs in: [Alpha Map](../../synthesis/alpha-map.md) (lanes) · [Engine v3](../../synthesis/engine-v3/index.md) (H1–H5)
- The governance math around them: [Solution Sheet](../../synthesis/institution-grade-solution-sheet.md) · [Backtesting & Overfitting](../../ml-stats/concepts/backtesting-overfitting.md) · [Performance Metrics](../../ml-stats/concepts/performance-metrics.md)
- Doctrine: [Stochastic Optimal Control](../../shared/concepts/stochastic-optimal-control.md) · [Transaction Costs](../../shared/concepts/transaction-costs.md) · [Kelly](../../shared/concepts/kelly-criterion.md) · [Who Pays You](../../shared/concepts/who-pays-you.md)
