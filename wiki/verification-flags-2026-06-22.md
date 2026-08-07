---
type: audit
title: Verification Audit — Points to Be Aware Of (2026-06-22)
description: Adversarial fact-check of the load-bearing claims across the whole wiki; flags corrections, weak provenance, and stale figures. Does not edit the underlying research.
tags: [audit, lint, market-research, systematic-trading, derivatives, ml-stats]
timestamp: 2026-06-22T00:00:00Z
status: active
sources: []
---

# Verification Audit — Points to Be Aware Of

**As of 2026-06-22.** This is a standalone audit, not a knowledge page. It records the result of a
multi-agent verification run over the wiki and **flags points to be aware of**. It deliberately does
**not** edit any existing research text — every page below is left as written; this page is the
"read me first" caveat sheet.

## Method & scope

A dynamic workflow extracted the **most load-bearing, externally-checkable claims** from every
research page (8 content clusters) and spawned one **adversarial web-verifier per claim** (instructed
to *refute* before accepting, using primary/authoritative sources). **71 claims** were checked.

| Verdict | Count | Meaning |
|---|---|---|
| **CONFIRMED** | ~36 | Matches primary sources; no action needed. |
| **PARTIALLY-CORRECT** | ~34 | Core is right but a figure, label, citation, or framing needs a caveat. |
| **REFUTED** | 0 | — |
| **STALE / UNVERIFIABLE** | 0 | (Some *sub-claims* are stale/unverifiable — captured below.) |
| **Not checked this run** | 1 | One verifier died on a credit error (see §5). |

**Headline:** the wiki is in good shape. No claim was outright false, **no cited paper was
fabricated**, and the major theses (memory cycle is dampened-not-abolished; momentum is the only
serious swing edge; VRP is real but a crash-risk premium; most active traders lose to costs) all
survived. The issues are **precision, provenance, and staleness**, concentrated in two places:
(a) academic citations where the *finding* is right but the *bibliographic detail* is off, and
(b) market figures attributed to banks that actually trace to vendor/Korean-press relays.

---

## 1. Material corrections — worth fixing in the source pages

These are real errors (wrong figure, wrong label, wrong/garbled citation, or an inverted claim).
The underlying point usually still stands; the specific statement does not.

1. **Day-trader citation is wrong on year *and* journal.**
   `sources/deep-research-long-term-profitability.md` (and [who-wins-empirical-record](shared/concepts/who-wins-empirical-record.md))
   cites "**Barber, Lee, Liu & Odean (2014, RFS)**, Taiwan 1995–99" for *all three* stats. Reality: the
   ">80% of day traders lose / +62 bp-per-day buy-minus-sell" figures are from the working paper
   *"Do Individual Day Traders Make Money?"* (Taiwan 1995–99); the **~1% persistently-skilled** figure
   is from *"The Cross-Section of Speculator Skill,"* **J. Financial Markets vol. 18 (2014)**, Taiwan
   **1992–2006** — *not* RFS. (The RFS 2009 BLLO paper is a different one, on aggregate losses.)
   Stats are all real; **split the citation and fix the journal/year**.

2. **Chen-Velikov net-anomaly figure is stale.** `sources/deep-research-swing-trading.md` cites
   **~8 bps/month** (the 2020 working paper, 120 anomalies). The published **JFQA 2023** version
   (204 anomalies) revised it down to **~4 bps/month** — which makes the skeptical conclusion
   *stronger*, not weaker.

3. **Li et al. (FAJ 2019) cost figures are mislabeled + a magnitude error.**
   `sources/deep-research-semi-rally-winners.md`: the **61–76 bps/yr** figures are
   **income/dividend strategies**, not "low-turnover conviction" strategies. The paper's genuinely
   low-turnover strategies cost **2–7 bps/yr**. Also, momentum (200–270 bps) vs those is a **~3–4×**
   gap, **not "1–2 orders of magnitude"** (that would be 10–100×).

4. **Daniel-Moskowitz crash betas are overstated.** [regime-detection](ml-stats/concepts/regime-detection.md):
   the **+232% (1932) / +163% (2009)** loser-decile returns are correct, but the
   **"loser beta >3 / winner <0.5"** thresholds are not in the paper — reported loser up-market beta
   in panic states is **~2.16**, winner leg **near-zero/slightly negative**. Directional story holds;
   the specific thresholds don't.

5. **The Harvey "concession" is inverted.** [factor-premia-and-alpha-decay](shared/concepts/factor-premia-and-alpha-decay.md)
   says factor-zoo skeptic Campbell Harvey "conceded *the results replicate*." He used that phrase only
   to confirm he could **re-run JKP's code** — he then rejected their 50%-true-prior and announced a
   counter-paper, *"Yes, There is Replication Crisis in Finance."* The JKP figures themselves (82.4%
   global, 13 themes, 93 countries, J. Finance 2023) are **correct**; the Harvey framing should be
   removed or reversed.

6. **"MU ~+762% TTM" on the sector page is a conflation.** [semiconductors](shared/instruments/semiconductors.md):
   **762.7% is Micron's TTM *EPS growth*, not its stock return.** MU's actual stock TTM return as of
   end-April 2026 was ~**+572% to +756%** depending on base date. (Note: the **micron-fq3** page's
   separate "~+756% as of Jun-18" figure *is* confirmed — see §3.)

7. **DRAM-ETF AUM: the ">$20B refuted" call is itself wrong.**
   [dram-etf-thesis-analysis](market-research/memory/dram-etf-thesis-analysis.md): **both are true** —
   NAV-based AUM **~$17.5B** (stockanalysis.com) *and* market-cap-based **~$20.67B** (TradingView,
   Jun 18). They measure different things; ">$20B" should not be marked refuted.

8. **DRAM-ETF "≥80% in HBM/DRAM/NAND/SSD" is unsupported.**
   `sources/deep-research-dram-etf-thesis-2026.md`: the prospectus rule is a **company-level test**
   (constituents derive **≥50% of revenue/profit** from memory), **not** a fund-level 80% allocation
   mandate. Launch facts (Apr 2 2026, Cboe BZX, 0.65% ER, active, "first-ever") all confirmed.

9. **HBM "contract prices shifting to YoY decline" (Q1 2026) is a superseded forecast.**
   [cyclical-vs-new-era](market-research/memory/cyclical-vs-new-era.md): the
   **DDR5 64GB RDIMM > HBM3e in per-wafer revenue *and* profitability** part is **confirmed actual**
   (TrendForce Jun 2 2026). But "HBM in YoY price decline" was a **Oct-2025 forecast TrendForce
   revised away** in Dec 2025 (slight YoY *increase*; HBM3e priced ~20% higher for 2026; ~flat YoY by
   Apr 2026). Flag it as a superseded forecast, not a Q1-2026 reality.

10. **"$8B HBM run-rate is NOT a management figure" — false.**
    `sources/deep-research-micron-gaps-2026.md`: Micron **management itself** used the
    "*annualized run rate of nearly $8 billion*" language in **FQ4-2025 prepared remarks**
    (backward-looking from ~$2B quarterly). It's a management figure, just not from the Q1-FY26 call.
    (The HBM TAM $35B→$100B/40% CAGR and the declined share target are both confirmed.)

11. **Han-Zhou-Zhu stop-loss: figure + framing.** `sources/deep-research-stop-loss-optimization-2026.md`:
    the **−49.79%→−11.36%** worst-loss and 1926–2013 period are confirmed, but the **EW Sharpe at the
    10% stop in the *published* paper is 0.165→0.504** (the "~0.17→0.37" is the earlier CICF draft).
    Also, the paper **does** argue net-of-cost survival (break-even costs 3.18–4.82%); the wiki's
    "refuted 0-3" refers to **external replication attempts**, not the paper's own claim — make that
    distinction explicit.

---

## 2. Provenance caveats — claims that stand, but on weaker sourcing than stated

The figures are plausible/uncontradicted, but the **attribution** is softer than the wiki implies.
Pattern to watch: **bank-attributed memory figures (BofA/UBS/Goldman) repeatedly trace to a vendor
newsroom or Korean press, not a citable primary note.**

12. **BofA "2026 HBM $54.6B / +58% / 1990s-supercycle"** — only public path is **SK Hynix's own
    newsroom**, and BofA named SK Hynix its "Top Pick" in the same note (conflict). The note is
    paywalled. Magnitude is corroborated (Yole ~$60B). *(memory-cycle & sk-hynix briefs)*

13. **"Per UBS, ~70% of NVIDIA Rubin HBM4 to SK Hynix"** — **UBS attribution unverified**; the figure
    traces to **Yonhap / Korean media (Jan 2026)**. The well-sourced figure is TrendForce's "**about
    two-thirds**" (Jan 28 2026). *(sk-hynix & dram-etf briefs — replace "per UBS" with the Korean-press
    attribution or flag as unconfirmed.)*

14. **Goldman ">50% HBM share through 2026"** ([sk-hynix](market-research/memory/sk-hynix.md)) —
    appears only on **SK Hynix's PR page** with no citable GS note; a parallel mid-2025 GS note actually
    *warned* about HBM-dominance risk. The Counterpoint quarterly shares (62%/57%/58%) it sits next to
    are solidly sourced.

15. **SK Securities ₩4.0M target "(~10× fwd P/E)"** — the **10.2× is Micron's** peer P/E cited for
    comparison, **not** SK Hynix's target multiple (SK Hynix's own fwd P/E is ~6.2×). The ₩4.0M target
    is **structural/LTA-based**, not P/E-derived. All the broker targets/dates themselves are confirmed.
    *(sk-hynix brief)*

16. **Noeddekaer (Polar Capital) quote & AUM.** `sources/deep-research-dram-etf-thesis-2026.md`:
    the quote is a **paraphrase, not verbatim**; the **$40B+ is Polar Capital's firm-wide AUM**, not his
    book (his funds are ~$227M); the **"trimming on the rally"** detail appears only in secondary
    aggregators, not the primary Bloomberg piece. His actual stance ("new paradigm, but not the end of
    cycles") is accurately represented.

17. **"HBM shortage to 2030."** [dram-etf-thesis-analysis](market-research/memory/dram-etf-thesis-analysis.md):
    the **SK chair's 2030 remark (Computex, Jun 2 2026) is confirmed but is an interested party**; the
    **Kearney 2030** leg is only a **Wikipedia secondary** (no primary found); and **TrendForce never
    names a "2027–2028" end-date** — soften to "tightness through ≥2027, relief possibly 2028."

18. **April-2026 LTA shift (3–5yr, 10–30% upfront, price floors).** Same page: corroborated by
    TrendForce (Apr 9 / May 4 2026) but terms are **attributed mainly to SK Hynix** (Samsung's still
    under negotiation), and the **Feb-6 TrendForce piece is *not* "the opposite"** — it described a
    different, transitional seller-favorable mechanism. All sourcing is journalist/Korean-press;
    neither maker has publicly confirmed terms.

---

## 3. Minor / precision notes (low priority)

- **CME FedWatch buckets transposed.** `sources/deep-research-week-ahead-2026-06-22.md`: it's
  **~33–34% for a 25bp hike / ~36% for 50bp** (wiki has them swapped); no-change **~11%, not ~14%**.
  The StockTitan "~77% hike by Dec (from ~24%)" and the whole hawkish direction are confirmed.
- **April headline PCE was 3.8% YoY, not ~4.0%** (same brief). ~4.0% is the *May* consensus
  (Jun-25 release). April **core** PCE 3.3% is correct.
- **Broadcom after-hours drop ~12%** (most-cited) rather than ~14%, and the **$100B target is
  FY2027-specific and was *reiterated*, not raised**. Core AVGO figures ($10.8B AI / $22.2B / $2.44)
  all confirmed. *(memory-cycle brief; the micron-fq3 page's "~14%" was judged a reasonable
  approximation.)*
- **NAND "deceleration" framing.** memory-cycle brief: the record **~90–95% QoQ applies to DRAM
  only** in 1Q26; NAND actually **accelerated** (~55–60% → 70–75%). 2Q26 figures themselves correct.
- **CXMT "~200k→300k/mo" ramp is stale** + **"UBS +120–140k" unverified.** micron-gaps brief:
  CXMT was already at **~240–290k/mo by end-2025**, so 2026 is more plateau than 50% jump; it's already
  a live #4 (~7.6%), so the "2027-not-2026 risk" applies to *new incremental* capacity.
- **MU FQ3 revenue consensus "$34.52B"** is the AlphaStreet figure (low end); others show
  **$34.66–35.56B**. EPS $19.72 and "above guidance" are correct. Consensus varies by aggregator/date.
- **Fama-French (2010) net alpha "−0.81% to −1.00%"** — the **−1.00% end is unsupported**; the figure
  is **~−0.8%/yr**. Bootstrap "~90%" applies to funds **≤~95th pct**, not the 90th specifically.
- **McLean-Pontiff framing** (swing brief & [factor-premia](shared/concepts/factor-premia-and-alpha-decay.md)):
  the **58% (raw mean) and 35% (regression) are different methodologies, not "raw vs net-of-bias,"**
  and the **~10% is pre-publication OOS decay**, not "share of in-sample returns from data-mining."
  All numbers real; the relationship between them is mischaracterized. (Paper covers **97** anomalies.)
- **Cici "~30% of managers disposition-prone"** (losing-position brief) — not pinpointable; the paper
  says "a substantial fraction," secondary sources give a **22–55%** range.
- **Sinclair *Volatility Trading*** ([source page](sources/sinclair-volatility-trading.md)) — **224
  pages**, not "~220." Publisher/year/ISBN all correct.
- **TrendForce wafer/bit HBM shares** (18/22/30% & 8/9/13%) are confirmed to the **Jun 2 2026**
  release, but the **"3–4× wafer area per GB" sub-fact comes from separate TrendForce/industry
  sources**, not that release — cite it separately.

---

## 4. Time-sensitivity (the market-research pages will go stale fast)

- **Micron FQ3-2026 prints Wed Jun 24 (AMC) — still pending as of this audit.** Every "beat/miss/
  reaction" framing is forward-looking; the post-mortem stubs are still empty. Consensus figures
  already drift by aggregator and by day.
- **All prices, P/Es, AUMs, market caps, and analyst targets are mid-June-2026 snapshots.** Several
  are already moving (e.g. BofA's MU target may have gone $950→$900 by Jun 10; Micron fwd P/E
  ~9×→~10–11×; TSMC fwd P/E spans 23–30×). Re-check before relying on any single number.
- **The macro backdrop is dated** to the Jun-17 FOMC / Jun-25 PCE+GDP / week of Jun 22–26.

## 5. Not verified this run

- **Carr-Wu (2009) single-name VRP** — "VRP significant for 21/35 stocks (level for 3/35)" plus the
  Driessen-Maenhout-Vilkov "−7%/mo (ITM) to −39%/mo (OTM)" index-minus-individual spread, on
  `sources/deep-research-volatility-risk-premium.md`. The assigned verifier failed on a 1M-context
  credit error. **Treat as unchecked** until a follow-up run. (Every *other* VRP citation on that
  page — BTZ 33.23/14.93, Carr-Wu −0.594/t≈−9.5, Bollerslev-Todorov 69.8%, DMV 46.7/28.9, AQR
  Sharpe 0.68 — was **CONFIRMED verbatim**.)

---

## What held up especially well

For balance: the **derivatives/VRP citations were near-perfect** (5 of 6 confirmed to the exact
table figure), and the **headline empirical anchors** were all confirmed verbatim against primary
sources — **Barber-Odean 710 bp**, **SPIVA ~92% / 0-of-22 / 0.00% persistence**, **Odean (1998)
disposition figures**, **George-Hwang 1.23%/mo**, **Sullivan-Timmermann-White p-values**,
**Korajczyk-Sadka $5B capacity**, **NVDA Q3-FY26 financials**, **SK Hynix Q1-26 / FY25 results**,
**the entire Jun-17 FOMC / dot-plot / SEP / BEA-calendar block**, and **Micron's $35B→$100B HBM
TAM**. The skeleton is sound; the flags above are about tightening the joints.
