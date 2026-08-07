---
type: concept
title: Leveraged-ETF Decay & the 3x-Daily Trap
description: Why daily-rebalanced leveraged ETFs (e.g. SOXL = 3x daily semiconductors) do NOT deliver their multiple over multi-day holds — the path-dependent volatility drag, derived from first principles, and why it makes a leveraged ETF a poor vehicle for holding through a multi-day catalyst window.
tags: [ml-stats, systematic-trading, instruments, risk, leveraged-etf]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: [../../sources/deep-research-micron-swing-position-2026.md, ../../sources/deep-research-semi-rally-winners.md]
---

# Leveraged-ETF Decay & the 3x-Daily Trap

A **leveraged ETF** (e.g. **SOXL** = Direxion Daily Semiconductor Bull 3X, or its inverse **SOXS** −3x)
promises a **multiple of the *daily* return** of an index — *not* a multiple of the cumulative return over
any longer horizon. Because it **rebalances to its target leverage every day**, its multi-day path is
**compounded**, and compounding of a leveraged series is **path-dependent**: in a choppy market it bleeds
value relative to the naive multiple ("**volatility decay**" / "beta slippage"), while in a smooth trend it
*adds* value. The decay is not a fee or a bug — it is a mathematical property of daily reset.

The issuer says this explicitly (Direxion, primary): the fund seeks "300% … of the … Index" returns **"for
a single day, not for any other period,"** should **"not be expected to provide three times … the return …
for periods greater than a day,"** **"a total loss may occur in a single day,"** and "the Fund will lose
money if the Index performance is flat over time."

## The math (first principles)

Let the index move `+x` then `−x` on two consecutive days (a "whipsaw"), and let `L` be the leverage.

- **Index, 2-day cumulative:** `(1+x)(1−x) − 1 = −x²`.
- **Leveraged ETF, 2-day cumulative:** `(1+Lx)(1−Lx) − 1 = −L²x²`.
- **Naive (wrong) expectation:** `L × (−x²) = −Lx²`.
- **Decay drag** = actual − naive = `−L²x² − (−Lx²) = −x²·L(L−1)`.

For `L = 3`, the drag per whipsaw pair is `−6x²`:

| Index whipsaw ±x | Index 2-day | SOXL 2-day (3x daily) | Naive 3× | **Decay drag** |
|---|---|---|---|---|
| ±5% | −0.25% | −2.25% | −0.75% | **−1.5 pts** |
| ±10% | −1.00% | −9.00% | −3.00% | **−6.0 pts** |
| ±15% | −2.25% | −20.25% | −6.75% | **−13.5 pts** |

The drag grows with the **square of volatility** — so decay is small in quiet tapes and **vicious around
high-volatility events**. (Compounding cuts both ways: a *trending* +10% then +10% gives SOXL +69% vs naive
+63% (3× the compounded index +21%) — a smooth trend *adds* ~6 pts. The asymmetry is that real markets chop, and the over-/under-exposure
that drives the slippage **increases on days the index is volatile near the close** — exactly an earnings/macro
window.)

## The continuous-time view: cube the trend, pay the variance

The whipsaw table generalizes. Under GBM with drift μ and volatility σ, an L×-daily fund's value
is (fees/financing aside) **exactly separable into a convexity term and a decay term**:

```
X_t = X_0 · (S_t/S_0)^L · e^{−½L(L−1)σ²t}
```

- **`(S_t/S_0)^L` — the convexity.** A *power* of the underlying, not a multiple: a clean +100%
  index trend delivers 2³−1 = **+700%** at L=3 (not +300%), and a crash is cushioned (a fraction
  cubed stays positive — why 2022's −35% SOX produced SOXL −85%, not −105%).
- **`e^{−½L(L−1)σ²t}` — the decay.** For L=3 the drag is **3σ² per year**: ~48%/yr at semis'
  normal σ≈40%, and **~0.5%/day (≈10%/month) at cascade vol** (σ_daily 4–5%). The fund is long
  trend-convexity and short realized variance — near-literally long gamma, short vega on the index.

So path, not endpoints: a smooth trend is the dream regime, a violent flat market the nightmare,
and the same −20% index move costs very different SOXL prices depending on how it happened. Live
validation (Jun–Jul 2026): SOXX fell −19.4% from peak in ~3 weeks *in a near-straight line* — the
cube predicted SOXL $158 vs $155.80 actual, i.e. only ~1.5% of accrued decay, because trends
don't pay the drag; the bill starts when the tape turns to chop
(the Jul-7 scenario map).

## When holding is actually optimal — the Kelly gate

"Never hold a leveraged ETF" is an unconditional statement of a **conditional** truth. Long-run
compound growth at leverage L is `g_L = Lμ − ½L²σ²` — a downward parabola in L peaking at the
Kelly/Merton leverage **`L* = μ/σ²`**. Three zones follow (thresholds scale with σ², so vol moves
them quadratically):

| Condition on the index | What L=3 does |
|---|---|
| μ < 1.5σ² (σ=40%: drift < 24%/yr; σ=60%: < 54%) | **negative growth — decays even if the index rises** |
| 1.5σ² < μ < 2σ² | positive, but *less* leverage compounds faster |
| μ > 3σ² (σ=40%: > 48%/yr; σ=60%: > 108%) | 3× is at/below Kelly — holding is genuinely correct |

The honest replacement for "don't hold" is a **two-gate rule: hold only while (1) the trend is on
(e.g. price above the 200-day) AND (2) realized vol is below its median; cut when either gate
fails — and size the sleeve to survive the −80% path.** The right tail (2023: SOX +65%, SOXL
+250%; 2020–21) is real and the cube captures it; the gates exist because the left tail (2022)
and the chop tax are also real, and because at cascade vol *no* sane drift forecast clears the
3σ² bar — even a committed bull re-enters better after vol renormalizes, paying a higher price
for a survivable seat. Caveats that keep the default rule honest: the holder is implicitly short
realized vol (blows up on the unforecast tail), regimes are labeled cleanly only in hindsight,
gap risk can gate any filter, and holding through −50% dips to stay in trend is behaviorally
brutal — for anyone who won't run the gates, "never hold" remains the right lie.

## Why it matters for holding through a catalyst

A leveraged ETF is engineered for **intraday-to-one-day** exposure. Holding one **across a multi-day,
multi-catalyst window** (e.g. an earnings print Wednesday night *and* a macro release Thursday) stacks three
distinct costs on top of the directional bet:

1. **Leverage** — the index move is multiplied (3x), so the *variance* of your outcome is ~9x a single share
   of the underlying.
2. **Volatility decay** — the path-dependent drag above, which is largest precisely when the window is volatile.
3. **Compounded macro exposure** — every systematic move in the window (a hot CPI/PCE print, a rate scare) hits
   the leveraged fund at the full multiple, not just the single-name catalyst you were positioned for.

So a leveraged ETF held through a stretched event window is **a worse vehicle than the unleveraged exposure
for the same view**: you pay decay and triple every unrelated shock, in exchange for amplifying a directional
bet whose expected one-day drift is ~zero absent a real edge (the event EV is a
[variance bet — see the swing-math brief](../../sources/deep-research-micron-swing-position-2026.md)).

## Worked example — SOXL through the Micron print (June 2026)

[Micron's FQ3 print](../../market-research/memory/micron-fq3-2026-earnings.md) (Wed Jun 24 AMC), with
[PCE the next morning](../../market-research/weekly/week-ahead-2026-06-22.md), is the canonical case.

- **SOXL tracks the NYSE/ICE Semiconductor Index 3x daily.** MU is a **top constituent** (working assumption
  **~7%**; the precise issuer weight list could not be verified — treat as approximate).
- **MU's direct contribution is small:** a 6.5% / 10% / 17% one-day MU move adds only **~1.4% / 2.1% / 3.6%**
  to SOXL *from MU alone* (`≈ 3 × weight_MU × move_MU`).
- **The realistic ±10-15%+ window swing comes from elsewhere:** **sympathy** (a MU HBM/guidance surprise
  re-rates NVDA/AMD/AMAT/equipment) **+ Thursday's macro × 3 + decay** — *not* from MU directly. (The sympathy
  magnitude is an unverified estimate.)
- **Implication:** the leveraged leg expresses the *same* [long-AI-memory bet](../instruments/semiconductors.md)
  as a direct MU/semis holding, but adds leverage, decay, and 3x macro. If trimming risk into the window, the
  leveraged leg is the structurally costliest to hold.

## Key points
- The multiple applies to **daily** returns only; multi-day return ≠ multiple × index return —
  it's `(S_t/S_0)^L` times a decay factor: **cube the trend, pay the variance**.
- Decay scales with **volatility²** and with `L(L−1)` — for 3x, `−6x²` per whipsaw pair, `3σ²`/yr
  continuous (~48%/yr at σ=40%; ~0.5%/day at cascade vol).
- Choppy tapes bleed; smooth trends add — but volatility near the close (events) maximizes slippage.
- Variance of a 3x ETF outcome ≈ **9x** the underlying — a leverage decision is a [risk-of-ruin](risk-of-ruin.md) decision.
- Holding is defensible only past the Kelly gate (`L* = μ/σ²` ≥ 3, i.e. Sharpe ≳ 1.2 at σ=40%) —
  operationally the two-gate rule: trend on AND vol below median, sized to survive −80%.
- The rebalance flow is reflexive at scale: an L× fund trades `L(L−1)·|r|·AUM` *with* the day's
  move into every close (SOXL at ~$30B AUM on a −6.7% day ≈ $12B of mechanical selling) — a large
  levered book is a synthetic short-gamma overlay on its own index.
- The product is designed for ≤1-day holds; using it as a multi-day position is an off-label use the issuer warns against.

## Relationships
- Amplifies exposure to the [semiconductors](../instruments/semiconductors.md) regime; the SOXL-decay figure
  was a long-standing open item from the [semi-rally-winners research](../../sources/deep-research-semi-rally-winners.md), now derived here.
- Interacts with [regime detection](../../ml-stats/concepts/regime-detection.md) (vol-targeting / when leverage is survivable) and
  [stop-losses & exit management](stop-losses-and-exits.md) (a leveraged hold needs tighter, regime-aware exits).
- Sizing/survival lens: [Kelly criterion](kelly-criterion.md) & [risk of ruin](risk-of-ruin.md) — leverage raises geometric-growth drag and ruin probability;
  the Kelly-gate section above is the applied form.
- Event context: [Micron FQ3-2026 earnings](../../market-research/memory/micron-fq3-2026-earnings.md);
  the full instrument map at a live decision point: SOXL scenario map, Jul-7-2026.
- The rebalance-flow cohort in context: [multi-week unwinds & recoveries](multi-week-unwinds-and-recoveries.md)
  (leveraged ETFs = the intraday amplifier cohort).

## Open questions
- ~~The current ICE Semiconductor Index constituent weights~~ **resolved 2026-07-07**: MU 8.16%
  (#1), AMD 8.15%, NVDA 7.50%, AVGO 6.56%, INTC 6.17% (as of Jul-2-2026 ◐; the old ~7% MU working
  assumption was right, and MU has since become the top weight). Still open: the quantified
  MU→complex sympathy beta.
- Empirical long-run SOXL tracking-vs-decay over a full semi cycle (how much of the gap to 3x-cumulative is
  decay vs fees vs financing). Partial live datapoint (Jun–Jul 2026): a *trended* −19.4% index leg
  accrued only ~1.5% decay — the decomposition says measure decay against realized *chop*, not time.
