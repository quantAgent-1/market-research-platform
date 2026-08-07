---
type: overview
title: The Production Model Book (Vol. 2) — What Actually Runs, One Level Deeper
description: The deeper production-grade catalog, teaching tier discarded per the Vol.-1 verification pass. What production alphas actually look like (the alpha-pool architecture and operators), the full Barra-style risk-model construction, Gârleanu–Pedersen dynamic trading (the production optimizer), the surviving factor library with construction math (revisions, SUE, short interest, BAB, quality, issuance), the production ML-combiner spec, Kalman filtering where it's actually used, impact-model estimation from own fills and the POV tradeoff, queue value, ETF/ADR parity math, the vol-desk production stack (variance-swap replication, term-structure carry, dispersion), and statistical governance tools (block bootstrap, SPA, empirical-Bayes alpha grading, CUSUM decay alarms). All from-training; every family tagged with data requirements and desk-usability.
tags: [systematic-trading, ml-stats, derivatives, model, microstructure]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: []
---

# The Production Model Book (Vol. 2)

> **Learning this material for the first time? Read the
> [plain-language version](production-model-book-plain.md) first** — same content, every
> prerequisite explained, worked examples. This page is the dense reference card.

> Continuation of the [alpha model book](alpha-model-book.md) after its verification pass: the
> teaching tier (VPIN, raw Kelly as policy, Hamilton-as-gate, Black–Litterman-for-pods) is
> **discarded**; this volume goes deeper on the confirmed production track and adds the families
> Vol. 1 didn't cover. ⚠️ All from-training. The recurring production pattern to hold in mind:
> **unimpressive formulas, industrialized** — the sophistication lives in the risk model, the
> combiner, the optimizer, the execution, and the monitoring, not in any single signal.

---

## 1. What production alphas actually look like — the alpha-pool architecture

The closest public artifact to a real pod's alpha library is Kakushadze's *"101 Formulaic
Alphas"* (2015, WorldQuant-style expressions, most in live-type use at the time). Three real
examples, verbatim in their operator language:

```
alpha#101 = (close − open) / ((high − low) + 0.001)
alpha#12  = sign(Δvolume) · (−Δclose)
alpha#6   = −corr(open, volume, 10)
```

Each is individually feeble (rank IC ~0.005–0.02, half-life days). Production is the
**industrialization around hundreds of these**:

**The operator algebra** (the actual production vocabulary): `rank(x)` — cross-sectional rank to
[0,1] (kills outliers and scale); `zscore(x)`; `ts_rank(x, d)`, `ts_mean`, `ts_std`, `delta(x, d)`
— time-series operators; `decay_linear(x, d)` — weighted moving average with weights d, d−1, …, 1
(turnover control *inside* the alpha); `indneutralize(x, group)` — subtract industry/sector
means; `scale(x)` — normalize to unit gross; `truncate(x, p)` — cap weights. An "alpha" in
production is a short expression in this algebra, applied to point-in-time panels.

**Pool combination.** Each alpha's daily return stream is computed standalone (after
neutralization and cost estimate), then combined:

```
w = argmax  w'μ_IC − λ·w'Σ_IC·w − κ·turnover(w)
```

— mean-variance over the *alphas* (Qian–Hua from Vol. 1) or, at scale, an elastic-net regression
of forward residual returns on the alpha panel (the L1 term performs alpha selection; the
correlation penalty stops rediscovery double-counting). New alphas enter the pool only if their
**residual** (after regression on the existing pool) carries IC — the orthogonality bar,
industrialized.

**Lifecycle:** each alpha carries birth date, trial-count provenance, live-IC control chart, and
a retirement rule. Pods run **50–500 concurrently**; the book's edge is the pool, and no single
expression matters. **[data: daily+ PIT panels · desk-usable: YES — this architecture at ~10–30
alphas scale is exactly what the v3 registry + IC harness becomes]**

---

## 2. The Barra-style risk model — the actual construction

Vol. 1 named it; here is the production recipe (the USE4/GEM-class methodology):

1. **Cross-sectional regression each day** of returns on country + industry + style exposures:
   `r = X·f + ε`, WLS with √mktcap weights, and the constraint `Σ_ind (capweight_ind)·f_ind = 0`
   to break the country/industry collinearity. Styles (momentum, size, value, vol, liquidity,
   growth, leverage) are z-scored, winsorized exposures.
2. **Factor covariance:** EWMA with *different half-lives for correlation (~90–180d) and
   volatility (~45–90d)*; **Newey–West adjustment** for serial correlation of factor returns;
   **eigenfactor adjustment** (Menchero) inflating the small eigenvalues that sample covariance
   systematically underestimates — this is the fix for "optimized portfolios load on the risk
   model's blind spots."
3. **Specific risk:** time-series estimate per name, Bayesian-shrunk toward a structural model
   (specific vol regressed on size/industry/vol characteristics) — names with short history get
   the structural prior.
4. **Validation by bias statistic:** for any test portfolio, `B = std(r_t / σ_forecast,t)`
   should ≈ 1; B > 1 means under-forecast risk. Run over rolling windows across many random
   portfolios — this is how risk models are actually graded.

Production point most retail misses: **the optimizer only ever sees the risk model, so risk-model
error becomes position error at full force.** That's why shops pay MSCI/Axioma eight figures.
**[data: fundamentals + returns · desk: the 4-factor mini version from the solution sheet is the
honest solo copy; add the bias-statistic test — it's free]**

---

## 3. Gârleanu–Pedersen dynamic trading — the production optimizer result

The most production-relevant portfolio math of the last 15 years (AQR lineage). With
mean-reverting alpha signals and quadratic transaction costs (`Λ ∝ Σ` is the tractable case),
the optimal policy has a closed form with two famous principles:

```
x_t = x_{t−1} + τ·(aim_t − x_{t−1}),         0 < τ < 1
aim_t = weighted average of E_t[Markowitz portfolios, now and future]
```

1. **Trade partially** toward the target — the trading rate τ falls with transaction costs and
   rises with risk aversion; you never jump to the Markowitz portfolio.
2. **Aim in front of the target** — the aim portfolio overweights **slow-decaying signals**
   relative to their current Markowitz weight (a fast signal isn't worth paying costs to chase;
   by the time you've traded, it's gone). Signals are weighted by their half-life *relative to
   your trading speed*.

This one result explains half of production portfolio behavior: turnover bands, why value
(slow) gets structurally bigger weight than short-term reversal (fast) at the same IC, and why
"the optimizer decides the trades." **[desk: YES — the no-trade band + weekly cadence in the
solution sheet is the poor-man's τ; when H2/H3 coexist, weight them by half-life per this logic]**

---

## 4. The surviving cross-sectional factor library (construction math + status)

The factors that still run in production books, with their actual constructions:

- **Analyst revision momentum** (one of the strongest production families historically):
  `REV_i = Δ(consensus FY1 EPS)_{1–3mo} / |price|` (or scaled by estimate dispersion), z-scored,
  sector-neutralized. Often traded as *estimate diffusion*: (#up − #down)/#total. Decayed from
  its 2000s peak but alive; needs IBES-class data (**paid** — the desk's gap).
- **SUE / PEAD, production form:** `SUE = (EPS − E[EPS]) / σ(surprise)` with E[EPS] from
  consensus (not seasonal random walk); drift traded 1–60 days *in the illiquid half of the
  universe*, earnings-window risk-managed. US large-cap version is dead (Vol.-1 verdict stands);
  the production residue is small/mid + international.
- **Short interest / utilization:** days-to-cover `= SI/ADV`; **utilization** and **borrow fee**
  from securities-lending data (Markit-class, paid). High-fee ("special") names reliably
  underperform *net of the fee earned by lenders* — one of the cleanest documented alphas;
  inaccessible without the data and the short leg, but its *long-side mirror* (avoid crowded
  shorts' squeezes / avoid high-utilization longs) is free via the alpha-map lane-1 screens.
- **Betting-against-beta (Frazzini–Pedersen):**
  `BAB = (1/β_L)·(r_L − r_f) − (1/β_H)·(r_H − r_f)` — rank by shrunk beta, leverage the low-beta
  leg, de-lever the high-beta leg. Payer: leverage-constrained investors overpaying for
  high-beta. Run in production at AQR-class scale; long-only copy = low-vol tilt.
- **Quality — gross profitability (Novy-Marx):** `GP/A = (revenue − COGS)/assets`, z-scored
  within sector; the accounting line least gameable. Pairs naturally with value.
- **Accruals (Sloan):** `(ΔWC − Dep)/assets` — high accruals → negative alpha (earnings quality
  mean-reverts). Decayed but still in production quality composites.
- **Net issuance/buybacks:** 12-month change in split-adjusted shares outstanding; issuers
  underperform repurchasers (management market-timing is real). Free from filings; slow;
  long-only friendly.
- **Industry & linked-firm momentum (Moskowitz–Grinblatt; Cohen–Frazzini):** industry-level
  momentum leads constituents; customer momentum leads suppliers ~1 month (the attention-lag
  payer). The desk's lane 4 is this family with a timezone twist.
- **Seasonality (Heston–Sadka):** same-calendar-month historical return rank predicts this
  month's cross-section — mechanical, weak, real; production shops keep it as one pool member.

**[desk: issuance/quality/industry-momentum are free-data implementable; revisions/short-interest
are the two named paid-data gaps — matching the present-state stack's gated-feeds list]**

---

## 5. The production ML combiner — the exact spec that separates it from retail

Not "ML finds alpha": ML **combines** features into a return forecast under governance.
Production spec:

- **Features:** the §1/§4 panel, each transformed to cross-sectional ranks or z-scores per day
  (stationarity by construction), winsorized, lagged correctly (PIT).
- **Target:** k-day forward **residual** return (vs. the risk model) — never raw return, or the
  model learns beta and sector bets.
- **Model:** gradient-boosted trees (LightGBM-class) or ridge/elastic net; depth ≤ 3–6, heavy
  min-samples, monotonic constraints where the mechanism demands them.
- **Validation: purged, embargoed, walk-forward CV** (López de Prado): drop training samples
  whose label windows overlap validation; embargo ~k days after each fold; expanding-window
  refits on a fixed calendar (monthly/quarterly), never on performance triggers.
- **Ensembling:** across seeds, folds, and lookback windows; the forecast is the average —
  variance reduction is worth more than any single model's fit.
- **Honest ceiling:** Gu–Kelly–Xiu-class results — monthly cross-sectional OOS R² of a *fraction
  of a percent*, ~doubling linear models. That's what winning looks like: tiny R², monetized by
  breadth and the optimizer.
- **Monitoring:** live-IC control charts per feature-cluster and for the composite (§8).

**[desk: the v3 exclusion stands — ≥5 registered linear alphas first, then this spec verbatim]**

---

## 6. Kalman filters where production actually uses them

Not regime detection — **time-varying parameter tracking**:

- **Dynamic beta:** state `β_t = β_{t−1} + w_t` (random walk), observation
  `r_t = α + β_t·r_m,t + ε_t`. The filter's gain automatically balances responsiveness vs. noise
  — strictly better than rolling-window OLS for hedging books, at three lines of code.
- **Dynamic pairs hedge ratio:** same state-space with `P1_t = γ_t·P2_t + μ_t + ε`; the filter
  re-estimates γ continuously — the production upgrade of static Engle–Granger, standard in
  systematic RV.
- **Mixed-frequency nowcasting (macro pods):** dynamic factor model `y_t = Λ·f_t + ε`,
  `f_t = A·f_{t−1} + u` with missing/mixed-frequency observations handled natively by the
  filter; the NY-Fed-style GDP nowcast machinery, run privately at macro funds.

**[desk: YES on all three — dynamic beta belongs in the v3 feature layer; the DFM is the
rigorous skeleton for a Korea-exports/semis-cycle nowcast someday]**

---

## 7. Execution production math — beyond Vol. 1's skeletons

- **Impact model estimated from your own fills** (the TCA ledger's destination):

```
shortfall_i = a·σ_i·(Q_i/ADV_i)^b + ½·spread_i + ε_i     # fit (a, b) by NLS; b ≈ 0.5–0.7
```

  Every serious shop maintains this regression on its *own* executions; broker-provided impact
  curves are marketing until reproduced in your fills.
- **The participation-rate tradeoff:** with alpha decaying at rate φ and impact convex in
  participation ρ, the optimal ρ* solves `marginal impact cost(ρ) = marginal alpha lost to
  decay(ρ)` — fast-decaying signals *justify* paying more impact; slow signals never do. This is
  Gârleanu–Pedersen's τ reappearing at the child-order level.
- **Queue value (the MM/limit-order decision):**

```
V_queue = P(fill | queue position, depletion rates) · [½spread + E(α | fill)] 
E(α | fill) < 0   # adverse selection: you get filled when you're wrong
```

  with P(fill) from a birth–death model of the queue. Post the limit order iff V_queue > value
  of crossing now. Production MMs solve this per-venue per-tick; the desk's residue is the rule
  it already has — default to limits/auctions, cross only with urgency.
- **ETF/ADR parity (the arb-desk bread and butter, and this week's SKH listing):**

```
ADR fair = local price × FX / ratio        ETF basis = price − intraday NAV (iNAV)
futures fair = S·e^{(r−q)(T−t)}
```

  Deviations beyond costs are the HFT arb tier's income (not accessible), but the *monitor* is
  free and directly useful: the SKH ADR–Seoul basis is a live read on which market is setting
  the price overnight — file under lane 4's instrumentation.

---

## 8. Vol-desk production stack (the confirmed-real subset, deepened)

- **Variance-swap replication (the log contract):**

```
K_var = (2·e^{rT}/T) · [ ∫₀^F P(K)/K² dK + ∫_F^∞ C(K)/K² dK ]
```

  — model-free variance from the full strike strip; the VIX is this integral discretized. This
  formula is production three ways: pricing variance swaps, defining the VRP trade, and building
  IV indices on any underlier with a liquid chain.
- **VIX term-structure carry:** roll-down on VIX futures — signal = slope
  `(F1 − VIX)/days` or F2/F1; short vol futures in steep contango, flat/long in backwardation.
  Simple, crowded, real; blow-up risk = the 2018 XIV lesson (the wiki already owns it).
- **Dispersion (implied correlation):**

```
ρ_imp = (σ_I² − Σ w_i²σ_i²) / ( (Σ w_iσ_i)² − Σ w_i²σ_i² )
```

  Sell index vol / buy single-name vol when ρ_imp is rich vs. realized correlation (index
  options are structurally bid by hedgers — the Premium payer, again). Capital- and
  ops-intensive: vol-fund tier.
- **Dupire local vol (dealer calibration, one line of it):** in total-variance form
  `σ_loc²(k,T) = ∂_T w / [1 − (k/w)·∂_k w + ¼(−¼ − 1/w + k²/w²)(∂_k w)² + ½·∂²_kk w]` — the
  deterministic surface consistent with all vanilla prices; SLV (local-vol × stochastic-vol with
  a calibrated leverage function) is what exotics desks actually hedge with. Included for
  completeness of "what runs"; far beyond this desk's needs.

---

## 9. Statistical governance — the production tools around everything above

- **Stationary block bootstrap** for Sharpe confidence intervals (blocks preserve
  autocorrelation; i.i.d. bootstrap flatters you).
- **White's Reality Check / Hansen's SPA test:** bootstrap the *maximum* performance across the
  whole strategy universe tried → p-value for "the best one beats benchmark by luck." The
  frequentist cousin of DSR; production shops run one of the two on any promotion decision.
- **Empirical-Bayes alpha grading:** across a pool of alphas, shrink each estimated IC toward
  the pool mean with reliability weight `Var_true/(Var_true + Var_noise)` — new alphas with
  short histories get graded mostly by the prior; this is the mathematically honest form of
  "don't trust your new backtest."
- **CUSUM decay alarms on live IC:** `S_t = max(0, S_{t−1} + (IC̄_ref − IC_t − slack))`, alarm at
  threshold h → the retirement-contract trigger from the solution sheet, in control-chart form.

---

## 10. The desk map (Vol. 2 additions only)

| family | data needed | desk verdict |
|---|---|---|
| alpha-pool architecture + operators | daily PIT panel | **build** — this is v3's registry, matured |
| Barra construction + bias stat | fundamentals | mini-version now; bias stat immediately |
| Gârleanu–Pedersen τ/aim | none (logic) | **adopt** — half-life-weighted signal blending |
| revisions / short-interest factors | IBES / Markit (paid) | the two named paid gaps; long-side mirrors partial |
| issuance / quality / industry-momentum | filings + prices (free) | **implementable now** |
| production ML combiner | ≥5 linear alphas first | later, spec frozen above |
| Kalman dynamic beta / hedge ratio | prices | **yes, immediately** |
| impact NLS from own fills | the TCA ledger | yes — it's the ledger's purpose |
| ADR/ETF parity monitor | SKH ADR + Seoul prices | **this week** (lane-4 instrumentation) |
| var-swap strip / dispersion / SLV | options chains, capital | read-only (S2′ archive feeds the read) |
| bootstrap / SPA / EB grading / CUSUM | none | **add to harness** — all cheap |

## Verification note 2 (2026-07-08) — "real alpha, or fancy outdated models?"

Second user challenge, and it exposes a category error worth fixing permanently: **models don't
have alpha; situations do** (a payer plus a barrier). Models are extraction technology. With that
lens, the catalog splits three ways:

**A. Infrastructure — never had alpha, cannot be outdated in the alpha sense.** The Barra
construction, Gârleanu–Pedersen, the operator algebra, the ML combiner, Kalman tracking, impact
models, TCA, bootstrap/SPA/CUSUM governance. These decide **how much of any alpha you keep** —
they are current best practice and alpha-free by design. Roughly 70% of Vol. 2 is this. Calling
them outdated is like calling double-entry bookkeeping outdated: the profit isn't in the ledger,
but you don't run a business without one.

**B. Alpha-bearing families — real but decayed, graded honestly (⚠️ from-training):**
- **The decay base rates first:** McLean–Pontiff measure anomaly returns falling roughly a
  quarter to a third out-of-sample and **more than half post-publication**; Hou–Xue–Zhang find
  the *majority* of the published factor zoo fails careful replication (microcaps and
  equal-weighting did the original heavy lifting). Anything in a book is at best a diminished
  edge, at worst a data artifact. This is the prior every row below starts from.
- **Still real, with conditions:** the **variance risk premium** (structural insurance demand —
  but the payoff is short-tail; XIV is the tombstone of harvesting it carelessly);
  **short-interest/utilization** (among the most robust documented cross-sectional signals — but
  needs paid lending data and mostly the short side); **TSMOM/CTA** (a dead-flat 2011–19 decade,
  a spectacular 2022 — the alpha is regime-lumpy and half the point is crisis convexity, which is
  why allocators still pay for it); **low-vol/BAB** (a real leverage-constraint premium, with
  crowding episodes); **quality & net issuance** (small, slow, persistent — survive because
  they're boring); **linked-firm/attention lags** (arbitraged in US large caps, alive where
  attention is genuinely scarce — cross-border, cross-language, small caps: the lane-4 thesis);
  **short-horizon reversal/stat-arb** (the *effect* persists because liquidity provision must be
  paid, but the easily-harvested layer is gone — pods extract it with ensembles, risk models, and
  execution quality, i.e., with category-A machinery).
- **Mostly dead as published:** PEAD in liquid US large caps, classic pairs on arbitrary stocks,
  12-1 momentum as an easy standalone (still real as a factor, no longer free money), calendar
  effects, the long tail of the 400-factor zoo.
- **Real but structurally inaccessible:** everything at the OFI/queue/microstructure tier — the
  alpha is genuinely there and genuinely harvested, by co-located infrastructure. For this desk
  it is sensing vocabulary, not income.

**C. The conclusion the split forces.** In 2026, published-model alpha is a *commodity input*;
the surviving edges live where a **barrier** still stands: data others don't process
(the Korea cohort-flow lane), markets and horizons others can't occupy (capacity floors,
retail-heavy microstructure, the KST clock), execution cost floors, and speed. That is exactly
why the [alpha map](../../synthesis/alpha-map.md) ranks lanes by barrier rather than by model
sophistication, and why the pod business model is not "own a great model" but "run a pipeline
that finds, sizes, monitors, and retires hundreds of small effects continuously" — **the
half-life is the business model.** The books (Vols. 1–2) are the tooling; the lanes are the alpha
claims; the IC harness is the arbiter; and no model on these pages should be traded on its
published parameters.

## Verification note 3 (2026-07-08) — first-principles re-derivation, on challenge

Third user challenge: "are you sure? verify from first principles." Re-derived rather than
re-cited. The core survives; **three walk-backs recorded.**

**The derivation chain (what first principles actually supports):**
1. **Sharpe's arithmetic:** before costs, the average active dollar earns the market; after
   costs, less. So gross alpha for one participant requires a counterparty losing it — alpha
   needs a **payer**. (Nothing new; the wiki's foundation.)
2. **Grossman–Stiglitz:** inefficiency persists in proportion to the cost of exploiting it.
   Post-publication, a strategy's exploitation cost = the cost of its **scarce inputs** (data,
   speed, capacity, risk-bearing, rare skill). Therefore: **after publication, a strategy's
   returns are rents on its scarce inputs, not returns to the knowledge itself.** A published
   model implemented with commodity inputs earns ~zero economic profit — perfect competition
   among implementers. This *derives* verification-note-2's "commodity input" claim instead of
   asserting it.
3. **Adaptive markets (Lo):** capital learns; every exploited situation decays. Steady-state
   firm profit = (flow of new situations found) × (average lifetime value) − research cost —
   i.e., the pipeline, not any edge, is the asset. "The half-life is the business model"
   survives derivation.
4. **Infrastructure:** net alpha = gross alpha × keep-rate − costs. Risk models, optimizers,
   TCA, governance move the **keep-rate**; they generate no gross alpha (no payer on the other
   side of a covariance matrix). Boundary case honestly noted: at the liquidity-provision tier,
   execution infrastructure *becomes* the gross source (you become the paid immediacy seller) —
   the infrastructure/alpha boundary is fuzzy exactly there, nowhere else.

**Walk-back 1 — "models don't have alpha" was too absolute.** A model can *be* the barrier
while it is rare and hard: early RenTec/D.E. Shaw extracted alpha from *public price data*
because statistical extraction skill was itself scarce (G–S: skill-while-rare is a scarce
input earning rents). The operative truth for these pages is narrower and stronger: **a
published model is never the barrier** — everything in Vols. 1–2 is published, so nothing here
carries alpha in itself. That's the claim that survives; the aphorism overshot.

**Walk-back 2 — I presented a contested literature as settled.** McLean–Pontiff's decay
estimates (~26% out-of-sample, ~58% post-publication) are the clean causal evidence and stand.
But the *replication-failure* rate is genuinely disputed: Hou–Xue–Zhang find the majority of
the zoo fails careful replication; Chen–Zimmermann replicate nearly all of a
differently-constructed set; Jensen–Kelly–Pedersen (Bayesian) argue most factors replicate and
decay less than claimed. Construction choices and priors drive the spread. The direction
(published ⇒ diminished) survives every camp; the "majority fails" line was one side of an
open fight. ⚠️ All from training.

**Walk-back 3 — the Korea "data moat" has been oversold in this thread, including by me.**
First-principles check: KRX investor-type flows are **public data**. Data-access is therefore
*not* the barrier — domestic Korean quant desks, prop shops, and a large Korean academic
literature actively use this data. What actually protects lane 1: **capacity floors** (the
per-name flush/LETF trades are too small for institutional size), **attention/integration**
(KST-native, fused with a discretionary sector book — scarce among *English-language systematic*
operators, which is the honest version of "underexploited"), and breadth of competing local
users being capacity-constrained themselves. Lane 1's prior stays high, **but for corrected
reasons: it is a capacity-and-attention rent on public data, not an exclusivity rent.** The
[alpha map](../../synthesis/alpha-map.md) carries a matching correction.

**Net verdict after re-derivation:** verification note 2's conclusions stand with sharper
foundations — published models = extraction technology whose returns accrue to scarce inputs;
infrastructure = keep-rate; decay = the business model. The desk's honest scarce inputs are:
smallness (capacity rent), the KST/Korean integration (attention rent), zero-cost operation
(G–S: a lower exploitation-cost floor), and discipline. Not: secret data, and not any model on
these pages.

## Relationships

- Vol. 1 (foundations + verification grades): [Alpha Model Book](alpha-model-book.md)
- Where the alphas plug in: [Alpha Map](../../synthesis/alpha-map.md) · [Engine v3](../../synthesis/engine-v3/index.md)
- Governance these tools extend: [Solution Sheet](../../synthesis/institution-grade-solution-sheet.md) · [Backtesting & Overfitting](../../ml-stats/concepts/backtesting-overfitting.md)
- The industry frame: [Algorithmic-Trading Landscape](../concepts/algorithmic-trading-landscape.md) · [Who Pays You](../../shared/concepts/who-pays-you.md)
