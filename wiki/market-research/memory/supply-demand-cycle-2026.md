---
type: overview
title: Memory Supply-Demand Cycle — DRAM, NAND & HBM (mid-2026)
description: The state of the memory market as of mid-2026 — a strong, HBM-led "supercycle," steep but decelerating commodity prices, HBM crowding out commodity DRAM, and pricing forecasts through end-2027 (bull tightness vs bear commodity glut).
tags: [market-research, semiconductors, memory, hbm, dram, nand]
timestamp: 2026-06-29T00:00:00Z
status: active
sources: [../../sources/deep-research-memory-cycle-micron-2026.md, ../../sources/deep-research-micron-gaps-2026.md, ../../sources/deep-research-micron-h2-2026-navigation-2026.md]
---

# Memory Supply-Demand Cycle — DRAM, NAND & HBM (mid-2026)

> **As of 2026-06-20. Time-sensitive.** Most price figures below are **forecasts** (TrendForce/BofA),
> not realized facts — flagged inline. See the [research brief](../../sources/deep-research-memory-cycle-micron-2026.md)
> for the full verification (19/25 claims confirmed) and the refuted figures not to cite.

The memory market is in a **strong, AI/HBM-led up-cycle** that TrendForce and BofA characterize as a
**"supercycle."** The defining feature of *this* cycle is the **bifurcation** between **HBM** (high-
bandwidth memory — tight, AI-driven, premium-priced, sold out) and **commodity DRAM/NAND** (more
cyclical, but currently dragged up by capacity reallocation toward HBM). This is the live extension of
the [semiconductors](../../shared/instruments/semiconductors.md) regime — in April 2026, memory/HBM
(Micron +55% in a month) was already among the leadership that broadened off NVDA.

## Where we are in the cycle (mid/strong up-cycle)
- **Commodity prices steep but decelerating (forecast).** 2Q26 conventional **DRAM contract +58–63%
  QoQ**, **NAND +70–75% QoQ** (TrendForce, 31 Mar 2026) — but *down* from 1Q26's record ~90–95% QoQ.
  Levels are high and rising; the *rate* of increase has peaked. PC DRAM is relatively soft — the
  driver is **AI server + capacity reallocation**, not every segment uniformly.
- **HBM sold out for 2026** — confirmed by *primary* company statements (SK Hynix CFO: entire 2026 HBM
  supply sold out; Micron: HBM fully sold out through end-2026).
- **"Supercycle" framing.** BofA: 2026 HBM market **$54.6B (+58% YoY)**, "a supercycle similar to the
  boom of the 1990s" (forecast; recurs across outlets — originally via SK Hynix's vendor-interested
  newsroom).

> **⚠️ Not to be confused (2026-07-13).** A *separately circulated* "BofA Global Memory" report claiming
> **$891.8B combined 2026 memory / DRAM +325% to $568.8B / HBM TAM $76.8B / "memory indicator 183"** was
> fact-checked and is a **garble** — the headline **traces to no primary BofA note** (most likely a total-
> semiconductor TAM, ~$1.3T, mislabeled as the memory market), and its HBM $76.8B runs *well above* both the
> real BofA **$54.6B** framing above and Micron's implied ~$49B. The **credible core survives** (HBM 3:1
> cannibalization, DDR4 shortage, +80–95% QoQ 1Q26 pricing — see below); the **full-year DRAM total does
> not** (real consensus ≈ Gartner's ~3× "memflation" to **$633B**, with the error concentrated in one
> overstated DRAM number). → [BofA report — verified & reconciled](bofa-memory-report-verified-2026-07-13.md).

> **🔄 Updated 2026-06-24 (H2-2026 [navigation run](../../sources/deep-research-micron-h2-2026-navigation-2026.md)).**
> TrendForce's **Jun-22** release confirms the trajectory held: prices **"continue rising in 3Q26"** — NAND still
> **accelerating** (+70–75% QoQ 2Q), even legacy **DDR2 +55–60% (2Q) → +35–40% (3Q26)** on the supply cascade. New
> supply-side anchors: **Goldman 2026 DRAM supply gap 4.9%** (worst in 15 yrs; NAND 4.2%, HBM 5.1%) **widening to
> ~5.9% in 2027**; inventories **2–4 weeks vs 15–31 at prior cycle peaks**; CY2026 memory fully locked under LTAs
> incl. a new **Anthropic** deal (2–3yr visibility). The cycle-ender (new-fab output, CXMT) is dated **late
> 2027/2028** — see the H2-2026 navigation playbook for the hold-vs-exit dashboard.

## The structural story: HBM crowds out commodity DRAM
HBM consumes **~3–4× the wafer area per GB** of standard DRAM, so allocating wafers to HBM removes a
disproportionate share of *commodity* bit-supply. TrendForce (2 Jun 2026), top-three suppliers:

| Metric (top-3 blended) | end-2025 | end-2026 | end-2027 |
|---|---|---|---|
| HBM as % of DRAM **wafer** input | ~18% | ~22% | ~30% |
| HBM as % of DRAM **bit** supply | ~8% | ~9% | ~13% |

*(SK Hynix individually runs higher — ~30% rising to ~40% wafer by 2027.)* This is the mechanism that
keeps **commodity DRAM tight even as commodity demand (PCs/phones) is mild** — supply is being eaten by
HBM. *(Forecasts. A competing "~25% of wafers in 2026" figure was refuted — use these.)*

## Supply structure & discipline
- **Disciplined oligopoly:** Micron + Samsung + SK Hynix ≈ **90% of DRAM** (Q1'26 revenue share:
  Samsung 38.6% / SK Hynix 28.8% / Micron 22.4% = 89.8%).
- **Demand locked in:** North-American CSPs accelerating AI **inference** and signing **3–5yr LTAs** at
  higher prices → supplier pricing power; ~20–30% of DDR bits projected LTA-locked by 2027.
- **The wildcard:** China's **CXMT** is now the #4 DRAM player (~7.5% share, capacity tripled to
  ~290K wafers/month). On a *capacity* basis (vs revenue) the Big Three sit a touch below 90% — and
  CXMT/YMTC are the core **commodity-glut** risk into 2027–2028.

## HBM market-share is volatile (don't anchor on one quarter)
Q2'25: SK Hynix 62% / Micron 21% / Samsung 17% (Micron briefly overtook Samsung). In **Q3'25**, SK Hynix
held **~57% (revenue), Samsung ~22%, Micron ~21%** (Counterpoint). *(Corrected 2026-06-21: an earlier
"Samsung 35% / Micron 11% / SK Hynix 53%" figure was contradicted by independent verification — use the
Counterpoint split.)* Treat any single-quarter HBM ranking as a snapshot; the HBM4 cycle (negotiations
opened 2Q26) will reset it again.

## Long-term pricing to end-2027
- **HBM:** forecast to **"surge multiples higher" in 2027** (TrendForce) on the HBM4 cycle + crowding-
  out. The *multiple is not quantified* by TrendForce — the "double" in secondary coverage is editorial.
- **Commodity DRAM/NAND:** shortages expected to **ease by 2027–2028**, but pricing **stays elevated
  through end-2027** on sustained AI demand + rising capital intensity (Gartner: "high through to end of
  2027"); some see the rally running **past 2028** (Samsung/SK Hynix cautious on expansion).
- **Bull vs bear:**
  - **Bull** — sustained HBM-driven tightness; LTAs + discipline hold; rally extends past 2028.
  - **Bear** — a **commodity-DRAM glut** as Big-Three + China (CXMT/YMTC) capacity arrives late-2027/28.
  - **Critical distinction:** any 2027 oversupply concentrates in **commodity DRAM** — **HBM is expected
    to stay tight** regardless. The two should be modelled separately.
  - → For the full bull-vs-bear adjudication, see the [cyclical vs "new era" verdict](cyclical-vs-new-era.md)
    (dampened & elongated, not abolished — and HBM margins currently run *below* commodity DRAM).

## Supply discipline & the 2027-glut question (follow-up research, 2026-06-20)
A second deep-research run ([gaps brief](../../sources/deep-research-micron-gaps-2026.md), `wf_3146c387-6a2`)
quantified the supply side:
- **2026 capex is restrained and tech-directed.** Industry **DRAM capex $53.7B → $61.3B (+14%)**; NAND
  **$21.1B → $22.2B (+5%)**. By company (DRAM, TrendForce est.): **SK Hynix $20.5B (+17%)**, **Samsung
  $20B (+11%)**, **Micron $13.5B (+23%)**. Crucially, TrendForce says the spend goes to **process upgrades,
  hybrid bonding, and HBM — *not* new capacity** — so **2026 bit-supply growth stays limited** (DRAM ~12%
  *undersupplied*). *(Forecasts, not company-confirmed; Micron's total-company capex is larger, >$25B FY26
  incl. construction — figures differ by basis.)*
- **Management guides tight *beyond* 2026.** Micron expects **both DRAM and NAND** to "remain tight beyond
  calendar 2026," with CY26 industry bit *demand* constrained by *supply* (DRAM bits +low-20s%, NAND ~+20%).
  Sell-side concurs into 2027: even cautious **Morgan Stanley raised 2027 MU EPS ~48%**; **UBS** sees DRAM
  tight to ~Q2-2028, NAND to ~Q4-2027. *(Self-interested forecast.)*
- **The bear's swing factor is China.** The documented 2027 glut risk is **CXMT** scaling DRAM wafers
  (~200k → 300k/mo in 2026; UBS est. +120–140k China wafers/mo), now the **#4 DRAM maker (~7.6%)** — an
  *additive 2027* supply risk, not 2026.
- **Net:** **HBM stays tight either way; the contested segment is commodity DRAM/NAND**, and the swing
  variable is Chinese capacity. *Still unquantified:* an explicit 2027 bit-supply-vs-demand balance and 2027
  (not 2026) capacity numbers — flagged open.

> **🔄 Updated 2026-06-29 — CXMT, from the SemiAnalysis primary note** ("China's CXMT Is Set to Challenge DRAM
> Incumbents," fetched directly; see the [week-ahead brief](../../sources/deep-research-semis-memory-week-ahead-2026-06-29.md)).
> This **partly softens** the China-glut bear leg for the near term and **quantifies** the prior open items:
> - **Capacity roadmap (primary):** CXMT ~**265 kwspm (2025) → ~350 (2026, ≈ Micron's ~385) → ~420 (2027, ~17% of
>   global capacity) → ~500 kwspm (2028)**. **Bit-supply share ~9% (2025) → ~12% (2027)** — a **~3-point gain** in a
>   ~$1T market. *(Supersedes the older "~7.5% / ~290K wafers" estimate above — same direction, firmer numbers; CXMT
>   is unambiguously the #4 maker.)*
> - **Not a price-war (yet):** in 1Q26 CXMT's **DRAM ASP was only 5-10% below** Samsung/SK Hynix/Micron while its
>   **cost-per-bit runs >30% higher** — so it is **riding the shortage, not dumping** (1Q26 earnings came from **ASP
>   +~57%**, bits only +11%). **HBM ≈ 1% of revenue** (negligible; yield/HBM hurdles cap disruption).
> - **No near-term glut:** SemiAnalysis expects **DRAM undersupplied through ~2028** (high-single-digit % in 2026 →
>   low-to-mid-teens in 2027), with **pricing on track to double again in 2026**, and judges **CXMT supply concerns
>   "overplayed at least for the next two years."**
> - **So:** the documented oversupply risk is pushed to **2028+**, not 2027 — the [cyclical-vs-new-era verdict](cyclical-vs-new-era.md)
>   (dampened, not abolished) is unchanged, but the *timing* of the commodity-glut tail is later than the bear case implied.

> **🔄 Updated 2026-07-16 — CXMT priced its STAR-Market IPO; the roadmap above is now *funded*.**
> Priced ¥8.66/sh (Jul-14), subscription Jul-16; **~¥579B ≈ $81B valuation**, earmarked ¥29.5B but priced
> to raise **~$8–10B** (the SMIC-2020 over-raise pattern; matches/tops SMIC's ¥53.2B STAR record); H1'26
> net profit guided **>¥50B** (~25×), i.e. priced at ~6× annualized *peak* earnings. What changes: the
> **265→350→420→500 kwspm expansion moves from state-drip-contingent to publicly funded** (~$8–10B ≈
> 50–70K wspm of new capacity) → the **late-2027/28 commodity-glut leg rises in probability, timing
> unchanged**; nothing reaches 2026 supply (18–30mo tools-to-bits). **HBM untouched** (~1% of revenue;
> HBM3-in-2026 serves the export-barred domestic market, not NVDA/AMD sockets). Tape effect: **MU −8–9%
> Jul-15** (≈$85–90B of cap, more than CXMT's whole valuation) — mostly positioning; displacement economics
> land on Samsung/SK-Hynix commodity books first. **Watch item added: China-supply acceleration** (bit
> output vs roadmap, Western qualification wins, tool orders). Full analysis →
> [CXMT IPO & Micron implications](cxmt-ipo-micron-implications-2026-07-16.md).

## So what (for the trader)
- The memory names are **high-beta, deeply cyclical** ([semiconductors](../../shared/instruments/semiconductors.md))
  — the up-cycle is real and HBM-backed, but the *price momentum* is decelerating and the chart is
  stretched (see the [Micron earnings note](micron-fq3-2026-earnings.md) and the [SK Hynix note](sk-hynix.md)).
  What that deceleration means for the *stocks* — cyclicals top on the **second derivative**, during the
  deceleration phase, before levels or earnings peak — is now a concept page:
  [trading the second derivative](../../shared/concepts/second-derivative-cycle-trading.md); the Jul-6
  levels-vs-rates adjudication
  reconciles the dueling bull ("HBM triples") and bear ("rapid deceleration") ASP charts — same forecast,
  two derivatives.
- **Watch for the turn** (the bear tell): commodity-DRAM contract prices flattening/declining, CXMT/YMTC
  bit-output surprises, Big-Three capex/expansion announcements, HBM4 pricing coming in soft. A
  commodity roll-over can hit the stocks even while HBM stays sold out — the [regime-detection](../../ml-stats/concepts/regime-detection.md)
  discipline applies.

## Open questions
- Quantified 2027 supply-demand balance (Big-Three + CXMT/YMTC bit growth vs HBM crowding-out).
- Sell-side pricing-trajectory targets for Samsung & SK Hynix (not just Micron).
- Realized 2Q26 prints vs the TrendForce forecasts above (update when 2Q26 closes).

## Sources
- [Deep-research brief: the memory supercycle & the Micron catalyst (2026)](../../sources/deep-research-memory-cycle-micron-2026.md)
  — TrendForce (primary), BofA via SK Hynix newsroom, Omdia/Counterpoint shares, Gartner.
- [Deep-research follow-up: closing the gaps (2026)](../../sources/deep-research-micron-gaps-2026.md)
  — 2026 capex by company (TrendForce), Micron "tight beyond 2026" guidance, the China/CXMT 2027 swing factor.
