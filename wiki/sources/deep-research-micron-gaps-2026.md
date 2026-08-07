---
type: research-brief
title: "Micron Catalyst — Closing the Gaps (Deep-Research Follow-Up, June 2026)"
description: Follow-up verification of four open gaps from the memory-supercycle brief — MU's options-implied move & post-earnings history, Micron's (non-)stated HBM share target & HBM TAM, the 2027 commodity-glut/capacity picture, and Samsung/SK Hynix targets (unanswered). Includes a flagged MU price-data inconsistency.
tags: [market-research, semiconductors, memory, hbm, micron, options, evidence]
timestamp: 2026-06-20T00:00:00Z
status: active
sources: []
---

# Micron Catalyst — Closing the Gaps (Deep-Research Follow-Up)

**Source:** Claude Code `deep-research` run `wf_3146c387-6a2` (2026-06-20). **Hit the session-quota wall**
mid-verification (only 4/25 confirmed, synthesis failed); **resumed past the 14:40 KST reset** (`args`
re-passed) → completed clean.
**Method:** 5 angles → 22 sources → 90 claims → 25 adversarially verified → **15 confirmed, 10 refuted →
13 findings.** Topics 1–3 rest on Micron's own call transcript + IR prepared remarks (primary), TrendForce,
and options vendors (Barchart/Options AI/OptionSlam/AlphaQuery). **Topic 4 returned no verified claims.**
**Purpose:** resolve the four gaps left open by the [first memory brief](deep-research-memory-cycle-micron-2026.md).

## ⚠️ Data-integrity flag — MU absolute price is inconsistent across vendors
The run surfaced **conflicting MU price levels**: **~$126** (TipRanks implied-$ math), **~$444** (Options AI,
the *Mar 18 2026* post-earnings close), and **~$1,134** (stockanalysis, used by the first brief for the
"Jun 18 close / +756% YoY"). This indicates **stale vendor pages and/or a stock-split/scaling artifact.**
**Percentage-based findings are unaffected**, but the **absolute** levels in the first brief (the ~$1,134,
the +756%, and "BofA $950 already exceeded") should be **reconciled against a primary real-time quote** —
e.g. pull MU directly from the `alpaca-data` lake — before relying on them. Flagged, not silently kept.

## Topic 1 — Options-implied move & post-earnings history
- **IV is extremely elevated → large IV-crush setup:** IV **~103.3%**, IV-Rank **94.8**, IV-Pctl **97**
  (Barchart, Jun 18; AlphaQuery ~103.5% corroborates). *Market data, time-sensitive.* [3-0]
- **The precise ATM-straddle implied move could NOT be pinned** — vendors conflicted and most were refuted:
  **~7.5%** (TipRanks, 0-3), **~11%** (Investing.com, 1-2), **~14.3% weekly / ~23% monthly** (OptionsLam,
  1-2 / 0-3). **Treat the "~11%" headline as unconfirmed** — do not "correct" it to another single number.
- **Solid:** MU's **average *actual* one-day post-earnings move ≈ 6.5%** (20 qtrs, Options AI; OptionSlam
  ~6.0% mean corroborates) [2-1]; **last 4 quarters ≈ 4.5% abs** — **−3.8% Mar'26 *despite a ~33% EPS beat*,
  +10.2% Dec'25, −2.8% Sep'25, −1.0% Jun'25** [3-0]. ⇒ **The implied move embeds a clear volatility-risk
  premium, and reactions have been muted/mixed even on big beats** — reinforcing the sell-the-news thesis.

## Topic 2 — Micron's HBM share target & HBM trajectory
- **Management *explicitly declined* a numerical HBM share target** (CEO Mehrotra, Q1-FY26 call: "we are not
  really going to be specifying… the share… we will be managing the mix between HBM as well as our non-HBM").
  The widely-cited **"~25% / DRAM-equivalent" is an analyst extrapolation, NOT Micron guidance** (he noted
  HBM share was *in line with* its ~20–25% DRAM share in CQ3-25 — backward-looking). [2-1]
- **What Micron *did* guide (its own number):** **HBM TAM ~40% CAGR, ~$35B (2025) → ~$100B (2028)** — the
  $100B milestone pulled **two years earlier** than its prior outlook. This is *industry TAM*, not
  Micron-specific revenue. [3-0]
- **The "$8B run-rate" is confirmed NOT a management figure** — FQ2-26 prepared remarks contain **no HBM $
  run-rate, no HBM share % target, no HBM $ TAM** (purely qualitative). [2-0]
- **CY2026 HBM sold out** — price *and* volume agreements concluded (incl. **HBM4**); **HBM4 36GB 12H in
  volume shipment for NVIDIA Vera Rubin**; Micron meets only **~50–66%** of key-customer HBM demand.
  **No equivalent 2027 sold-out commitment stated.** (A "~90% of 2026 HBM3E pricing locked" claim was
  refuted 0-3.) [3-0]

## Topic 3 — 2027 commodity-glut probability & quantified capacity
- **2026 capex restrained & tech-directed (bull case):** industry **DRAM capex $53.7B → $61.3B (+14%)**,
  NAND **$21.1B → $22.2B (+5%)**; by company (DRAM, TrendForce est.): **SK Hynix $20.5B (+17%) / Samsung
  $20B (+11%) / Micron $13.5B (+23%)**. Spend targets **process upgrades, hybrid bonding & HBM — not new
  capacity** → **2026 bit-supply growth stays limited** (DRAM ~12% *undersupplied*). [3-0 totals / 2-1 split]
  *(TrendForce forecasts, not company-confirmed. Micron's total-company capex is larger — >$25B FY26 incl.
  construction — figures differ by basis; a "$18B→$20B raise" claim was refuted 1-2.)*
- **Tightness extends beyond 2026 (management + sell-side):** Micron guides **both DRAM and NAND** tight
  beyond CY26 (CY26 industry bit *demand* constrained by *supply*; DRAM bits +low-20s%, NAND ~+20%); even
  cautious **Morgan Stanley raised 2027 MU EPS ~48%**, **UBS** sees DRAM tight to ~Q2-2028, NAND to ~Q4-2027.
  [3-0] *(Self-interested forecast — and commodity DRAM/NAND is exactly the contested segment.)*
- **The bear's documented swing factor is China:** **CXMT** scaling DRAM wafers (~200k → 300k/mo in 2026;
  UBS est. +120–140k China wafers/mo), now **#4 DRAM maker (~7.6%)** — an *additive 2027* supply risk, not
  2026. **HBM is expected to stay tight regardless.** [3-0]
- **Net (medium confidence):** bull = restrained capex + sold-out HBM + tight-beyond-2026 guidance + sell-side
  agreement; bear = Chinese commodity-DRAM capacity in 2027. *Still unquantified:* an explicit 2027
  bit-supply-vs-demand balance and 2027 (not 2026) capacity numbers.

## Topic 4 — Samsung & SK Hynix targets (UNANSWERED)
**No Samsung/SK Hynix price-target, rating, or consensus claim survived 3-vote verification** — do **not**
assert numbers here. **Unconfirmed leads** (sources real, claims not verified): Samsung target raised to
**₩490,000** (Sedaily, May 21) and a "bold **₩850,000**" Street target (Sedaily, Jun 1); **Morgan Stanley
bumped SK Hynix** ("undervalued as HBM pricing tightens", Investing.com). **Needs a dedicated re-run**
focused on the Korean names (Korean-source verification was the weak spot).

## What got refuted (do NOT cite)
- MU implied move **~7.5%** (TipRanks, 0-3) · **~14.3% wk / ~23% mo** (OptionsLam, 1-2 / 0-3) · the **~11%**
  Bloomberg figure (1-2, *unconfirmed*).
- "OptionsLam mean post-earnings move 10.88%" (0-3); an 8-quarter actual-move series incl. "+23.8% / −13.8%" (0-3).
- Micron **"~21% HBM share, targets ~25%"** (0-3 — not Micron-stated) · **"~90% of 2026 HBM3E pricing locked"** (0-3).
- Micron **"FY26 capex $18B→$20B"** (1-2 — basis-dependent).

## Caveats
- **Forecast vs fact:** the HBM TAM ($100B/2028), "tight beyond 2026," capex growth, and company splits are
  **forecasts** (Micron mgmt / TrendForce). The earnings **date**, "HBM **sold out** 2026," and "management
  **declined** a share target" are **facts** about what was contracted/said. Options figures are a **Jun-18–20
  snapshot.**
- **Topic 4 is a genuine gap** (zero verified claims). **The MU absolute-price inconsistency** (see top) is
  unresolved.

## Open questions
1. **Samsung & SK Hynix** current targets/ratings/consensus + 2026 changes (dedicated re-run; Korean sources).
2. The **precise current ATM-straddle implied move** for MU from one authoritative, reconcilable source.
3. The explicit **2027 bit-supply-vs-demand balance** + 2027 (not 2026) capex/wafer numbers for the Big-Three,
   CXMT and YMTC; an explicit Morgan Stanley cycle-top/correction call.
4. **Reconcile the MU price** (~$126 / ~$444 / ~$1,134) — split / scaling artifact / stale data? (Use the lake.)

## Feeds into the wiki
- Updates: [Micron FQ3-2026 earnings note](../market-research/memory/micron-fq3-2026-earnings.md)
  (options/IV + HBM target + price flag) · [Memory supply-demand cycle](../market-research/memory/supply-demand-cycle-2026.md)
  (capex + tight-beyond-2026 + China swing factor).
- Builds on the [first memory brief](deep-research-memory-cycle-micron-2026.md).

## Primary / key sources
- Micron Q1-FY2026 earnings call transcript (Dec 17, 2025) — https://www.fool.com/earnings/call-transcripts/2025/12/17/micron-mu-q1-2026-earnings-call-transcript/
- Micron FQ2-2026 prepared remarks (IR, Mar 18, 2026) — https://investors.micron.com/static-files/e089f8c0-065d-47b8-9d02-bfa863cdb357
- "Micron forecasts $100B HBM market by 2028…" (Seeking Alpha) — https://seekingalpha.com/news/4532757-micron-forecasts-100b-hbm-market-by-2028-as-supply-tightness-persists-through-2026
- TrendForce, "2026 memory capex" (Nov 13, 2025) — https://www.trendforce.com/presscenter/news/20251113-12780.html
- MU options/IV — Barchart https://www.barchart.com/stocks/quotes/MU/expected-move · Options AI https://tools.optionsai.com/earnings/mu
- Unverified (Topic 4): Sedaily ₩490k / ₩850k Samsung; Investing.com "MS bumps SK Hynix target"
