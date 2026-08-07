---
type: research-brief
title: "Verifying the '$DRAM ETF / Memory is the Cheap AI Play' Thesis (Deep-Research Brief, June 2026)"
description: Fact-check + stress-test of a viral X bull thesis on memory stocks. Facts mostly true (the Roundhill Memory ETF is real; forward multiples genuinely low; HBM shortage real to 2027-28) but the core claim — multi-year contracts "took the volatility away" → premium re-rate — is unsupported and reads as a late-cycle "this time is different."
tags: [market-research, semiconductors, memory, hbm, dram, valuation, evidence]
timestamp: 2026-06-21T00:00:00Z
status: active
sources: []
---

# Verifying the "$DRAM ETF / Memory is the Cheap AI Play" Thesis — Deep-Research Brief

**Source:** Claude Code `deep-research` run `wf_0787eabd-da1` (2026-06-21). Walled at fetch on the first
pass (all-abstained, not refuted) → **resumed past the 7:30pm KST reset** → clean.
**Method:** 5 angles → 25 sources → 87 claims → 25 adversarially verified → **18 confirmed, 7 refuted →
11 findings.** ETF facts rest on primary (Roundhill issuer page + SEC EDGAR); valuations & structure on
TrendForce (primary) + Korean press + aggregators. **Evidence/education, NOT investment advice.**
**Purpose:** verify+analyze a viral X post pitching the memory complex (via the "$DRAM" ETF) as "the last
genuinely cheap corner of the AI trade," with a re-rate thesis. Companion to the
[cyclical-vs-new-era verdict](deep-research-memory-cyclical-debate-2026.md) — which it independently corroborates.

## Cross-validation (2026-06-21)
A second independent pass (4 adversarial agents) confirmed the core verdict and **refined three points toward
the bull**: (1) the **3-5yr LTA shift is real & current** (Apr 2026) and the LTAs carry **price floors + 10-30%
upfront payments** — not pure volume (the earlier "makers shortened contracts" was a *transitional* late-2025
phase); (2) **AUM best estimate ~$17.5B** (stockanalysis live NAV; ">$20B" unconfirmed); (3) the **"30/50/100×"**
comparison is **accurate for AI software/IP** (ARM ~181×, Palantir ~92×), though big infra (Nvidia ~23×, TSMC
~26-29×) is below 30×. **Bear side strengthened:** Noeddekaer's "we are not buying [no cycles]" + trim verified
verbatim; the "low-P/E-at-peak = value trap" framing and the 2018 (MU −56%) / 2022 (FY23 rev halved) peak→collapse
history confirmed. Minor: SK Hynix is the ETF's *largest* holding (~27%); MU fwd ~9-11×; SanDisk "~19×" not
corroborated (sources 11.7-33.8×). **Net: core verdict unchanged and stronger** — the structural shift is more
real than a flat "volume-not-price" framing (it *dampens* the trough) but still does not justify a *premium* re-rate.

## One-paragraph verdict
**A MIXED BAG: the concrete facts are mostly TRUE/roughly-right, but the core analytical leap — that
multi-year contracts "took the volatility away," justifying a re-rate from a cyclical to a premium
multiple — is NOT supported and reads as a textbook late-cycle "this time is different."** Cheap
multiples vs AI peers and a real HBM-driven shortage are **facts**; "the cycle is tamed → re-rate" is the
poster's **interpretation** and the weakest, most contestable link.

## Claim-by-claim (verified)

### Facts that hold (TRUE / roughly-right)
- **The "$DRAM" ETF is real:** Roundhill Memory ETF (BATS/Cboe BZX: **DRAM**), issued by Roundhill, **launched
  Apr 2 2026**, **0.65% ER**, actively managed, "first-ever" memory ETF (≥80% in HBM/DRAM/NAND/SSD). [3-0, primary+SEC]
- **Holds the named makers "in one ticker" — with a catch:** SK Hynix + Micron + Samsung + SanDisk + Kioxia/
  WDC/Seagate/Nanya/Winbond (~16 lines), **~73-75% in the top three**. BUT Korea-listed names are accessed via a
  **mix of direct foreign-ordinary shares + total-return swaps** (for RIC 25%-cap compliance); **Micron's ~27%
  is mostly synthetic** (~23.9% swap + 3.68% direct), and the #2 line by weight is actually a ~14.6% T-bill
  (swap collateral). It is **NOT leveraged** (~1:1; a 2x product is only proposed). [3-0]
- **Forward multiples genuinely low; the relative gap is real:** SK Hynix **~5.8-7.6×** fwd (it narrowly
  *overtook* Samsung's 6.77× for the first time, May 13), Samsung **<6-7×**, Micron **~9×** — vs Nvidia
  ~22-23×, TSMC ~26×. [3-0]
- **Micron facts:** revenue **~doubling** (TTM +85%); **HBM sold out through 2026**; "tripled off its lows"
  is actually an **understatement** (MU ≈ **11×** off its ~$103 low). [revenue/sold-out cross-confirmed by
  prior wiki research; ETF exposure 3-0]
- **SK Hynix HBM leadership** ("dominant," "majority of NVIDIA's HBM," "~58% share"): **TRUE per prior
  verified wiki research** (62% Q2'25 ship / 57% Q3'25 rev / 58% Q1'26; UBS ~70% of NVIDIA Rubin HBM4) —
  *not re-tested this run* (flagged a gap here, but the wiki confirms it).
- **"New fabs ~2027":** roughly right — TrendForce: meaningful capacity expansion **unlikely until late
  2027/2028**. [2-1]

### Where it exaggerates or misleads
- **"AI names at 30/50/100×":** EXAGGERATED for the chip/infra comps — **Nvidia ~22-23×, TSMC ~26×.** The
  gap is real but the AI side is overstated (only pure software, e.g. Palantir, reaches ~100×).
- **"Multiple compressed as the stock climbed":** ❌ **false for SK Hynix** (its forward P/E *expanded*
  5.28×→6.79× as the stock rose, Feb→May); **unverified for Micron**. [refuted 1-2]
- **"Moved from 1-year to multi-year contracts, taking volatility away":** MISLEADING. 3-5yr LTAs are a real
  trend, but they **lock VOLUME, not PRICE** — CSPs *accept higher prices* to secure supply (reinforcing
  pricing power). Commodity prices are still moving **+58-63% QoQ (DRAM) / +70-75% (NAND)** in 2Q26; in
  *early 2026* makers even **SHORTENED** contracts to capture hikes (opposite of the thesis). **Exception:**
  some HBM LTAs (Micron, SK Hynix-Google) embed bottom-price clauses — so the structural shift is real for
  **HBM only**, not commodity. [3-0 / a "contracts removed cyclicality" claim refuted 0-3]
- **"Shortage runs to 2030":** the **2030** figure is from **SK Hynix's chairman** (Computex, Jun 2) + a
  Kearney analysis — an *interested-party* forecast. Neutral research (**TrendForce**) horizon is **2027-2028.** [2-1]
- **AUM:** UNVERIFIABLE — sources span **~$6.5B-$17.5B**; the ">$20B" figure was **refuted** (0-3, from a
  low-reliability outlet that also got holdings wrong) and the poster's "$13.36B" is unconfirmed. Clearly
  billions, but the weakest-sourced number. (The "$0.25M seed" was launch-day only.)

### The core re-rate claim — the weakest link (bear rebuttal is stronger)
1. **A low multiple on PEAK earnings is rational, not a bargain.** SK Hynix ~6-8× *forward* vs ~26× *trailing*
   = the market pricing a sharp earnings ramp; a single-digit multiple on peak EPS is the classic late-cycle
   signature, and historically trough-low multiples at cycle peaks **precede** earnings collapses. "Cheap at
   8-12× forward" only holds **if peak earnings are sustainable** — unestablished.
2. **Cyclicality is empirically still here** (+58-75% QoQ commodity price swings).
3. **A $40B+ memory bull rejects the core claim:** Polar Capital's **Jorry Noeddekaer**: *"we are in a new
   paradigm… [but] we don't agree memory chips will never see cycles again"* — and he's been **trimming** on
   the rally. [3-0]
4. **HBM-vs-commodity conflation:** the thesis borrows HBM's structural tightness to re-rate the *whole*
   complex; commodity DRAM/NAND (most of the bits) is still sharply cyclical. **No memory maker is shown to
   have sustainably re-rated to a secular premium multiple.** [synthesis]

## Caveats
- **Time-sensitive:** forward P/Es move daily and are provider-dependent (SK Hynix ranged ~5.8× NTM to 9.46×);
  the stock re-rated hard intra-window (SK Hynix +272% YTD, ATH ₩2,891,000 Jun 19). A forward multiple on a
  cyclical at peak earnings is inherently unstable (the denominator is a contested forecast).
- **Not re-tested this run (treat via the cross-referenced wiki):** the 58% HBM share / NVIDIA-majority, and
  Micron's tripled-off-lows / revenue-doubles / sold-out specifics — corroborated by prior briefs, not by a
  surviving source in *this* batch.
- **Forecast vs fact:** TrendForce's +58-75% QoQ are *projections*; "2030" is an interested forecast; "2027"
  is when capacity *begins*, not when the shortage *ends*. The re-rate conclusion is *interpretation*.

## Open questions
1. DRAM ETF's actual current AUM (official NPORT would settle the "$13.36B").
2. What fraction of total **bits** is locked under *fixed-PRICE* multi-year LTAs vs volume-only (HBM vs
   commodity)? This decisively settles the cyclicality debate.
3. Micron-specific: did its forward multiple actually compress, and the precise off-lows magnitude.

## Feeds into the wiki
- Creates: [The "$DRAM ETF / cheap AI memory" thesis — verified & stress-tested](../market-research/memory/dram-etf-thesis-analysis.md)
- Corroborates/links: [Cyclical vs "new era" verdict](../market-research/memory/cyclical-vs-new-era.md)
  (the re-rate claim is the same dampened-not-abolished question) · [SK Hynix](../market-research/memory/sk-hynix.md)
  (HBM share, the fwd-P/E-only-if-earnings-triple crux) · [Micron FQ3-2026](../market-research/memory/micron-fq3-2026-earnings.md) ·
  [Memory supply-demand cycle](../market-research/memory/supply-demand-cycle-2026.md).

## Primary / key sources
- Roundhill Memory ETF (issuer) — https://www.roundhillinvestments.com/etf/dram/ · holdings — https://stockanalysis.com/etf/dram/holdings/ · SEC EDGAR CIK 1976517 (Form 497K)
- "Roundhill Memory ETF (DRAM)…" (Motley Fool, May 28 2026) — https://www.fool.com/investing/2026/05/28/roundhill-memory-etf-dram-micron-sandisk-dram/
- SK Hynix fwd P/E overtakes Samsung (Seoul Economic Daily, May 14 2026) — https://en.sedaily.com/news/2026/05/14/sk-hynix-forward-per-overtakes-samsung-electronics-for
- "Why are their P/Es less than half of TSMC's" (nai500, Apr 2026) — https://nai500.com/blog/2026/04/samsung-and-sk-hynix-see-profits-soar-why-are-their-p-e-ratios-less-than-half-of-tsmcs/
- TrendForce 2Q26 contract prices +58-63%/+70-75% (Mar 31 2026) — https://www.trendforce.com/presscenter/news/20260331-12995.html
- TrendForce: makers shift to short-term deals (Feb 6 2026) — https://www.trendforce.com/news/2026/02/06/news-samsung-sk-hynix-micron-reportedly-shift-to-short-term-post-settlement-deals-for-north-american-big-tech/
- TrendForce: annual→3-5yr LTAs (Apr 9 2026) — https://www.trendforce.com/news/2026/04/09/news-from-annual-deals-to-3-5-year-ltas-samsung-and-sk-hynix-reportedly-reset-big-tech-memory-contracts/
- Noeddekaer / Polar Capital (Bloomberg via Yahoo / The Edge) — memory "new paradigm" but cycles not dead
- "Every memory cycle ends the same" (UncoverAlpha) · "DRAM was the worst business in chips" (ChipLog) — bear base rate
