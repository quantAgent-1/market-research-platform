---
type: market-note
title: "Semis Week Ahead — July 13–17, 2026 (TSMC / ASML / CPI)"
description: A trader-facing week-ahead preview for the semiconductor complex — the CPI (Tue) → ASML (Wed) → TSMC (Thu) event spine, the TSMC bar and what actually moves it (capex, CoWoS, FX), the macro overlay, NVDA/AMD/MU traded by proxy, positioning/flow, and the asymmetric risks. As-of 2026-07-12; expected to go stale after 7/17 (post-mortem stub below).
tags: [market-research, semiconductors, TSMC, ASML, macro, event-preview]
timestamp: 2026-07-12T00:00:00Z
status: active
sources: []
---

# Semis Week Ahead — July 13–17, 2026

**As of:** Sunday 2026-07-12 (pre-market). **Expected to go stale:** after Friday 2026-07-17 —
grade it in the [post-mortem](#post-mortem-stub-fill-after-717) at the bottom.

> **What this is.** A forward-looking, trader-facing preview of the week for a book that tracks
> NVDA / AMD / MU / TSMC / ASML and the SMH/SOXX/SOXL complex. Built from a
> [deep-research run](#provenance) (run `wf_c552e035-018`; the TSMC/ASML/CPI spine is
> primary-source-verified) plus training-level analysis of what actually moves the tape. This is
> also the first live rep of the [market-research skill](../designs/market-research-skill.md)'s
> "week-ahead" job, run by hand. **Dates/numbers are flagged confirmed vs. expectation
> throughout.**

## Bottom line

Three events form the week's spine and they cluster Tuesday→Thursday: **June CPI (Tue), ASML
pre-open (Wed), TSMC overnight (Thu)**, then **monthly options expiration Friday**. TSMC is the
whole ballgame — the cleanest single read on whether the AI-capex build-out is still accelerating,
and because it governs CoWoS packaging (NVDA/AMD supply) and HBM pull (MU), **your names trade the
TSMC call by proxy at Thursday's open without reporting themselves.**

The setup is a **high-bar, "buy-the-rumour" tape**: sell-side is bullish (Citi at a Street-high
NT$3,800), semi ETFs just took a record one-day inflow, and a guidance/capex *raise* is already
the consensus expectation. That is the asymmetry — TSMC has already pre-guided FY26 growth ">30%"
and capex to the ~$56B high end, so an in-line-to-modest raise can sell off a positioned market
even on "good" numbers. **The reaction is a second-derivative trade: it turns on whether the raise
beats what is already priced, not on whether one happens.**

## The calendar (all times ET)

| Day | Event | Time | Why a semis book cares |
|---|---|---|---|
| **Mon 7/13** | Fed speakers (Bowman, Waller) | — | Rate-path tone; quiet, no data |
| **Tue 7/14** | **June CPI** | 8:30am | The macro-beta event. Core consensus **+0.2% m/m** (prev +0.3%, per Trading Economics). Hot → yields up → high-beta multiples compress |
| Tue 7/14 | Fed Chair testimony *(calendar names Warsh — secondary, verify)* + Barr, Goolsbee, Cook | — | A (new) Fed Chair testifying on CPI day is its own vol layer |
| **Wed 7/15** | **ASML Q2** (pre-open) + **June PPI** (8:30) + Empire State | AM | Semi-cap read one day ahead of TSMC; PPI confirms/denies CPI |
| **Thu 7/16** | **TSMC Q2** (call 2:00–3:30am ET / 2:00pm Taipei) + Retail Sales + Jobless Claims + Philly Fed | overnight / 8:30 | **The main event.** Results land overnight US time → the US reaction is at the Thursday cash open |
| **Fri 7/17** | Monthly options expiration + Industrial Production | — | OpEx gamma unwind one day after the TSMC catalyst |

**No FOMC this week** — the next policy decision is **July 29**. So this is a data-and-speakers
week, not a decision week. Risk density runs Tue→Thu and **peaks Thursday**, when TSMC, retail
sales, and claims all hit within hours of each other, the day before expiration.

## The main event — TSMC, Thursday 7/16 (confirmed)

Reports before the US open; analyst call 2:00–3:30am ET (2:00pm Taipei). Quiet period ran
7/6–7/15. Note the timing trap: **the print and call are overnight US time, so the tradeable US
reaction is Thursday's 9:30 open**, not a specific intraday slot.

**The bar it is judged against — TSMC's own Q1 guide (primary, from the SEC 6-K):**

- Revenue **US$39.0–40.2B** (~+9–12% QoQ off Q1's $35.90B)
- Gross margin **65.5–67.5%**, operating margin 56.5–58.5%
- **Conditioned on FX = 31.7 NTD/USD.** This is live: roughly **0.4pp of gross margin per 1% move
  in the Taiwan dollar**, so a stronger TWD since the guide *helps* USD revenue but *squeezes*
  reported margin. Check the FX before reading any margin figure as a beat or miss.

**Street consensus (Zacks/aggregator — secondary):** revenue ~**$40B** (+32–33% YoY off $30.07B),
EPS **~$3.77–3.83 per ADR** (vs $2.47 a year ago). Unit trap: EPS is quoted **USD-per-ADR**; the
headline prints in NT$ (~NT$18–19). Because consensus already sits at the *top* of TSMC's own
guide, the guide-vs-consensus gap is tight — which is why the **guidance raise, not the Q2 actual,
is the real catalyst.**

**What actually moves the stock, in order:**

1. **2026 capex.** Guided US$52–56B — the largest in company history, ~+37% over 2025's ~$40.9B —
   and already steered to the ~$56B high end at the Q1 call. Both Citi and GF Securities (Jeff Pu)
   expect a raise. A number starting with a 5-handle **above** $56B is the bull trigger;
   reaffirming $56B is the "sell-the-news" risk. This one line is the cleanest read on the whole
   semi-cap complex (ASML/AMAT/LRCX/KLAC).
2. **CoWoS / advanced-packaging commentary.** CoWoS is the physical bottleneck for NVDA and AMD
   GPUs, so TSMC's expansion pace *is* the NVDA/AMD supply signal.
3. **HPC/AI mix and 2nm ramp.** Q1 node mix: 3nm 25% / 5nm 36% / 7nm 13% (advanced = 74%); **2nm
   is not yet a separate line**, so any N2 ramp/pricing colour is new information.
4. **FY26 growth guide.** Already ">30%"; a bump toward mid-30s+ is what a positioned tape needs.

**Sell-side setup:** Citi (Laura Chen) carries a Street-high NT$3,800 target (up from NT$2,875,
Buy reiterated) — ~+57% over the ~NT$2,415 level on 7/11 (52-wk high ~NT$2,535). The bullish
posture *is* the risk: the bar is high.

## ASML — Wednesday 7/15, pre-open (confirmed)

The other semi-cap catalyst, one day early. **Revenue consensus $10.28B (+17.8% YoY, Zacks)** vs
ASML's own EUR **8.4–9.0B** guide — not directly comparable ($10.28B ≈ €8.9–9.5B, i.e. near/just
above the top of the euro guide, not a big gap). The watched line is **net bookings / new orders,
especially EUV** — the earliest hard commitment that fabs are *placing* capacity bets, plus China
exposure post-export-controls. Caution from the verification pass: an ASML "EPS consensus" (~$7.98)
and a 51–52% GM figure floating in the press are actually mislabeled *company guidance* — **do not
trade those as consensus.**

## The macro overlay — CPI (Tue) / PPI (Wed)

High-beta semis trade off the rate path, so CPI is the second-biggest event after TSMC. **June CPI
is confirmed for Tue 7/14** (primary: the White House/OMB release schedule; 8:30am ET is
convention, not stated in the doc). Core consensus **+0.2% m/m** (Trading Economics); one source
notes headline should moderate after WTI crude fell ~20% in June, putting the weight on **core**.
The live upside risk is **tariff-driven goods inflation** — a hot core sends yields up and semis
lead the drawdown; a cool print is risk-on into the prints. **PPI follows Wed 7/15** (consensus
headline +0.1% / core +0.2% m/m) as the confirm. Retail sales + jobless claims land Thursday
alongside TSMC.

## Your names — NVDA / AMD / MU (none report this week)

They trade the **TSMC read-through**, not their own numbers:

- **NVDA** — no earnings. Baseline: H200 exports to China were approved back in **January 2026**
  (the Trump administration reversed the Biden ban), subject to a cap — that is *background*, not a
  this-week catalyst, but China-export headlines remain the live tail. NVDA's Thursday gap is
  driven by TSMC's HPC revenue and CoWoS commentary overnight. A blog source had NVDA in a
  **positive dealer-gamma regime (net GEX ~+$1.4B)** — dealers dampening intraday moves — but it is
  **undated and low-quality**, so treat it as a hypothesis to confirm on a real gamma feed, not a
  fact.
- **AMD** — no earnings this week, but **"Advancing AI 2026" is July 22–23** (Moscone, confirmed by
  AMD IR) — *next* week. So this week is a **pre-event drift/positioning window** into the
  MI-series reveal, on top of the TSMC read.
- **MU** — already reported (late-June). This week it is a **supply-chain/pricing play**: rising
  DRAM/HBM pricing and Micron qualified into **NVIDIA's Vera Rubin** platform since ~March. Trades
  off TSMC's HPC tone and any HBM demand colour.

## Positioning & flow

- **SOXX took ~$5.43B of net creations in a single day on July 8** (ETF.com) — a record-scale
  rotation *into* chips right before the week. This is the "buy-the-rumour" fuel and the reason the
  bar is high.
- **~$50B of leveraged-ETF rebalancing** flagged as a market-vol driver (Benzinga) — directly
  relevant to the desk's [forced-flow](../shared/concepts/leveraged-etf-decay.md) work: a big
  TSMC-driven SMH move Thursday mechanically amplifies into the close via SOXL-type rebal.
- **OpEx Friday 7/17.** If the complex is in positive gamma, expect vol suppression *until* a
  catalyst breaks it — and the TSMC print Thursday is exactly the catalyst positioned to break a
  pinned tape one day before expiration.

## How to think about the asymmetric risks

1. **The high-bar problem (primary).** Bullish positioning + a pre-announced raise means "good but
   not great" is a sell. The clean expression: the move is in the *capex number above $56B* and
   *CoWoS expansion*, not the Q2 actual.
2. **TWD/FX.** A margin "miss" may just be Taiwan-dollar strength against the 31.7 assumption —
   don't misread it as operational.
3. **CPI two-way (Tue).** Tariff goods inflation is the upside surprise; WTI −20% should moderate
   headline, so weight **core**.
4. **China-export headline tail.** Unscheduled by nature; the ambient risk that can override a good
   TSMC/ASML print in one headline.

## Honest limits (confirmed vs. expectation vs. unconfirmed)

- **Confirmed (primary):** all dates/times (TSMC IR, ASML cadence, White House/OMB schedule);
  TSMC's guide numbers and FX condition; the node mix; June CPI on 7/14.
- **Expectation, not fact:** the TSMC guide/capex *raise* (Citi/GF view); consensus figures are
  aggregator (Zacks), not primary.
- **Weak/unconfirmed — verify before trading:** the NVDA +$1.4B gamma (undated blog); the "Fed
  Chair Warsh" testimony naming (single secondary calendar that also showed placeholder "actuals");
  exact retail-sales/claims consensus (sources disagreed). **Live SMH/SOXX/NVDA levels and the
  TSMC/ASML options-implied moves were not pulled** — get those before sizing.

## Post-mortem stub (fill after 7/17)

*Grade the week here — this is the rep that makes the note worth writing:*

- **CPI (Tue):** actual vs +0.2% core → semis reaction (did the rate-beta call hold?) — *TBD*
- **ASML (Wed):** bookings/EUV vs watched → SOX reaction — *TBD*
- **TSMC (Thu):** capex revision (did it beat ~$56B?), CoWoS tone, FX-adjusted margin → the
  gap-and-go vs sell-the-news call — *TBD*
- **The proxy trade:** did NVDA/AMD gap on the TSMC read as framed? — *TBD*
- **The high-bar thesis:** was "good news sold"? (the recurring 2026 pattern) — *TBD*
- **Lessons for the next week-ahead:** — *TBD*

## Provenance

Deep-research run `wf_c552e035-018` (2026-07-12): 6 search angles → 26 sources → 25 claims
adversarially verified (3-vote), 22 confirmed / 3 refuted. The TSMC/ASML/CPI spine traces to
primary sources (TSMC IR + SEC 6-K, ASML 6-K, White House/OMB release schedule); consensus and
sell-side framing are secondary (Zacks, Forbes, Seeking Alpha, TechTimes, TipRanks). Full verified
ledger retained in the session transcript.

## Relationships

- Whole-complex fundamentals & the drawdown thesis: [Semis/AI State of Play (2026-07-09)](semis-ai-state-of-play-2026-07-09.md)
- The tool this preview is a manual rep of: [Market-Research Skill](../designs/market-research-skill.md) · the [Semis Institutional-Flow Map](../designs/semis-institutional-flow-map.md) (positioning/flow layer)
- Mechanics referenced: [Leveraged-ETF decay](../shared/concepts/leveraged-etf-decay.md) · [Forced-Flow Calendar](../designs/forced-flow-calendar.md)
- The Asia→US lead this week exercises: [Alpha Map, Lane 4](../synthesis/alpha-map.md)
