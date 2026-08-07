---
type: overview
title: The Institution-Grade Solution Sheet — Every Layer, Down to Formulas and Constants
description: Technical companion to the institution-grade overview — the buildable spec per layer. Data schemas and quality-gate thresholds, the IC/DSR evaluation math, concrete H1/H2/H3 signal specs with defaults, the portfolio-construction pipeline with constants, the numeric risk rulebook, the TCA ledger with shortfall decomposition, decay/retirement rules, ops (heartbeats, dead-man switch, degraded mode), and monthly governance. Every constant is a pre-registered default, changeable only via protocol.
tags: [systematic-trading, ml-stats, engineering, process, small-account]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: []
---

# The Institution-Grade Solution Sheet

> Technical companion to [Institution-Grade, Profitable](institution-grade-quant-system.md) (the
> why and the failure taxonomy) and to the [engine-v3 project outline](engine-v3/project-outline.md)
> (repo tree, nightly DAG, PROTOCOL v3.0, week-by-week plan). This page is the third level of
> zoom: **formulas, schemas, thresholds, and pseudocode** per layer. Where the outline names a
> module, this sheet specifies what runs inside it. Nothing here contradicts the outline; where a
> default is new, it is marked **[default — pre-registered, change only via protocol]**.
>
> Honesty header: the constants below are *defensible defaults from practitioner convention*, not
> optimized truths. The whole point of the harness is that they get revised by registered
> evidence, never by in-the-moment judgment.

---

## Layer 1 — Data: the PIT lake

### 1.1 Storage schemas (parquet)

**`bars/`** — partitioned by date, one row per (symbol, date):

| column | type | note |
|---|---|---|
| symbol, date | str, date | primary key |
| open, high, low, close | float | **raw, unadjusted** |
| volume | int | shares |
| source | str | `yfinance` / `stooq` / `alpaca` |
| ingested_at | timestamp UTC | write-once |

**`adjustments.parquet`** — (symbol, ex_date, split_ratio, div_cash). Adjusted prices are a
**view computed at read time** from raw bars × cumulative factors — never overwrite history.
This is the restatement defense: when a vendor back-adjusts (yfinance does, silently), your
stored raw series doesn't move, and a factor diff is detectable.

**`universe.parquet`** — (symbol, added_date, removed_date, removal_reason ∈ {delisted, acquired,
liquidity_fail, manual}). Membership queries are always as-of: `added ≤ t < removed`.
**Delisting return rule [default]:** if a terminal print is missing, book −30% on the delisting
day for involuntary delistings (the Shumway convention), acquisition price for M&A.

**`krx_flows.parquet`** — (date, symbol, investor_type, net_value_krw, net_volume), investor_type
∈ {foreign, institution_total, pension, invest_trust, insurance, private_fund, bank, other_corp,
retail}. Already half-built as the engine's S-fetchers; this is the desk's structural data edge.

**Vendor snapshots:** every raw API response zipped to `raw_vendor/YYYY-MM-DD/` append-only. You
cannot re-download the past; the archive is what makes future audits possible.

### 1.2 Universe rules [defaults]

ADV(63d) > $50M · price > $5 · listed ≥ 1yr · optionable (liquidity proxy). Re-screen monthly,
**decisions never backdated** (the outline's forward-clean rule). v1 ≈ S&P-100 ∪ Nasdaq-100 ∪
~20 ETFs ∪ semis complex (~170 names) → ~300 later.

### 1.3 Quality gates (fail-loud, block-on-fail)

| gate | threshold [default] | on fail |
|---|---|---|
| row count vs universe | within ±2% of expected | halt run, alert |
| calendar alignment | matches XNYS trading calendar | halt |
| NaN per name | forward-fill ≤ 2 days, else | quarantine name, flag report |
| return outlier | \|1d return\| > 40% | cross-check 2nd source; mismatch → quarantine |
| stale price | 5 identical closes with volume > 0 | quarantine name |
| zero volume | on a liquid name | flag |
| split sanity | price gap ≈ split ratio ±5% | halt (bad adjustment) |

Gate results append to `data_quality.jsonl` (date, gate, pass/fail, detail). **Degraded-mode
policy:** any halt → the report still publishes with a red DEGRADED banner, **new signals are
blocked, yesterday's targets carry over** — never trade on data that failed a gate. Vendor outage
→ stale mode ≤ 2 days, then full halt.

---

## Layer 2 — Research: the evaluation math

### 2.1 Residualization (what "alpha" is measured against)

Per day t, cross-sectional regression over the universe:

```
r_i = α + β1·beta_i + β2·ln(mktcap_i) + β3·mom12-1_i + Σ_s γ_s·sector_is + ε_i
```

- `beta_i`: 252d OLS vs SPY, shrunk `β* = 0.67·β̂ + 0.33·1` (Blume/Vasicek — raw betas overfit).
- WLS weights √mktcap [default]; sector = GICS level-1 dummies.
- **The residual ε_i is the alpha target.** Signals predict ε, not r — otherwise every "signal"
  is disguised beta (failure mode #1's quiet cousin).

### 2.2 The IC framework

- **Daily rank IC:** `IC_t = SpearmanCorr(score_{i,t}, Σ_{d=1..k} ε_{i,t+d})` for horizons
  k ∈ {1, 2, 3, 5, 10, 21}.
- **Significance:** `t = mean(IC) / (std(IC)/√T)`; for k > 1 the ICs overlap, so use
  **Newey–West with k−1 lags** (or sample every k-th day) — skipping this overstates t by ~√k.
- **Decay curve:** plot mean IC vs k. The natural holding period is where cumulative IC per unit
  of implied turnover peaks; H2 is expected to decay within ~5 days, H3 to persist for months.
- **Quantile portfolios:** deciles (quintiles if N < 100), equal-weight, rebalanced at the
  signal's cadence. Report Q_top−Q_bottom annualized **net of the cost model**, and
  **monotonicity** = Spearman(decile index, decile mean return) with ≥ 0.8 as the pass bar
  [default] — a spread driven only by the tails is a fragile spread.
- **Turnover → cost hurdle:** one-sided turnover `τ = ½·Σ_i |w_{i,t} − w_{i,t−1}|` per rebalance.
  Annual cost drag = τ × rebalances/yr × 2 × cost_per_side. **Pass bar: the Q-spread survives at
  2× the modeled cost** [default, inherited from v2's fee-ladder practice].
- **Effective breadth honesty:** IR ≈ IC·√BR, but BR is *independent* bets — correlated names and
  autocorrelated signals shrink it. Report effective breadth alongside nominal (a 200-name daily
  signal with 0.9 day-over-day autocorrelation is not 200 × 252 bets; it is closer to
  200-adjusted × 252·(1−ρ)/(1+ρ)).

### 2.3 Multiple-testing control

- **Registry accounting:** N trials = every `experiments.jsonl` row **plus the imported v2
  counts** for overlapping families (~150 EV-lab + 163-config sweep + ~40 ledger rows). Nothing
  is free: exploration notebooks that influenced a hypothesis count as trials for that family.
- **Deflated Sharpe (Bailey–López de Prado 2014):** compute the expected maximum Sharpe of N
  random trials, `SR₀ ≈ √V[SR̂] · [(1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e))]` (γ ≈ 0.5772), then
  `DSR = Φ( (SR̂ − SR₀)·√(T−1) / √(1 − skew·SR̂ + (kurt−1)/4·SR̂²) )`. **Ship bar: DSR ≥ 0.95**
  (v2's threshold, carried).
- **Walk-forward with purge + embargo:** expanding window; k-day labels → purge the k overlapping
  days at every split boundary and embargo 5 further days [default] so training never sees
  information that leaks into validation (López de Prado's purged CV).
- **Sealed holdout:** 2026-06-01 → forward, one shot, per PROTOCOL v3.0 — and the forward paper
  record is the living out-of-sample.
- **Orthogonality bar for new signals:** regress candidate scores on the current champion's
  scores cross-sectionally; the **residual** must carry IC on its own. Correlated rediscoveries
  of the same effect don't add breadth, they add false confidence.

### 2.4 Signal specs (concrete defaults — registered, then frozen)

**H1 — regime/vol overlay (gates everything):**
```
trend  = 1.0 if SPY_close > SMA200(SPY) else 0.5      # [default: 0.5 floor, not 0 — long-only
vol    = min(1.0, σ_target / σ_realized)              #  system keeps a foot in; pre-registered]
σ_realized = EWMA(λ=0.94) of daily portfolio returns, 63d window, annualized
exposure E = trend × vol, flips require 2 consecutive days (hysteresis — whipsaw guard)
```

**H2 — cross-sectional short-term reversal (flagship):**
```
ε_{i,d}  = residual returns from §2.1
raw_i    = − Σ_{d=t−4..t} ε_{i,d}                     # 5-day cumulative residual, sign flipped
score_i  = zscore_xs(winsorize(raw_i, ±3σ))
exclusions: earnings window [t−1, t+1] if calendar available (else flag as caveat);
            hard-to-borrow / SI > 20% float names
hold ~3–5 days per the decay curve; trade only when H1 exposure > 0.5
expected per-name IC: 0.02–0.05 (the honest institutional range — breadth does the work)
```

**H3 — momentum ballast:** 12-1 month total return (skip the last month — it belongs to
reversal), top quintile equal-weight, rebalance monthly on the last trading day, trade next open.
Low turnover (~20–40%/month one-sided) is the point: it's ballast and a decorrelator, not a
sprint.

---

## Layer 3 — Portfolio construction (the pipeline, in order)

```
scores → winsorize(±3σ) → zscore_xs → neutralize(beta, size, sector)   # regression residual
       → long-only tilt: w̃_i = max(z_i, 0)
       → normalize: w_i = w̃_i / Σ w̃            # cash is the residual asset
       → caps: name ≤ 5%, sector ≤ 25%          # renormalize after capping
       → exposure scale: w_i × E (from H1), target book vol 12% ann [default]
       → no-trade band: skip |Δw_i| < 0.5%      # turnover control
       → integer shares at current prices; positions target N ≈ 20–40 names
```

**Why no optimizer [decision]:** at N ≤ 300 daily names, estimation error in the covariance
matrix swamps what a QP adds over "score-proportional with caps and bands"; if an optimizer is
ever introduced, it is `max α′w − λ·w′Σw − c·|Δw|` with **Ledoit–Wolf shrunk Σ**, λ solved to hit
the vol target — registered like any other change. The optimizer decides trades, so it lives
under protocol, not preference.

**Never levered:** exposure scalar capped at 1.0. The synthetic short is the regime gate, not
margin.

---

## Layer 4 — Execution & TCA

**Conventions (inherited verbatim from v2):** signal on close t → orders at open t+1; gap-through
stops honored in simulation; no order routing by code — tickets only. *(Amended 2026-07-07: the
tickets-only rule is now rung 0 of a promotion ladder — automated routing is specced in the
[execution-layer design](engine-v3/execution-layer.md) and unlocks only through its shadow →
paper → live-small gates.)*

**Live order policy [defaults]:** marketable limit at the open, cap = quote + 10 bps; opening
auction acceptable at this size; never chase after the first fill window — an unfilled ticket
books as opportunity cost, not a market order at 09:35.

**The TCA ledger** — `tca.csv`, five things measured, one row per ticket:

| column | meaning |
|---|---|
| ts_signal, symbol, side, qty | identity |
| decision_price | close at signal (what the backtest assumes it acts on) |
| arrival_price | next open (what the convention fills at) |
| fill_price, filled_qty, fees | reality |
| close_same_day | for opportunity cost on unfilled remainder |

**Shortfall decomposition (per ticket, in bps, sign = side):**
```
delay        = side · (arrival − decision) / decision
execution    = side · (fill − arrival)   / arrival        # spread + impact
opportunity  = side · (close − decision) / decision × unfilled_fraction
total        = delay + execution + opportunity
```
Monthly aggregation answers the only question that matters: **is the live-vs-paper gap the signal
decaying or the execution leaking?** Delay dominates → the next-open convention is the cost
(consider close-to-close simulation instead). Execution dominates → order type/venue problem.
Neither → look at the signal's live IC. The zero-fee window to Dec-31 makes this a clean
laboratory: fees are off, every residual bp is spread + timing. **Cost model recalibrates
quarterly from this ledger** — assumed 5 bps/side [default] until measured.

---

## Layer 5 — Risk: the numeric rulebook

All constants pre-registered; **changes require a registered proposal + 1-week cooling period and
are forbidden mid-drawdown** (the tripwire doctrine — rule edits under fire are breaches).

| rule | constant [default] | action |
|---|---|---|
| per-name cap | 5% | at construction |
| sector cap | 25% | at construction |
| gross exposure | ≤ 100%, cash = default asset | structural |
| book vol target | 12% annualized | exposure scalar |
| drawdown ladder (from HWM, paper & live tracked separately) | −5% / −10% / −15% | exposure ×0.75 / ×0.50 / flat + written post-mortem gate to restart |
| live sleeve unit risk | 1R = 1% NAV design risk per position | sizing |
| daily stop (live) | −2R day | 2-day stand-down |
| weekly stop (live) | −4R week | flat for the week |
| un-signaled trade | any | breach: flat by close + same-day post-mortem (the −$39.76 rule) |
| crowding screen | SI > 20% float or borrow fee > 5% | name excluded |
| correlation guard | avg pairwise 63d corr of book > 0.7 | treat book as one bet: exposure ×0.5 |
| stress replay | weekly auto-job: current weights through 2020-03, 2022, 2024-08-05, 2026-06/07 windows | alert if modeled worst 5-day < −8% |

**Decay management (the retirement contract):** every registered signal ships with a retirement
rule written at registration, e.g. *"rolling 126-day live/paper IC < 0 → weight 0 until
re-registered."* The decay panel on the nightly report shows each signal's rolling IC against its
own contract. Allocation follows current IC, not discovery-era IC. Nothing is defended out of
attachment; retirement is the system working.

**The second-human substitute, stated plainly:** solo, the researcher = risk manager = trader.
The structural replacements are (a) the adversarial fresh-eyes gate for research claims (kill is
final), (b) this mechanical rulebook for risk (fires without debate), and (c) adherence-% as a
first-class published metric — the human is inside the system boundary and gets measured like any
other component.

---

## Layer 6 — Ops: run unattended, fail loudly

- **Heartbeats:** every DAG step appends (run_date, step, status, duration_s, rows_out, error) to
  `ops/heartbeat.parquet`. The report renders the SLA table. **Silent-failure count** (a step that
  neither completed nor alerted) is a tracked metric whose only acceptable value is 0.
- **Dead-man switch:** the DAG's final step pings healthchecks.io; a *missing* ping triggers the
  external alert channel (Telegram) independently of the runner — the failure mode where the
  runner itself dies is the one your own alerting can't catch.
- **Idempotency:** all outputs run-date-keyed; writes are temp-file → atomic rename; re-running a
  night replaces cleanly. Ingest via per-ticker watermarks (the outline's rule).
- **Backups:** weekly lake archive to private storage; **restore drill quarterly** — an untested
  backup is a hope, not a backup. Runbook documents both.
- **Secrets:** GH-Actions repo secrets / gitignored `settings.local.yml`. Nothing sensitive in
  the public repo — public-engine/private-config split per the outline.
- **Degraded mode:** defined in §1.3 — publish with banner, block signals, carry targets.

---

## Layer 7 — Governance: the monthly review (first weekend, ~1h, written)

1. Green-run streak & silent-failure count (target: streak ≥ 15, silent = 0).
2. Adherence % on the live sleeve (bar: ≥ 95%; every breach has a post-mortem on file).
3. Live-vs-paper IC gap per signal + TCA decomposition (which leak is it?).
4. Decay panels vs each signal's retirement contract — retire what's due, no exceptions.
5. Cost model vs realized TCA (recalibrate quarterly).
6. Experiment ledger: N trials this month, DSR budget spent, verdicts count (bar: ≥ 2/month).
7. Breach log review + rulebook change proposals (cooling period starts now, not mid-month).
8. Denominator policy check: contributions on schedule; account grows by savings while the system
   earns trust.

---

## What this sheet deliberately does not cover

Repo scaffolding, CI config, and the week-by-week build order (the
[project outline](engine-v3/project-outline.md) owns those); Korean tax/compliance framing for
public signals (open decision there); and any promise about returns — the
[parent page](institution-grade-quant-system.md) prices "profitable" honestly: Sharpe 0.5–1.0
unlevered at this horizon, dollars scale with the denominator, and t ≈ SR·√years says the record
needs years — which is why the ops layer that keeps it running unattended *is* the alpha of this
whole sheet.

## Relationships

- Parent (why / failure taxonomy): [Institution-Grade, Profitable](institution-grade-quant-system.md)
- Sibling (repo/DAG/protocol/weeks): [Engine v3 project outline](engine-v3/project-outline.md) · [design brief](engine-v3/design-brief.md)
- The methods these specs implement: [Algorithmic-Trading Landscape](../systematic-trading/concepts/algorithmic-trading-landscape.md) (IC pipeline, residual reversal template)
- Measurement doctrine: [Performance Metrics](../ml-stats/concepts/performance-metrics.md) · [Backtesting & Overfitting](../ml-stats/concepts/backtesting-overfitting.md)
- Risk doctrine: [Risk of Ruin](../shared/concepts/risk-of-ruin.md) · [Kelly Criterion](../shared/concepts/kelly-criterion.md) · [Transaction Costs](../shared/concepts/transaction-costs.md)
- The culture the rulebook encodes: [Tripwire-Exit Execution](../systematic-trading/checklists/tripwire-exit-execution.md) · [Who Pays You](../shared/concepts/who-pays-you.md)
