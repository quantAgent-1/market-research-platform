---
type: research-brief
title: "Micron FQ3 Print — Swing Magnitude & the Hold-vs-Sell Position Question (Deep-Research, June 2026)"
description: First-principles verification of the Micron June-24 swing math and a hold-vs-sell framework for a concentrated MU + SOXL book. Headline correction — the implied move is ~14% WEEKLY / ~8-9% event-jump, NOT the ~17% one-day figure (refuted); realized ~6.5% (20Q); SOXL 3x-daily decay derived; the two positions are the same long-AI-memory bet.
tags: [market-research, semiconductors, memory, micron, options, soxl, evidence]
timestamp: 2026-06-22T00:00:00Z
status: active
sources: []
---

# Micron FQ3 Print — Swing Magnitude & the Hold-vs-Sell Position Question

**Source:** Claude Code `deep-research` run `wf_a7f8b589-e70` (2026-06-22). **Walled on the session-quota
mid-verification** (1st pass: 14 src → 66 claims → top-25 extracted, but all 75 verify votes died on the
quota error → a *false* "0-0 refuted / inconclusive"); **resumed past the 20:50 KST reset** (`args` re-passed,
new task) → completed clean.
**Method:** 5 angles → **23 sources → 106 claims → 25 adversarially verified → 15 confirmed, 10 killed → 11
findings.** Strongest anchors are **primary** (Micron & Broadcom 8-Ks via SEC/StockTitan; Direxion
prospectus/fact sheet; TrendForce press release); options/IV/realized-move and consensus rest on secondary
vendors (Barchart, OptionsAI, OptionSlam), several cross-corroborated. **Deliberately adversarial** (try-to-
refute each claim) and **first-principles** (the swing math and SOXL decay were *re-derived*, not just cited).
**Purpose:** go deeper on, and stress-test, the live answer to "what to expect from the print, is it sell-
the-news, and what's the risk of holding MU + SOXL through it."

## Headline verdict
The setup is **real and adversarially robust**: MU reports **Wed June 24, AMC**, into an all-time high
(~$1,134, +~756%/yr), with consensus (~$19.72 EPS / ~$34.5B rev) **above** its own guide → a **headline beat
is the base case** and the reaction hinges on the **forward narrative**, not the beat. The AVGO precedent is
verified (a non-blowout print on a priced-for-perfection name sold off hard on a *failure to raise*). On
magnitude, the key quant finding survived 3-0 and was re-derived: **realized ~6.5%, priced event-jump
~8-9%, weekly straddle ~14% — a ~2x volatility-risk premium on average** (not a per-print guarantee). For the
position, the education-framed conclusion: **MU and SOXL are the same long-AI-memory bet**; SOXL adds 3x-daily
leverage, **confirmed structural volatility-decay**, and 3x exposure to Thursday's macro print — so a stock-
holder's event **EV ≈ zero-drift / huge-variance unless they hold a genuine edge on the guidance.**

## Key corrections to the prior live answer (the value-add)
1. **"~±17% one-day move" — REFUTED.** At IV ~103%, a one-day implied move is only **~5.4%** (S·IV·√(1/365)).
   The ~14-17% figures are a **WEEKLY straddle** (to Fri Jun 26), not one-day. Best-sourced weekly ≈ **14.3%**
   (OptionSlam); decomposing it implies a **~8-9% discrete earnings event-jump** on top of multi-day diffusion.
   The "17.6%" (1-2) and "11%" (0-3) vendor figures were refuted. **Use ~14% weekly / ~8-9% event-jump.**
2. **AVGO was NOT a "clean beat across the board."** It beat adj-EPS ($2.44 vs $2.40) but **narrowly *missed*
   revenue** ($22.19B vs $22.27B strict consensus, +48% YoY); it fell **~12-15%** for the forward reason (no
   raise of the $100B AI target + soft near-term AI guide). The lesson survives; "beat across the board" was overstated.
3. **The specific analyst-target list was REFUTED 0-3** ("avg $1,091 / Cantor $1,500 / Susquehanna $1,750 /
   27 Strong Buy" as a sourced set). The *spirit* (crowded-bullish, stock near/above avg target) is supported
   by prior wiki research — but don't cite those exact numbers as verified.
4. **SOXL's exact index weights were REFUTED 0-3** (could not confirm MU 7.0% / NVDA 8.4% / etc. from the
   issuer). MU is a top holding; **~7% is now a working assumption, not a verified weight.**

## Findings by topic (confirmed unless noted)

### The print (high)
- **Date Wed June 24 AMC** ✓ (Barchart "06/24/26 [AMC]"; Micron IR; Wall Street Horizon "CONFIRMED").
- **Consensus above guidance** → beat near-certain. Cite **central ~$19.72 EPS / ~$34.5B**, *not* the
  $20.25 / $34.66B top-of-range marks. Guide (primary FQ2 8-K): **rev $33.5B±0.75, non-GAAP GM ~81%, non-GAAP
  EPS $19.15±0.40.** **GM 81% (record, non-GAAP forecast)** — the conflicting **68% is erroneous** (no source). ✓
- **What would count as a "RAISE"** (the AVGO escape hatch): a numerical HBM-share target, raising/pulling-
  forward the **$100B-by-2028 HBM TAM**, or an explicit **sold-out-2027** commitment. **Critical nuance:**
  management has *repeatedly declined* a numerical HBM share target, and only **2026** is the confirmed sold-out
  year — so the single most bullish catalyst is precisely the one Micron has historically **withheld**, mirroring
  AVGO's sin. *(medium — from prior verified research + primary TrendForce.)*

### Swing magnitude (high)
- **Realized:** MU's average one-day post-earnings move is **~6.53% over 20 quarters** (independently
  recomputed = 6.534%), **~4.4-4.5% last 4Q** (MarketChameleon 4.4% corroborates). **−3.78% in Mar'26 despite a
  ~33% EPS beat** ✓. Recent signs split (−3.8 / +10.2 / −2.8 / −1.0). **Fat tails:** the last 8 prints include a
  **+23.8% and a −13.8%**, so a wide *priced* move is not irrational.
- **Implied & the VRP gap (re-derived):** IV **~103%** (IV-rank ~95, pctl 97) ✓ — a large IV-crush setup.
  Naive 1-day move at 103% ≈ 5.4% → the ~14% is **weekly**; decompose → **~8-9% event-jump**. Versus ~6.5%
  realized ⇒ **~2x volatility-risk premium**. **But REFUTED:** the blanket "IV is *systematically* overpriced" —
  realized **exceeded** implied in **4 of the last 8 quarters**, so the straddle-seller edge is an *average*, not
  a per-print guarantee.

### Direction (high on AVGO; medium on base rate)
- **AVGO precedent** ✓: beat EPS, narrowly missed revenue, **fell ~12-15%** on a *failure to raise* its
  long-term $100B AI target (total Q3 guide actually exceeded). The live template for "records weren't enough;
  the forward narrative was."
- **Base rate:** sell-the-news is an **elevated risk for stretched ATH AI names, not a law** — MU itself rose
  **+10.2%** on a ~21% beat in Dec'25 and fell −3.78% on a ~33% beat in Mar'26. Positioning is directionally
  crowded-bullish, but the precise "priced-for-perfection" target list could not be verified (see correction 3).

### Fundamental durability (high)
- ~20x FY26 / ~12x FY27 EPS is on **peak-cycle earnings** → **rational pricing, not a clear bargain.** Cycle
  **dampened/elongated, not abolished**; bifurcated (HBM stickier; commodity DRAM/NAND cyclical); **HBM margins
  run *below* commodity DDR5** (TrendForce, confirmed persistent through mid-2026) — the cleanest single argument
  against a secular HBM premium. China (CXMT/YMTC) + HBM4 oversupply once all three vendors are NVIDIA-qualified
  are the live 2027 glut triggers. **Value-trap risk is genuine if 2027-28 turns.** *(Grounds the durability
  view in the prior bear-tilted [re-rate brief](deep-research-memory-rerate-2026.md).)*

### SOXL & the read-through (high on mechanics; medium on read-through)
- **3x the DAILY return** of the NYSE/ICE Semiconductor Index; issuer states it should **not** be expected to
  deliver 3x over >1 day, and **"a total loss may occur in a single day."** ✓ **Derived decay:** a ±10% two-day
  whipsaw → **SOXL −9% vs index −1%** (6-pt drag vs naive 3x); ±15% → SOXL **−20%**. Trending moves *add* ~6 pts
  (compounding cuts both ways). → unsuitable to **hold** across a multi-day, two-catalyst window.
- **Read-through (derived):** at MU ~7% weight, a 6.5%/10%/17% MU move gives SOXL only **~1.4%/2.1%/3.6% from
  MU alone** (matches the prior "~3.6%" estimate). The realistic **±10-15%+** event-window swing comes from
  **sympathy** (NVDA/AMD/AMAT re-rating) **+ Thursday's macro ×3 + decay** — the sympathy magnitude is an
  **unverified estimate** (flagged open). See the new concept page: [leveraged-ETF decay](../shared/concepts/leveraged-etf-decay.md).

### Macro overlay (low — UNVERIFIED this run)
- **NOT in this run's verified set:** PCE/GDP date+time, Kevin Warsh as Chair, the June dot-plot hike-flip,
  hike-priced next move, VIX ~16.8, Iran/Hormuz oil tail. Only the **structural point** is relied upon — a
  second, macro catalyst lands the day after the print, and SOXL gets it 3x. *(These specifics WERE verified in
  prior-session research — the [week-ahead brief](deep-research-week-ahead-2026-06-22.md), 22/25 — but were not
  re-tested here; treat as prior-verified.)*

### Decision framework (medium — synthesis; EDUCATION, not advice)
- **Scenario × macro P&L sketch** (illustrative, MU ~$1,134 spot): **(A) Beat+RAISE × benign-PCE** — MU +8-15%,
  SOXL +15-30% (the only clearly favorable cell); **(B) Beat-no-RAISE [the AVGO base case] × benign** — MU −4 to
  −10%, SOXL −10 to −25%+; **(C) In-line × benign** — MU ~±3-6% (muted), SOXL ~±10% bleeding decay; **(D) Miss ×
  benign** — MU −10 to −17%+, SOXL −30%+. **Any column × HOT-PCE** shifts both down and amplifies SOXL 3x Thursday.
- **EV vs variance:** with realized ~6.5% roughly centered and no verified directional edge, **IV is the market's
  fair price of the gap** → a stock-holder's event EV ≈ ~0 drift / huge variance, justified only by a genuine edge
  on the *guidance*.
- **Concentration:** MU + SOXL = the same trade → doubling; SOXL triples it AND adds decay AND triples Thursday's
  macro. The single strongest education point.
- **Middle paths:** trimming the **leveraged leg (SOXL)** removes leverage + decay + 3x-macro while keeping core
  exposure; a **collar/protective put at peak IV (IV-rank ~95) is expensive** (protection bought at the top of its
  range; post-print IV-crush erodes long-vol hedges).
- **What flips the call toward holding:** a credible **explicit forward RAISE** (numerical HBM-share target /
  raised-or-pulled-forward $100B HBM TAM / sold-out-2027 commitment + HBM4 36GB allocation). **What confirms
  caution:** in-line guidance, no long-term raise, any 2027-softness hint, or a hot PCE.

## What got refuted (do NOT cite)
- MU implied move **"17.6% one-day"** (1-2) · **"~11%"** (Bloomberg/Investing.com, 0-3) · "7.5%".
- The blanket **"IV systematically overpriced / guaranteed straddle-seller edge"** (0-3 — realized > implied in
  4 of 8 recent quarters).
- The **exact SOXL index weights** (MU 7.0 / NVDA 8.4 / AVGO 8.3 / AMD 6.5 / AMAT 5.9) (0-3 — unconfirmed from issuer).
- The **specific analyst-target list** (avg $1,091; Cantor $1,500; 27 Strong Buy) (0-3 as a sourced set).
- An 8-quarter realized average of **8.6%** (0-3 — shorter/noisier window than the robust 20Q ~6.5%).
- AVGO exact-magnitude "~12%" / "~14%" variants split (1-2) — the *drop* is fact, the precise number contested.

## Caveats
- **Time-sensitivity:** a 2-day-pre-print snapshot in a fast tape — IV keeps inflating into the print then
  crushes after; price/consensus drift weekly. **After June 24 this goes stale; the post-mortem replaces it.**
- **N=1:** AVGO + MU-Mar'26 establish *elevated* sell-the-news risk, **not** a deterministic law.
- **Forecast vs fact:** the GM 81%, $100B TAM, "tight beyond 2026," 2027 price surge are **forecasts**; the date,
  "HBM sold out 2026," "management declined a share target," and AVGO's result are **facts**.
- **Unverified this run:** the whole macro overlay; the MU→complex sympathy magnitude.

## Open questions
1. The **clean single-event ATM-straddle** implied move (event-jump isolated from the weekly horizon) — best-
   sourced is OptionSlam's ~14.3% *weekly*; the ~8-9% event-jump is *derived*. A live front-expiry ATM-straddle
   pull on Jun 23-24 would resolve it (and could use the `alpaca-data` lake / OPRA).
2. The **actual ICE Semiconductor Index constituent weights** + a quantified **MU→complex spillover** (event-study
   of prior MU prints' same-day effect on NVDA/AMD/AMAT) — drives the realistic ±10-15% SOXL window swing.
3. Independent re-confirmation of the **macro overlay** (PCE/GDP timing, Warsh, dot-plot, VIX, oil).
4. **Whether Micron actually delivers a forward RAISE on June 24** — the single variable that flips the asymmetry,
   and the one management has historically withheld. Only the print resolves it → fill the post-mortem stub.

## Feeds into the wiki
- Updates: [Micron FQ3-2026 earnings note](../market-research/memory/micron-fq3-2026-earnings.md) (corrected
  swing-math; resolves its flagged-open implied-move gap; direction refinement; SOXL read-through).
- New concept: [Leveraged-ETF decay & the 3x-daily trap](../shared/concepts/leveraged-etf-decay.md) — closes the
  long-standing "SOXL decay unverified" open item from the [semi-rally-winners brief](deep-research-semi-rally-winners.md).
- Builds on the [first memory brief](deep-research-memory-cycle-micron-2026.md), the
  [gaps follow-up](deep-research-micron-gaps-2026.md) (which left the implied-move unpinned), and the
  [re-rate brief](deep-research-memory-rerate-2026.md) (durability/value-trap).

## Primary / key sources
- Micron FQ2-FY2026 8-K guidance (SEC EDGAR / StockTitan): rev $33.5B±0.75, non-GAAP GM ~81%, non-GAAP EPS $19.15±0.40.
- Broadcom Q2-FY2026 8-K (SEC / StockTitan): rev $22.187B (+48% YoY), non-GAAP EPS $2.44 — https://www.cnbc.com/2026/06/03/broadcom-avgo-earnings-report-q2-2026.html
- Direxion SOXL/SOXS product page + prospectus/fact sheet (3x daily; decay disclosures) — https://www.direxion.com/product/daily-semiconductor-bull-bear-3x-etfs
- TrendForce (HBM profitability below DDR5; 2027 price surge) — https://www.trendforce.com/presscenter/news/20260602-13074.html
- MU options/IV & realized — Barchart https://www.barchart.com/stocks/quotes/MU/expected-move · OptionsAI https://tools.optionsai.com/earnings/mu · OptionSlam https://www.optionslam.com/earnings/stocks/MU
- MU consensus/guidance — AlphaStreet https://news.alphastreet.com/micron-technology-q3-2026-earnings-preview-june-24-street-expects-19-72-eps/ · Seeking Alpha https://seekingalpha.com/news/4566187-micron-signals-33_5b-q3-revenue-target-and-81-percent-gross-margin-guidance-driven-by-ai
- Refuted implied-move/realized — Investing.com https://www.investing.com/news/stock-market-news/micron-technology-stock-may-move-11-on-june-24-earnings-93CH-4747774
