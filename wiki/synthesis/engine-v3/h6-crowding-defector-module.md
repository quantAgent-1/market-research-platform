---
type: overview
title: Engine v3 — H6 Crowding & First-Defector Module (Production Build Plan)
description: The full production blueprint for the positioning-fragility module inside enginev3 — Signal A (crowding condition) + Signal B (defector trigger) + Signal C (overshoot-gated constraint exhaustion, the re-entry leg) → a tax-aware exposure overlay. Data contracts with PIT/bitemporal rules, exact A1–A14/B1–B8/O1–O3/C1–C5 definitions, the CROWD→DEFECT→CASCADE→EXHAUST state machine, episode-library falsification harness, ops hardening, phased build with exit gates, and pre-committed kill criteria.
resource: project-outline.md
tags: [systematic-trading, positioning, crowding, risk, market-microstructure, engineering, monitor]
timestamp: 2026-07-03T00:00:00Z
status: active
sources: []
---

# Engine v3 — H6 Crowding & First-Defector Module (Production Build Plan)

*Companion to the [Engine v3 project outline](project-outline.md) (which owns the repo
skeleton, PROTOCOL v3.0, and the nightly DAG). This page specifies one hypothesis family — **H6:
positioning fragility** — to production depth: every data contract, formula, threshold, gate, and
failure mode. A copy seeds `docs/H6-DESIGN.md` in the repo. Education, not investment advice.*

**Origin:** the June–July 2026 memory tape, where the manual version of this module already ran —
crowding ledger as condition, tripwires
+ breadth as triggers. The design case: a +22.5% EPS beat plus the dream raise moved MU's ATH close
by **+0.18%** (the ceiling event),
the euphoria marker (SK Hynix crowned #1 KOSPI market cap ~Jun-22) printed one day before the top,
and the complex then gave back 10–15% on zero earnings news, ordered exactly by crowdedness
(the liquidation signature).
**Second origin (Signal C, added 2026-07-03):** the July 1–3 cascade-and-V — SKH −25% in two
sessions on no estimate change, then the scheduled capitulation morning (반대매매 belt) turning at
~10:00 into a +5.37% buy-sidecar close — showed the module also needs the *exit of the exit*: a
quantified version of the intuition *"this is selling off more than the fundamental value revision;
it should bounce; roughly to here."* That is Signal C (§5b), gated by the overshoot meter (O1–O3).
Mechanics: [KRX session clocks & forced liquidation](../../shared/concepts/krx-session-clocks-and-forced-liquidation.md) ·
operational twin: [catching-the-V-day checklist](../../systematic-trading/checklists/catching-the-v-day-checklist.md).

---

## 0. Mission, scope, and the pre-registered KPI

- **What H6 is:** a daily-clock **risk-state machine**. Signal A measures *how crowded/fragile*
  positioning is (a condition — predicts asymmetry, never timing). Signal B detects *the first
  credible defectors* (a trigger — supplies timing, valid only inside an A-extreme). Output: a
  published state + an **exposure overlay** with tax-aware trim/re-add tickets.
- **What H6 is not:** a top-caller, a short-selling signal, or a standalone alpha stream. It never
  adds leverage, never shorts, never trades options (v3 guardrails inherited).
- **Primary KPI (pre-registered — decide success by this, nothing else):** on the overlaid book vs
  untouched buy-and-hold, **net of costs and KR tax**: (a) max-drawdown / ulcer-index reduction per
  episode, (b) upside forgone, (c) net Calmar improvement. Explicitly **not** a KPI: gross alpha,
  hit rate on "calling tops."
- **Named payer (PROTOCOL v3 registration requirement):** the late momentum chaser who buys the
  trim near the highs (Greater-Fool payer) and the forced de-grosser who sells the flush to the
  re-add (Constraint payer) — see [who pays you](../../shared/concepts/who-pays-you.md).
- **Honest base rate up front:** genuine consensus extremes ≈ dozens per decade, cross-correlated.
  This is a low-n, fat-tail family. It ships **dashboard-first** and earns exposure authority only
  through the gates in §10.

## 1. Architecture in one diagram

```
14 data feeds ──► A1–A14 component gauges ──► CROWD score 0–100 ──► state machine
                     (rolling percentiles          (coverage-weighted        NORMAL → ELEVATED → EXTREME
                      + 20d slopes)                 vote count)                    (hysteresis)
                                                                                      │
 8 event detectors ──► B1–B8 dated events ──► k-of-n FAMILY vote ──► DEFECT fires only in EXTREME
                                                                                      │
                                                              exposure overlay m ∈ {1.00, 0.85*, 0.60}
                                                              (* optional, default OFF — tax)
                                                                                      │
 overshoot meter O1–O3 ──► "fell more than revisions" gate ──► CASCADE (belt loaded, de-grossing live)
 5 exhaustion detectors ──► C1–C5 (2-of-5, O-gate open) ──► EXHAUST ──► staged re-entry (halves)
                                                              (weak close → belt reloads → stay CASCADE)
```

## 2. Repo delta (inside the v3 tree)

```
src/enginev3/
├── data/
│   ├── ingest_options_eod.py      # ORATS/DataShop EOD: IV30, IV-rank, 25Δ risk-reversal skew, P/C OI+vol, term slope
│   ├── ingest_krx_flows.py        # pykrx: investor-type net flows per name (foreign/inst/retail) + short-sale balance
│   ├── ingest_short_interest.py   # FINRA/Nasdaq bi-monthly SI; days-to-cover
│   ├── ingest_etf_flows.py        # shares-outstanding/AUM deltas; leveraged-ETF registry (SOXL, KR 2× singles)
│   ├── ingest_cot.py              # CFTC COT weekly (ES/NQ non-commercial net)
│   ├── ingest_estimates.py        # FMP/Finnhub: EPS estimates+revisions, ratings actions, targets, earnings surprises
│   ├── ingest_surveys.py          # AAII, NAAIM weekly
│   ├── ingest_kofia_credit.py     # S10: KOFIA 신용융자 daily balance (margin-fuel stock; free)
│   ├── ingest_krx_events.py       # S11: sidecar / circuit-breaker / VI event log (KRX notices)
│   └── positioning_registry.py    # per-source contract: schema hash, SLA, forward_clean_from, fallback, ToS note
├── features/
│   ├── crowding.py                # A1–A14 gauges → (percentile, slope) pairs
│   ├── defectors.py               # B1–B8 detectors (event objects with evidence payloads)
│   ├── overshoot.py               # O1–O3: revision-anchored gap, de-rating z, retracement anchor
│   └── exhaustion.py              # C1–C5 detectors + the belt-load meter (constraint ledger)
├── signals/
│   └── h6_fragility.py            # composite, state machine, DEFECT logic, overlay scalar, ticket builder
├── evaluation/
│   ├── episodes.py                # labeled episode library + schema
│   └── conditional.py             # conditional event-study metrics; block bootstrap BY EPISODE
├── report/                        # build.py gains a crowding panel + data-freshness table
config/crowding.yml                # complexes, params, thresholds, weights, hysteresis, k-of-n — all versioned
tests/{unit,integration,protocol}/h6_*   # incl. the chaos fixture (§9)
```

DAG placement (`ops/runner.py`): after step-2 ingest → **2b positioning-ingest** (parallel,
fail-soft per §9) → **3b crowding features + H6 state** → report/alerts. OHLCV stays fail-hard;
H6 sources never halt the run.

## 3. Data layer — contracts, PIT rules, budget

### 3.1 The bitemporal rule (the single most important detail)

Every H6 table carries **`effective_date` + `observed_at` + `source` + `ingest_run_id`**. All
feature computation and every backtest join on **`observed_at` ≤ decision time** — never on
effective date. This family's inputs publish with lags (SI ~days, COT 3 days, revisions dribble
in); ignoring that is how this module would silently lie. Sources whose history cannot be
reconstructed point-in-time (free estimate feeds, AUM scrapes, survey re-edits) are stamped
**`forward_clean_from: <go-live date>`** in `positioning_registry.py` and are **excluded from all
historical performance claims** — they accumulate evidence forward only (mirrors PROTOCOL v3's
forward-clean universe rule).

### 3.2 Source contracts

| # | Source | Fields | Cadence / pub-lag | PIT status | Failure fallback | Cost |
|---|---|---|---|---|---|---|
| S1 | OHLCV (v3 core: yfinance→Stooq) | prices, volume | daily / same-night | clean | fail-hard (halts run) | free |
| S2 | Options EOD — **ORATS or CBOE DataShop** | IV30, IV-rank, 25Δ RR skew, P/C OI & volume, 1m/3m term slope | daily / T+0 evening | buy 5y PIT history | component→stale | ~$30–100/mo + one-time history |
| S3 | KRX investor flows — pykrx | foreign/inst/retail net ₩ per name; short-sale balance | daily / T+0 ~18:00 KST (final) | reconstructable, clean | component→stale | free |
| S4 | Short interest — FINRA/Nasdaq | SI shares, % float, DTC | 2×/month / ~T+4bd after settlement | clean w/ observed_at | carry-forward ≤20 sessions | free |
| S5 | ETF flows/AUM — issuer + shares-outstanding | AUM, ΔSO, leveraged-ETF registry | daily / T+0–1 | forward-clean (scrape) | component→stale | free |
| S6 | CFTC COT | non-commercial net (ES/NQ) | weekly Fri / Tue data (3d lag) | clean w/ observed_at | carry-forward ≤10 sessions | free |
| S7 | Estimates/ratings — **FMP or Finnhub paid tier** | EPS estimates & 30/90d revisions, ratings actions, targets, standardized earnings surprise | daily / T+0–1 | **forward-clean** (true PIT = IBES-class, out of budget) | component→stale | ~$25–75/mo |
| S8 | Surveys — AAII, NAAIM | bull−bear, exposure index | weekly | forward-clean | carry-forward ≤10 sessions | free |
| S9 | VIX + term (CBOE) | VIX, VIX3M | daily | clean | component→stale | free |
| S10 | KOFIA margin credit — freesis | 신용융자 balance (total + KOSPI/KOSDAQ), daily Δ | daily / T+1 morning | reconstructable, clean (published series) | carry-forward ≤ 3 sessions | free |
| S11 | KRX trading-curb events | sidecar (buy/sell), CB, VI halts: timestamp + direction | event-driven / same day | reconstructable (public record) w/ observed_at | component→stale | free |

*(Signal C's cross-market confirm reuses S1: add the Taiwan reference tickers to the universe —
no new ingestor. The O-gauges reuse S7′ estimates + S1 prices — no new source, same forward-clean
caveats.)*

**Data-tier decision (2026-07-03): free-first, paid-at-authority.** Phases 1–3 (dashboard +
falsification — no money authority) run entirely on the free tier: **S2′** = a self-collected
forward archive of options metrics scraped nightly from free delayed sources (yfinance/CBOE chains
→ IV30, 25Δ RR skew, P/C OI computed in-house; no history; quality-flagged), and **S7′** =
yfinance analyst data + Finnhub free tier (ratings/targets/surprises; rate-limited;
lower-confidence marks). The **paid upgrade (≈ $60–170/mo: ORATS/DataShop + FMP/Finnhub paid) is
the Phase-4 entry gate** — subscriptions start the day the module first gets paper-money
authority, because that is when silent data corruption starts costing money. The standing warning
survives the tiering: free-scraped options/analyst data is the #1 silent-corruption risk, so
S2′/S7′ run under the same §9 drift-quarantine checks, and their components validate on forward
evidence only (they were forward-clean-stamped anyway). Optional: the ~$100–500 one-time
options-history purchase can be pulled forward to Phase 3 if episode-validation of the options
gauges is wanted before go-live.

### 3.3 Universe config (`config/crowding.yml`)

Complexes are first-class config objects, e.g. `memory: {us: [MU, WDC, SNDK], kr: [005930, 000660],
reference: [NVDA], xmarket_reference: [2330.TW, ^TWII], etfs: [SMH, SOXX], leveraged: [SOXL,
<KR 2× singles>]}` — the `reference` slot is the demand-side control for the NVDA-test ordering;
`xmarket_reference` is Signal C's cross-market confirm (for the KR memory complex: Taiwan/TSMC,
whose open is the 10:00-KST clock). Add SK Hynix ADR after its ~Jul-10 listing.
Market-level overlay uses the index complex (SPX/NDX + S8/S6/S9). Every complex re-selection is
logged (PIT-caveat rule inherited).

## 4. Signal A — component definitions (A1–A14)

Each gauge emits a **rolling percentile `p` (3y window, min 250 obs)** and a **20d slope `s`**.
All parameters below are **registered defaults — calibrate on the validation era, then freeze in
the ledger**; changing any = a new variant (~10-variant obituary cap inherited).

- **A1 — one-trade-ness:** PC1 variance share of the complex's 60d daily-return correlation
  matrix (min 5 members).
- **A2 — correlation regime:** mean pairwise ρ(20d) − mean pairwise ρ(120d).
- **A3 — dispersion collapse:** cross-sectional MAD of 20d returns across members, **inverted**.
- **A4 — IV-rank:** (IV30 − min₂₅₂)/(max₂₅₂ − min₂₅₂).
- **A5 — complacency skew:** 25Δput − 25Δcall IV, percentile **inverted** (flat skew at highs =
  nobody hedged; steepening later is B6's job).
- **A6 — put/call OI:** percentile **inverted** (thin puts = one-sided book).
- **A7 — leveraged fuel:** Σ(long leveraged-ETF AUM referencing the name or complex) ÷ 20d dollar
  ADV; plus its 20d change. (The June mechanism: KR 2× singles ≈ 14% of Samsung/SKH turnover.)
- **A8 — short-side thinness:** SI % float percentile **inverted**, DTC inverted (no shorts left =
  no squeeze fuel, no marginal covering bid under the market).
- **A9 — KR cohort crowding:** z of 20d cumulative foreign net-buy (₩, normalized by 60d ADV) +
  retail share-of-turnover percentile (retail-frenzy marker). KR names only.
- **A10 — futures spec positioning:** COT non-commercial net percentile (market overlay only).
- **A11 — analyst-consensus shape:** %Buy percentile + target dispersion (σ/μ) **inverted** + 90d
  net-revision breadth (the "wall of raises chasing price" marker — targets follow price).
- **A12 — survey extreme:** AAII bull−bear and NAAIM percentiles (market overlay only).
- **A13 — news-response decay (the ceiling gauge):** rolling event-study over the trailing 8
  quarters of complex earnings: response slope of CAR(0,1) vs standardized surprise, plus the
  most recent event's response z. A large positive surprise producing ≤ +0.25σ next-day move is
  the crowding tell measured (the MU +0.18% case).
- **A14 — extension:** (P − 200DMA)/σ₂₀ percentile + 12m-return cross-sectional rank.

**Composite.** Vote per component: `v=1` if `p ≥ 90` **and** `s > 0` (extreme *and intensifying* —
the quote's operative clause); `v=0.5` if `p ≥ 90` and `s ≤ 0`; else 0. **CROWD = 100 × Σwᵢvᵢ/Σwᵢ**
(weights default 1; coverage-weighted). **Minimum coverage 8/14 populated**, else state =
`INSUFFICIENT_DATA` (publish, never trigger, overlay frozen — fail-closed, §9).

**State machine with hysteresis:** NORMAL < 40 ≤ ELEVATED < 65 ≤ EXTREME; exit EXTREME below 55,
exit ELEVATED below 30 (no flapping); state changes require 2 consecutive sessions.

## 5. Signal B — defector detectors (B1–B8)

Each emits a dated event `{date, family, strength, evidence}` — evidence payloads go verbatim into
the report so a human can audit every fire.

- **B1 — ceiling event** *(family: event-response)*: standardized earnings surprise ≥ +1.0 and
  CAR(0,1) ≤ +0.25 × daily σ.
- **B2 — leader crack** *(price-structure)*: two-sided CUSUM on daily log-RS(most-crowded member ÷
  equal-weight complex): `S_t = max(0, S_{t−1} − r_t − k)`, fire at `S_t > h`; defaults k = 0.5σ_RS,
  h = 4σ_RS, calibrated to ≤ 2 false fires/yr on validation.
- **B3 — structure break** *(price-structure)*: first lower swing-high (5d fractal) after a ≥ 40d
  uptrend (price > 50DMA on ≥ 80% of days), **or** a failed breakout — close above the 60d high
  then back below it within 5 sessions on ≥ 1.2× ADV.
- **B4 — distribution count** *(price-structure)*: ≥ 5 distribution days (return ≤ −0.2% on higher
  volume) in 25 sessions, or ≥ 2 churn days (volume ≥ 1.5× ADV20, |return| < 0.3%, within 2% of the
  60d high) in 10 sessions.
- **B5 — flow-price divergence** *(flow)*: KR — 10d cumulative foreign-net z ≤ −1.5 while price ≥
  98% of its 60d high (distribution, measured). US proxy — complex-vs-SPX RS 5d z ≤ −1.5 while
  |SPX 5d return| < 1%.
- **B6 — hedging defection** *(options)*: Δ(25Δ skew, 10d) ≥ +1.5σ of its own history while spot's
  10d return > 0; or put-volume percentile ≥ 90 arriving from < 50 within 10 sessions.
- **B7 — statement defection** *(statements)*: first downgrade or ≥ 5% target cut after ≥ 60d
  containing zero cuts and ≥ 5 raises (the bold-deviator carries the information); optional
  Form-4 cluster: ≥ 3 distinct insiders selling within 10 sessions.
- **B8 — vol-structure turn** *(options)*: VIX 3m−1m slope percentile ≤ 10, or front>back
  inversion, arriving from > 50 within 10 sessions.

**DEFECT logic (k-of-n by *family*, not by event — price events double-count each other):**
families = {price-structure, flow, options, event-response, statements}. Fire when **≥ 3 distinct
families** produce events inside a rolling 10-session window **while state = EXTREME** (≥ 4
families if only ELEVATED). Then: 10-session cool-down; re-arm only after a fresh 20d high or a
state re-entry. Unconditioned B-events are logged but never fire — the false-positive control is
the conditioning, and the SNR reality
(~97% of a daily move is noise) is why every detector demands multi-day evidence.

## 5b. Signal C — overshoot meter & constraint exhaustion (O1–O3, C1–C5) *(added 2026-07-03)*

**The intuition this leg quantifies (its north star):** *"this is selling off more than the
fundamental value revision → it could bounce back → maybe to about here."* Every component below
is one clause of that sentence made measurable. The theory:
[temporary impact reverts, permanent impact doesn't](../../shared/concepts/liquidity-cascades-and-v-reversals.md);
the KR scheduling that concentrates the temporary component into mornings:
[KRX session clocks](../../shared/concepts/krx-session-clocks-and-forced-liquidation.md).

### The overshoot meter (O1–O3) — "more than the fundamental revision," measured

All three anchor price to the **estimate path** (S7′ NTM consensus EPS, complex =
coverage-weighted member aggregate), so the flow component of a drawdown is the *residual after*
the fundamental component, never a chart pattern. Same (percentile, slope) emission as the A-gauges.

- **O1 — revision-anchored gap:** over the episode window (pre-DEFECT 20d high → today):
  `gap = ΔlnP − ΔlnE_ntm`. Emit raw and as a percentile vs the 3y distribution of same-length
  rolling windows. Jul-1→3 worked value: SKH ΔlnP ≈ −29% (log), ΔlnE ≈ 0 → the *entire* drawdown
  was gap. A genuine demand crack shows ΔlnE falling with price → small gap → no overshoot.
- **O2 — de-rating z:** Δ(NTM P/E) over the window, z-scored vs its 3y daily-change distribution
  scaled by √window-length. Separates "multiple compressed on unchanged earnings" (flow-suspect,
  or crowding-premium repricing) from "estimates fell" (fundamental).
- **O3 — retracement anchor:** `anchor = P_peak × (E_today / E_peak)` — where the pre-cascade
  price *would* sit on today's earnings estimates. `overshoot = anchor − low`. The bounce
  expectation is **a band, never a point**: `low + r̂ × overshoot`, with `r̂` the episode library's
  retracement-fraction distribution (p25/p50/p75) conditioned on flow-signature strength and belt
  cure. Until the episode harness ships (next handoff), the dashboard prints anchor + raw
  overshoot with `band: pending episode library`. Jul-3 sanity: the close recovered the morning
  flush plus ~⅓ of the two-day fall — the crowding-premium share of the gap stayed repriced, which
  is why r̂ conditions on how much of the gap the A-composite attributes to crowding unwind.

**The anchor-staleness veto (the intuition's known failure mode, §11):** "fell more than
revisions" is wrong precisely when revisions haven't *printed yet*. The O-gate therefore requires
S7′ inside SLA **and** no B1/B7 event (ceiling, statement defection) in the last 5 sessions
without a subsequent estimate refresh; if 30d revision breadth is negative *and steepening*, the
anchor itself is falling — O1's required threshold rises one band (registered default: p80→p90).

### The exhaustion detectors (C1–C5) — "it could bounce back… now"

Dated events with evidence payloads, like the B's. Families in braces.

- **C1 — belt discharge** *{mechanical}*: the **belt-load meter** (in `features/exhaustion.py`:
  percentile of Σ over the current consecutive-down-close run of |close-to-close return| ×
  S10-fuel-percentile; KR names add the S3 retail net-sell share) was ≥ p90 at yesterday's close,
  and today prints a higher low with an up-close — the scheduled forced supply cleared without
  breaking the low.
- **C2 — flush-exhaustion print** *{tape}*: promoted from old §7 — an episode-drawdown-≥15% day
  closing up on ≥ 1.5× ADV, or an undercut-and-reclaim of a prior panic low within 2 sessions.
- **C3 — absorber turn** *{flow}*: S3 institutional 10d net-buy z ≥ +1.5 while foreign net ≤ 0
  and price < O3 anchor — the scheduled buyer stepping in front of the finish (Jul-3: institutions
  +₩2.65T against foreign −₩1.48T).
- **C4 — cure confirmation** *{mechanical}*: complex-weighted up-close ≥ +3% — tonight's close
  cures collateral ratios and disarms tomorrow's belt (the chain-breaker, not just a bounce).
- **C5 — cross-market confirm** *{cross-market}*: the `xmarket_reference` (KR: TSMC/TAIEX) closes
  green on the candidate day, or the US complex members closed green overnight — the 10:00-clock
  information at EOD granularity.

**EXHAUST logic:** state must be **CASCADE** (see below) and the **O-gate open** (O1 ≥ p80 with
the staleness veto satisfied). Fire on **≥ 2 of C1–C5 from ≥ 2 families within 3 sessions**. A
new hard down close (complex ≤ −3%) resets the C-window and reloads CASCADE — the belt is
recharged, per the conveyor mechanics. Unconditioned C-events are logged, never fire (same
placebo discipline as the B's).

**State machine extension:** `EXTREME + DEFECT` + episode drawdown ≥ 8% from the pre-DEFECT high
→ **CASCADE** (published sub-state; overlay already at 0.60). CASCADE + EXHAUST → staged re-entry
(§7). CASCADE with neither EXHAUST nor a new down-close for 20 sessions at state ≤ ELEVATED →
timer re-entry (the old backstop, kept). All thresholds are registered defaults in
`config/crowding.yml` — calibrate on validation, freeze in the ledger.

**Division of labor (deliberate, not a gap):** the engine's clock is EOD. Signal C names the
*candidate day* and arms the human the night before (alert: "CASCADE · belt-load p97 · sell
sidecar today → tomorrow morning is the scheduled capitulation slot"), and grades the day after.
The intraday 9:00–10:30 execution sequence belongs to the human running the
[V-day checklist](../../systematic-trading/checklists/catching-the-v-day-checklist.md) — no
minute-data scope creep in Phases 1–3.

**Pre-registered KPI extension (Signal C is judged by these, nothing else):** per episode —
re-entry slippage vs the oracle low; fraction of qualifying V-days entered vs missed;
false-re-entry rate (EXHAUST fired, then a new episode low within 5 sessions); all net of the §7
tax/churn math. Same KPI philosophy as §0: timing quality of the *re-entry*, not "calling bottoms."

## 6. Falsification harness (what makes this not astrology)

- **Episode library** (`evaluation/episodes.py`): schema `{id, complex, condition_start, peak_date,
  trough_date, peak_drawdown, mechanism_tags, data_coverage_tier, sources[]}`. Seeds: **2026-06/07
  memory** (design case — see contamination note), 2024-08 yen-carry unwind, 2021-11 growth/ARKK
  top, 2021-01 GME (short-crowding mirror), 2020-02, 2018-01 short-vol, 2018-09 semis top, 2015-08
  CNH, 2011-05 silver, 2008-07 crude, 2007-08 quant quake, 2000-03 Nasdaq. Coverage is tiered:
  full 14-component data exists only ~2015+; older episodes run the price/breadth subset —
  claims are made per tier, never pooled silently.
- **Holdout-contamination note (binding):** the June-2026 memory episode falls inside PROTOCOL
  v3's holdout (≥ 2026-06-01) *and* motivated the design — it is hindsight-contaminated by
  construction. It is used as a **narrative sanity case only** (Phase-2 exit check) and **excluded
  from every performance statistic**. Evidence = validation-era episodes + the forward paper record.
  **The same quarantine binds the July 1–3, 2026 cascade-and-V** (it motivated Signal C the day it
  happened) — demo/seed only, never validation.
- **Signal-C episode annotations:** each library episode gains
  `{cascade_start, exhaust_date, retracement_frac_5d/21d, O1_at_trough, belt_load_peak}` so r̂
  (O3's band) is estimable per tier. Two required counterexample labels: **2024-08-05 yen-carry**
  (global constraint — the 10:00 turn never came; tests that C stays *silent* when the constraint
  outsizes the local morning) and any episode where an apparent flush preceded genuine estimate
  cuts (tests the anchor-staleness veto).
- **Pre-registered hypotheses:** (H6-A) EXTREME shifts the *left-tail* of 21/63d forward returns
  (skew/vol), not necessarily the mean; (H6-B) DEFECT|EXTREME shifts the *mean* of 5/21d forward
  returns negative vs the unconditional and vs EXTREME-without-DEFECT; (H6-FP) unconditioned
  B-events have no edge (the placebo arm). **Added 2026-07-03:** (H6-O) trough-forward 5/21d
  retracement fractions are increasing in O1-at-trough — episodes with a large revision-anchored
  gap recover more of it (the overshoot→reversion claim); placebo: O1 recomputed against a
  randomized estimate series shows no such ordering. (H6-C) EXHAUST-timed re-entry beats both the
  old two-pattern heuristic and the 20-session timer on re-entry slippage vs the oracle low, net
  of tax; placebo: unconditioned C-events (outside CASCADE / O-gate shut) have no timing edge.
- **Statistics for n≈12:** conditional forward-return distributions with **block bootstrap by
  episode** (the episode, not the day, is the independent unit); exact binomial CIs on hit rates;
  lead-time distributions; per-component ablation; parameter-plateau requirement (a threshold that
  only works at exactly 90 is dead). DSR with v2+v3 trial counts imported.
- **Promotion gates:** no component enters the composite without a registered verdict; the
  composite needs H6-A supported on validation; the overlay needs H6-B supported **plus** the
  Phase-4 paper month. Fresh-eyes audit before any live authority; kill is final.

## 7. Portfolio integration — the overlay (how it touches money)

- **Exposure scalar `m`:** NORMAL → 1.00 · ELEVATED → 1.00 (awareness only) · EXTREME → 0.85
  **optional pre-trim, default OFF** (KR tax math below) · **EXTREME + DEFECT → 0.60**, staged in
  thirds over ≤ 3 sessions. Final engine exposure = **min(H1 scalar, H6 m)** — two independent
  gates, never multiplied.
- **Re-entry (staged, in halves) — rewritten 2026-07-03, superseding the two-pattern heuristic:**
  first half on **EXHAUST** (§5b: CASCADE + O-gate open + ≥ 2 of C1–C5 — the old undercut-reclaim
  and flush-day patterns live on as C2); second half on the next session's close *holding* (no new
  hard down close — the belt stayed disarmed). Backstop unchanged: 20 sessions elapsed with state
  ≤ ELEVATED. A post-re-entry new episode low within 5 sessions logs a false-re-entry (KPI, §5b)
  and re-enters CASCADE. The re-entry ticket prints the O3 anchor + overshoot next to the
  net-of-tax math, so the human sees *both* "what the discount is against revised fundamentals"
  and "what re-entering costs" on one line.
- **Churn/tax guards:** max one trim+re-add cycle per name per quarter. Every ticket prints the
  **net-of-tax breakeven**: KR 22% on gains > ₩2.5M means a trim is +EV only if it avoids a
  drawdown ≥ (tax paid + spread + re-entry slippage) — the ticket shows this number next to the
  episode library's conditional median drawdown, so the human decision is a comparison, not a vibe.
- **Two books, one module:** (a) the engine's systematic sleeve consumes `m` automatically in
  `portfolio/construct.py`; (b) the **discretionary core book** (the real money, held at the
  broker) receives human-readable tickets via `live/sleeve.py` — "trim 25% of MU, rationale,
  breakeven math" — and `live/adherence.py` logs follow/ignore. Adherence stays a first-class
  metric; an ignored ticket is data.
- **Hard constraints (inherited + new):** long-only, no leverage, no options, no shorting; max
  exposure delta 25%/day; overlay authority is revocable by one config flag (`h6_authority:
  dashboard|paper|live`).

## 8. Report & alerting spec

Nightly report gains a **Positioning panel**: state gauge with CROWD score history; the 14-
component table (percentile bar, slope arrow, staleness age each); active B-events timeline with
evidence links; episode-relative context ("current drawdown vs library percentiles"); the overlay
scalar + any open ticket with its breakeven math; and a **data-freshness table** (every source vs
its SLA). **Signal-C additions:** an overshoot dial (O1 percentile + raw ΔlnP-vs-ΔlnE decomposition
— "how much of this drawdown is flow"), the belt-load gauge with tonight's cure/reload verdict, the
O3 anchor + band, and the active C-event timeline while in CASCADE. Alerts (existing
`ops/alerts.py` webhook): state transitions, any DEFECT fire (with the family vote),
**CASCADE entry, the armed-morning alert ("belt-load ≥ p90 → tomorrow is the scheduled
capitulation slot" + checklist link), any EXHAUST fire**, any source SLA breach, any quarantined
batch (§9). Later (optional, Phase 4+): a
17:30 KST mini-run refreshing KR-flow components after the Seoul close, so a KR defection alerts
before the US open — deferred until the single nightly clock proves insufficient.

## 9. Ops hardening (production non-negotiables)

- **Fail-soft matrix:** OHLCV fail-hard (halts, inherited). Every H6 source fail-soft: on failure
  the component goes `stale`, the composite re-weights by coverage, and below 8/14 the state is
  `INSUFFICIENT_DATA` with the **overlay frozen at its last valid value** — never silently reset
  to 1.0. Fail-closed on risk.
- **Staleness SLAs** (sessions): options 2 · KRX flows 2 · ETF AUM 3 · estimates 5 · COT 10 · SI 20
  · surveys 10. Breach → alert + stale-mark; carry-forward only within SLA.
- **Vendor-drift quarantine:** per source per batch — pinned schema hash, row-count z vs history,
  KS-test on key field distributions. Any tripped check → batch quarantined + alert; **never
  auto-adapt** to a changed feed.
- **Idempotency:** every ingestor watermarked per (source, ticker), retries with exponential
  backoff, re-run-safe via run-date keys (inherited pattern). Backfill runbook per source in
  `docs/RUNBOOK.md`: pykrx full history; FINRA/COT archives; options history purchased once;
  S5/S7/S8 forward-only (stamped).
- **Testing:** unit — hand fixtures for every formula (percentile edges, CUSUM traces, hysteresis).
  Property (hypothesis) — composite bounded [0,100]; missing data can never *raise* the score; the
  state machine cannot oscillate on constant input. Integration — a synthetic fixture lake
  replaying a scripted rise→crowd→defect→crash episode through the full DAG → snapshot the report +
  assert the alert. Protocol — evaluation cannot read post-holdout rows (boundary test, inherited);
  ledger append-only. **Chaos** — a CI variant deletes one source dir and asserts the degrade path
  + alert fire.
- **Config discipline:** every threshold in `config/crowding.yml`, versioned; a parameter change is
  a new registered variant, not an edit.

## 10. Build phases & exit gates (calendar-aware)

**Sequencing decision (2026-07-03 — supersedes the paragraph that stood here):** H6 is now **the
first build** — module-first instead of engine-first, per user call. It rides on a **minimal
spine** borrowed from the outline's Wk-1 scaffold (repo/CI/parquet lake/quality gates/report/
alerts + the ledger); the IC evaluation core, H1–H5, and every money path are **deferred, not
dropped**. The buildable scope, milestones, and definitions of done live in the
[H6-first build handoff](h6-first-build-handoff.md) — that document (plus this spec and the
outline) is what gets handed to the coding agent.

- **Phase 0 — decisions (½ wk, can run now):** vendor *shortlist only* (S2, S7 —
  subscriptions land at the Phase-4 gate, §3.2); complex
  definitions; confirm KRX/pykrx ToS for this use; EXTREME pre-trim default (recommend OFF);
  SK Hynix ADR inclusion date; sign off the KPI in §0. *Gate: decisions logged in the ledger.*
- **Phase 1 — data layer (~2 wks):** S1 + free-tier S2′–S9 ingestors + registry + quality gates +
  freshness panel; PIT backfills where clean (S3, S4, S6, S9); the S2′/S7′ forward archives start
  accumulating from day 1. *Exit: 5 consecutive green nightly runs, every source inside SLA,
  backfill ≥ 3y on the clean-history sources.*
- **Phase 2 — features + state (dashboard-only, ~1–1.5 wks):** A1–A14, B1–B8, **O1–O3 + belt-load
  meter + C1–C5 (CASCADE/EXHAUST states; O3 prints anchor-only until Phase 3's episode library
  supplies r̂)**, composite, state machine, report panel, alerts. *Exit: state vector publishing
  nightly; the June-2026 replay sanity check shows EXTREME by mid-June and a DEFECT vote by
  Jun-25/26; **the Jul-1→3 replay shows CASCADE by Jul-2's close, the armed-morning alert that
  evening, and EXHAUST on Jul-3's close** (both replays = sanity/demo, explicitly not validation —
  see §6).*
- **Phase 3 — falsification (~2 wks):** episode library, conditional harness, registered verdicts
  for H6-A / H6-B / H6-FP on validation-era episodes; component obituaries as they die. *Exit: ≥ 2
  registered verdicts; fresh-eyes audit of the surviving spec.*
- **Phase 4 — paper overlay (≥ 4 wks elapsed):** paid S2/S7 subscriptions activate at this gate
  (§3.2); `m` applied to the paper portfolio only; tickets
  generated but flagged PAPER. *Exit to live tickets: ≥ 20 clean sessions, zero gate failures, no
  quarantines open, adherence loop tested, second fresh-eyes pass.* Live = tickets to the human
  core book first; systematic-sleeve authority last.
- **Ongoing:** quarterly re-audit (drift, coverage, realized-vs-registered hit rates); episode
  library grows one labeled post-mortem per real episode.

## 11. Pre-committed failure modes & responses

| Risk | Detection | Response |
|---|---|---|
| PIT leakage (esp. S7 revisions) | protocol boundary test; observed_at audits | forward-clean stamp; exclude from history; re-verdict |
| Vendor drift / silent schema change | §9 quarantine checks | batch quarantined, human review, never auto-adapt |
| Small-n overfit | plateau + ablation + DSR + episode bootstrap | component obituary; composite survives by coverage |
| Meta-crowding (signal decay) | forward hit-rate vs registered expectation, quarterly | de-weight famous components (A12, A6) before bespoke ones (A13, S3) |
| Overlay whipsaw (tax bleed) | per-cycle net-of-tax P&L in adherence log | quarterly cycle cap; raise DEFECT k; demote to dashboard |
| KR data access breaks | S3 SLA breach | KRX direct endpoints fallback; complex runs US-only subset |
| **Anchor staleness (Signal C's intrinsic trap):** price falls *ahead* of estimate cuts that are coming — O1 reads "overshoot" when it's actually early information | S7′ revision-breadth slope; B1/B7 fires without estimate refresh | O-gate veto (§5b): threshold rises p80→p90; EXHAUST blocked until estimates refresh; false-re-entry KPI catches residuals |
| Cascade outlives the morning (multi-day/global constraint — the Aug-2024 shape) | new hard down close inside CASCADE | C-window resets, belt reloads, re-entry stays blocked; the 2024-08 counterexample episode tests exactly this |
| **Kill criterion (binding):** after 12 forward months — DEFECT-conditioned hit rate ≤ base rate (exact binomial), or two consecutive triggered episodes each costing > 1% net with no drawdown avoided | annual review | **demote permanently to dashboard-only** (it retains awareness value; it loses money authority) |

## 12. Cost & effort budget

Data: **$0/mo through Phases 1–3** (free tier S2′/S7′); **≈ $60–170/mo from the Phase-4 gate**
(+ optional ~$100–500 one-time options history, §3.2). Compute: trivial (EOD, vectorized — no new
infra beyond the v3 lake). Build effort: ~5–6 focused weeks across Phases 1–3, then the gated
paper month. Under the H6-first sequencing (§10) the module **is** the schedule: realistic
overlay-live is **~9–11 weeks from the first scaffold commit**; the IC core and H1–H5 resume
afterwards on the outline's own plan.

## Relationships
- Repo skeleton + protocol this plugs into: [Engine v3 project outline](project-outline.md) ·
  [design brief](design-brief.md).
- The two-signal concept and its manual June run: meta-compute selloff & memory state ·
  tripwire playbook ·
  [distribution & pullback tells](../../shared/concepts/distribution-and-pullback-tells.md) ·
  MU print postmortem (the ceiling event).
- Mechanism pages the design leans on: [price formation & the float identity](../../shared/concepts/price-formation-and-the-float-identity.md) ·
  [liquidity cascades & V-reversals](../../shared/concepts/liquidity-cascades-and-v-reversals.md) ·
  [who pays you](../../shared/concepts/who-pays-you.md) ·
  [informed vs. uninformed flow](../../shared/concepts/informed-vs-uninformed-flow.md).
- Signal C's mechanism + operational twin (added 2026-07-03):
  [KRX session clocks & forced liquidation](../../shared/concepts/krx-session-clocks-and-forced-liquidation.md) ·
  [catching-the-V-day checklist](../../systematic-trading/checklists/catching-the-v-day-checklist.md).
- Cohort clocks behind A9/B5: where alpha lives — three pools, three clocks ·
  [unwind duration & flows](../../market-research/positioning/unwind-duration-and-flows-2026-06-30.md).

## Open questions
- Can B5's US proxy (factor-return de-grossing signature) be validated against the episodes where
  prime-brokerage narratives are public (Aug-2007, Jan-2021, Jul-2026)?
- Does A13 (news-response decay) generalize beyond earnings to guidance/capex headlines, or is the
  event set too sparse per complex?
- Where is the tax-adjusted indifference curve for the EXTREME pre-trim (currently default-OFF) as
  a function of position gain and episode-conditional drawdown?
- Is the S7′ free-tier estimate feed *fresh enough* to anchor O1 (the staleness veto assumes
  revisions post within ~days) — or does the O-gate need the paid S7 pulled forward from Phase 4?
- Can r̂ (O3's retracement fraction) be decomposed into a recovered-flow share vs a repriced
  crowding-premium share using the A-composite at episode start (Jul-3's ~⅓ retrace suggests the
  split is real and estimable)?

---
**Refresh triggers:** any Phase gate passed (update status here + journal); any vendor/spec change
(new registered variant); each new labeled episode. When the repo's `docs/H6-DESIGN.md` diverges,
that copy wins and this page gets a pointer note.
