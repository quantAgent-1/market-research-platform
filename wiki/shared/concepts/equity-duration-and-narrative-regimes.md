---
type: concept
title: "Equity Duration & Narrative Regimes — the Fishing-Rod Mechanics, Verified"
description: Why late-rally stocks trade on narratives instead of earnings, rebuilt from first principles — equity duration (the fishing rod formalized), the early/late catalyst asymmetry, the regime marker corrected for cyclicals (duration hides in E, not P/E), and the net-new narrative-flow asymmetry (the boom manufactures its own bear narratives). Includes the adversarial verification of the desk's S48 framework with four amendments walked back on-page.
tags: [shared, market-research, asset-pricing, cyclicals, semiconductors, volatility]
timestamp: 2026-07-17T00:00:00Z
status: active
sources: []
---

# Equity Duration & Narrative Regimes — the Fishing-Rod Mechanics, Verified

**Origin (2026-07-17):** a circulated educational post ("imagine you're holding a fishing rod…")
argued that after big rallies, stocks stop trading on earnings and start trading on 1–3-year-out
narratives, with rising volatility and tops that form on trivial news. This page (1) rebuilds the
post's claims from first principles and grades them, (2) runs the same adversarial pass on the
desk's own S48 framework (remaining-integral, three-variable taxonomy, good-news-sold streak,
touch probabilities) and **records the walk-backs**, and (3) files the one genuinely new
mechanism the combination exposes: **narrative-flow asymmetry**.

## 1. The fishing rod is equity duration

A stock's price is the present value of expected cash flows. Define its **duration** the way a
bond's is defined: the value-weighted average arrival time of those cash flows. A stock priced
mostly off the next year's earnings has short duration — your hand near the tip. A stock priced
off years 3–5 has long duration — your hand at the handle, and the tip (price) moves much more
than your hand (assumptions).

The sensitivity math: if the market anchors on year-3 earnings, then a *narrative* that shaves
the assumed growth path by 4–5 points per year cuts the year-3 earnings estimate by ~15%
(1.05⁴ − 1 ≈ 22% at four years; 1.04³ ≈ 12% at three), and if the exit multiple echoes even
modestly (worse cycle position ⇒ −10%), the price falls ~20% **with zero change to any current
number**. Worked on MU at the June peak: $1,255 ≈ 5.3× a 2029 EPS of ~$314 (=$143 × 1.30³).
Trim the narrative growth rate from 30% to 25% and let the exit multiple slip 10% → price −20%.
That reproduces the observed −21% median chip drawdown *from small-news events* — the mechanism
closes quantitatively. **Verdict: TRUE**, and it is standard asset pricing (for high-multiple
stocks, price variance is dominated by long-horizon expectation revisions, not current
cash-flow news — the Campbell–Shiller decomposition result, informally rediscovered).

## 2. Why the best catalyst changes over the rally (early/late asymmetry)

Early in a cycle, the market's prior on earnings *persistence* is low ("cyclical glut fears") — a
beat is evidence the regime itself changed, so it forces a large upward revision (the beat
updates φ, not just this quarter). Late in the cycle, the persistence prior is already maxed —
a beat confirms what's priced and updates nothing. Formally: the likelihood ratio of a beat under
bull-vs-bear *long-horizon* hypotheses ≈ 1, so beats carry ~zero Bayesian weight against a
2028-supply narrative. Only information about the long-dated variables moves the price.
**Verdict: TRUE** — and it is the post's version of the desk's three-variable taxonomy (turn
date / trough depth / normalized level): late-cycle, only those reprice the stock.

## 3. The regime marker, corrected for cyclicals — duration hides in E, not P/E

The subtle trap: MU at ~6.4× forward earnings looks like a *short-duration* (cheap) stock. It is
not. For a cyclical at peak earnings, the long-dated uncertainty lives inside **E** — "how long
does $143 persist and where does it trough" — which is exactly a narrative variable. A low
multiple on peak earnings can carry *more* narrative-duration than a high multiple on stable
earnings. The post's own marker handles this where plain P/E fails: **trailing ÷ forward P/E**.
MU: trailing-twelve-month EPS ≈ $50–55 (the ramp: ~$5 → $8–10 → $12–15 → $25.11) ⇒ trailing
≈ 17–18× vs forward ≈ 6.4× ⇒ **ratio ≈ 2.8×** — squarely inside the post's "trailing 2–3×
forward" narrative regime, despite the "cheap" forward multiple. That is why valuation arguments
settle nothing here (both $650 and $1,300 are "justified" by choosing the persistence
assumption), and why the desk's reverse-DCF is used as an *assertion-reader*, not a signal.

## 4. The net-new mechanism: narrative-flow asymmetry (the wind blows one way)

The post treats late-cycle narrative sensitivity as symmetric volatility. It is not symmetric,
and this is the sharpest thing the verification produced:

**A boom manufactures its own bear narratives.** High prices fund the supply response (the CXMT
IPO is literally the bear thesis getting a public war chest); high input costs incentivize
demand-efficiency work (CXL pooling, KV-cache compression, quantization — every one a
"memory-per-dollar falls" story); extreme margins invite entry, regulation, and price-fixing
suits; extended positioning generates its own de-risking events. Meanwhile, *incremental bull
narratives require raising assumptions that are already at record levels* — there is almost no
room on that side. So late-cycle, the narrative **flow** — the arrival rate of repricing-relevant
stories — is structurally net-bearish even while fundamentals print green.

This one mechanism unifies three observations the desk had been holding separately: why good
news gets sold (it carries no narrative weight), why tops form on trivial news (the marginal
narrative is bearish by construction), and why the drawdown persists against green tripwires
(tripwires measure the machine; the narrative flow reprices the machine's *future*). The long
rod isn't just long — the wind on it blows one way in the late innings.

## 5. Management tone (the post's aside, formalized)

"Semi management is always bullish; rare exceptions mark bottoms" is a **pooling equilibrium**:
bullish tone is what every management says in every state (incentives: stock comp, customer
confidence, competitive signaling) ⇒ zero information. A bearish statement breaks pooling at
personal cost ⇒ high information — and since managements see order books turn before the street,
capitulation-tone clusters near troughs (SK Hynix's ~50% capex cut Oct-2022; "worst downturn in
13 years" 2023 ≈ the bottom). Corollary the post omits: the *costly signal* readable in both
directions is **capex action**, not tone — which is exactly why the desk's master variable is
the capex guide, not the conference-call adjective count. **Verdict: TRUE, with the corollary.**

## 6. Scorecard on the post

| Post claim | Verdict |
|---|---|
| Early rally: current beats are the catalyst; late: they can't be | **TRUE** (persistence-prior updating; Campbell–Shiller) |
| Fishing rod: small long-run assumption changes → big price moves | **TRUE** (equity duration; MU arithmetic closes at −20%) |
| Late-stage: narratives (CXMT, efficiency, supply) dominate earnings | **TRUE**, sharpened: the flow of such narratives is *asymmetrically bearish* (§4) |
| "Narratives can't be falsified today by good earnings" | **TRUE but incomplete** — some have scheduled falsification dates (capex guides, SKH print); the desk's calendar is the edge over the post's fatalism |
| Valuation can't decide semis buys/sells | **MOSTLY TRUE** mid-range; valuation still works as an assertion-reader and at extremes |
| Volatility rises after big rallies | **TRUE** (duration ↑ + ownership migrates to price-dependent hands); note it inverts the index-level leverage effect — a regime marker in itself |
| Tops form on very little news | **TRUE** (marginal-buyer exhaustion + §4 asymmetry; Jun-22 peak formed on no news; March needed VIX-31 shocks to *bottom*) |
| Trailing/forward 2–3× as the regime marker | **TRUE and better than P/E for cyclicals** (§3 — it catches MU at 2.8× where forward P/E misleads) |

## 7. The same pass run on the desk's own framework — amendments recorded

1. **Remaining-integral principle — refined, cartoon version walked back.** As stated ("a record
   quarter that doesn't extend the cycle shortens the integral by one boom quarter"), the
   arithmetic is wrong in expectation: the banked quarter adds cash worth face value, and the
   expected shrinkage of the remainder is already in the price — the pure model predicts *flat*,
   not down, on an as-expected print. What makes as-expected prints genuinely mildly bearish is
   the **rising-hazard refinement**: if the cycle's turn has a hazard rate that rises with age,
   then surviving another quarter *without cycle-extension evidence* raises the posterior turn
   probability — the integral shrinks by more than the banked slab. State it that way.
2. **Three-variable taxonomy — completeness amendment.** Turn date / trough depth / normalized
   level is complete for *fundamental* repricing but not for *price*: add the two
   non-fundamental channels the desk already uses in practice — macro discount-rate moves (the
   Jul-1–2 leg was partly hot-jobs/hike-odds) and pure flow mechanics (opex, LETF rebalance).
   Three fundamental + two non-fundamental.
3. **"Good-news-sold ×6" — overcounted, walked back.** ASML rallied ~5% on its own print
   (day-1 counter-example); MU's Jun-24 reaction was a +15.7% rally that round-tripped on
   *quarter-end flows*, not an immediate sell. The defensible statement: **every index-level
   rally attempt since the Jun-22 peak has been sold within 1–3 sessions, and single-print
   reactions have been mixed-to-negative** — aggregate-level distribution evidence, not a clean
   streak of six. The conclusion (distribution regime) survives on the aggregate; the counting
   was sloppy and n is small either way.
4. **Touch probability must float with spot and σ.** "~40% by year-end" was quoted at MU ≈ $970;
   at ≈ $900–920 the same machinery gives **~35–40%**, and the number moves ±10 points for
   σ ∈ [50%, 70%]. It is a function, not a constant; quote it with its arguments.
5. **Stocks-lead-pricing magnitude softened.** The "1–3 quarters" lead is 2018-anchored; 2021's
   evidence is mixed (the equity top and the spot-price peak roughly coincided; contract prices
   peaked later). Robust form: *stocks never wait for the pricing peak to be visible in
   hindsight; the lead ranges ~0–2 quarters and may be longer now that cycle data arrives
   faster.*
6. **"No VIX bell" scoped.** True within the sector-contained base case. If this de-rate ever
   *does* print a VIX spike, that is not the awaited bottom-bell — it is the signature of the
   bust tail activating (semis are too large an index weight to fall 25%+ quietly).
7. **Tripwire list gains candidate #7:** a demand-efficiency shock (CXL pooling adoption,
   inference-efficiency breakthroughs) — currently only tracked as a 2027 note, but §4 says
   efficiency narratives are exactly the kind the late-cycle tape overweights.

## 8. What survives, and what to do with it

Both the post and the framework survive first-principles reconstruction; they are the same
physics at different resolutions. The post's gap is **dates and asymmetry** — it leaves the
reader with "endure the volatility," where the falsification calendar (Jul 28–30: hyperscaler
capex, SK Hynix HBM4, Q3 contract close) converts narrative exposure into a testable schedule.
The framework's gaps were the four amendments above, now recorded. Practical conversions:
size to narrative-vol not fundamental conviction (the rod is long — same thesis, smaller
position); pre-commit cycle-clock exits (pricing momentum, capex budgets, cohort flows), because
in a narrative regime the *fundamental* sell signal arrives while earnings still look perfect;
and treat duration cutting both ways — the same convexity that takes 8% out on a broker note
puts 15% back on a clean print. Long-duration ≠ doomed; it means the tails are where the
returns live.

## Honest limits

- The MU trailing-EPS figure (~$50–55 TTM) is assembled from the reported ramp, not a filing
  pull — verify before using in anything sized.
- The narrative-flow asymmetry (§4) is argued from mechanism and one live episode; it wants a
  measured artifact (count repricing-relevant headlines by sign across a cycle) before being
  treated as law.
- Event probabilities and the touch function remain subjective inputs; the value is the
  post-mortem discipline, not the point estimates.

## Relationships

- Siblings: [Trading the Second Derivative](second-derivative-cycle-trading.md) (the cyclical
  clock this page's §3 plugs into) · [Multi-Week Unwinds](multi-week-unwinds-and-recoveries.md) ·
  [Distribution & Pullback Tells](distribution-and-pullback-tells.md) ·
  [Informed vs Uninformed Flow](informed-vs-uninformed-flow.md)
- The S48 pages this pass amends: MU $1,200 first-principles
  (§7 probability now floats; remaining-integral refined) ·
  [Drawdown anatomy March-vs-July](../../market-research/positioning/drawdown-anatomy-march-vs-july-2026-07-16.md)
  (no-bell scoped) · [CXMT IPO & Micron](../../market-research/memory/cxmt-ipo-micron-implications-2026-07-16.md)
  (the IPO = §4's funded-bear-narrative exhibit)
- Ledger: extends **M6** (duration/convexity — the equity-side application of the rates lens).

## 9. The question-cadence corollary (added 2026-07-31 — the April→July round trip as the page's live case study)

The two 2026 earnings rounds bracket a complete regime cycle and yield the operational form of §2:

**An earnings round re-rates a stock only if it answers the question the market is currently
asking.** The April round answered *"is the boom real, and how big?"* — yes, bigger than modeled
(record Q1s, +50–60% Q2 pricing guided, capex confirmed, HBM pre-booked into 2027) — so price
moved twice at once: estimates up AND multiple up (SOX +40% in 17 straight sessions off the March
fear-discount; MU to $1,255 = 8.8× boom-year EPS = 5.3× the 2029 narrative number; duration fully
extended). The July round answered *"is 2026 intact?"* — yes, at records — **but the market had
moved to "what does 2027 look like?", which no July print could answer** → every record was sold
(the §2 likelihood-ratio ≈ 1 mechanic, observed at maximum volume: SKH's largest-ever Korean OP
sold −14.65% on print day).

The arithmetic of the round trip: between the rounds, memory earnings roughly **doubled**
(Samsung OP ₩57.2T→₩89.5T, SKH ₩37.6T→₩60.5T) while the multiple roughly **halved** (~8.8×→~6×
on MU) — a pure duration-compression event against improving fundamentals, amplified by cohort
unwinds (four July tranches, then the Korean leveraged-retail cascade). And per §4, the interim
news-flow that did the damage was manufactured by the boom itself: CXMT's IPO (the bear thesis
capitalized), the supply response tooling up (LRCX backlog), demand elasticity appearing (Samsung
DX's first-ever loss on parts costs), and the financing margin repricing (the NVDA–OpenAI
guarantee story). Not one negative 2026 fact printed in the entire five-week de-rate.

Cycle-clock check: memory equities historically top 1–3 quarters before pricing peaks — a June-22
equity top with the pricing second derivative rolling +90–95%→+50–60%→+13–18%E into Q4 is *on
schedule*, not anomalous. Corollary for the next round (Oct): it is the first that CAN answer the
2027 question (first 2027 capex framings + 2027 HBM contract pricing + elasticity in volumes) —
i.e., the first with two-sided re-rating power since June; see the
adjudication-week thread §10.

## 10. The scarcity-response asymmetry — why "AI succeeds" and "memory de-rates" are one forecast, not two (added 2026-07-31)

Prompted by: *"fundamentals look intact — am I contrarian to believe AI eventually succeeds? In
2020–21 I knew NVDA would be the AI-hardware monopoly, and 2022 felt like this."* The dissolution:

- **A monopoly's scarcity gets paid.** When NVDA was the bottleneck (2022–24), customers had no
  substitute (CUDA, the design lead), so the industry's success was *forced through its margins* —
  every AI dollar crossed its toll booth. Scarcity → pricing power → the owner collects.
- **A commodity's scarcity gets competed away — by its own customers.** Memory buyers respond to
  76% supplier margins by funding alternatives: Apple lobbying Commerce to qualify CXMT, NVDA
  designing Rubin CPX around GDDR7 instead of HBM, customer deposits underwriting SKH's +55%
  capex, the capital markets handing CXMT ~$8–10B at the top. The boom *finances its own ending* —
  2018 and 2021 ran the same script.
- Therefore "AI succeeds" (the consensus — 4-for-4 capex raises) and "memory margins mean-revert
  in 2027–28" are **not opposing views; the second is a consequence of the first at these
  prices.** AI at scale *requires* memory getting cheaper, and its buyers are making it happen.
  Record fundamentals are the evidence for the de-rate, not against it.
- **Position corollary:** a 3–5-year "AI succeeds" conviction is horizon-matched to *bottleneck
  owners*; expressed through commodity cyclicals it silently becomes a cycle-timing bet, whatever
  the holder intends. The honest exception: the HBM layer (3 suppliers, annual contracts,
  deposits, sold out into 2027) is the most monopoly-like memory has ever been = the
  dampened-cycle bull case — but the commodity layer, which printed Q2's records, is the same
  cycle as ever.
- **The NVDA-2022 lesson, inverted:** NVDA fell −66% *while the monopoly thesis was true*. Being
  right never prevented the drawdown; what collected the ChatGPT vindication was *surviving to
  it* — unlevered, holdable size, and an asset that couldn't be competed away in the interim.
  Pain is not information about the thesis; it is information about the size.
