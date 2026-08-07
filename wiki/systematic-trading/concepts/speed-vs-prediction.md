---
type: concept
title: Speed vs Prediction — The Horizon Economics of Trading Edges
description: Why the latency race is a rank-order tournament with a fixed prize and a rising entry fee (Budish et al. — the pie didn't shrink, the bar rose 97ms→7ms; ABO ~$5B/yr global; the microwave network at ~the speed-of-light floor), why forecasting pays proportionally to skill and only above a horizon where IC·σ√h clears costs (the arithmetic that lands on minutes-to-hours), the 2015 crossover that produced XTX, the evidence a firm's horizon choice is readable from capex + lobbying, and the horizon ladder from microseconds to weeks — including where this desk sits on it.
tags: [systematic-trading, microstructure, market-making, hft, strategy-design]
timestamp: 2026-07-13T00:00:00Z
status: active
sources: []
---

# Speed vs Prediction — The Horizon Economics of Trading Edges

**In plain language.** Two ways to win at electronic trading: be *faster* than everyone at
reacting to things everybody can see, or be *better than everyone at guessing* what prices do
next over the following minutes and hours. These are not two flavors of the same business — they
have opposite economics. Speed is a **tournament**: only the fastest firm gets paid, the prize
pool is roughly fixed, and every competitor's spending raises the entry fee without growing the
pot. Prediction is a **graded exam**: everyone gets paid in proportion to how good their forecast
is, the pot grows with how much risk you can warehouse, and spending on research compounds
instead of obsoleting. [XTX](../../shared/people-firms/xtx-markets.md)'s famous design choice —
ML forecasts, minutes-to-hours holding, GPUs instead of microwave towers — is simply the decision
to play the second game, made at the exact historical moment (2015) when the first game's prize
stopped justifying its entry fee. This page gives the details: the measured economics of the
speed race, the arithmetic of why prediction only pays above a certain horizon, the evidence, and
the honest boundaries of the story.

---

## 1. The claim, made precise first

"XTX doesn't compete on speed" does **not** mean XTX is slow. Every quoting firm needs
*defensive* speed — if a correlated future ticks in Chicago and your London quote doesn't move
within your latency budget, you *are* the stale quote someone races to pick off. XTX co-locates,
runs professional low-latency infrastructure, and hires the engineers for it. The design choice
is about two other things:

1. **Where the marginal dollar of capex goes** — to the research cluster (forecast quality),
   not to shaving the next microsecond off the reaction path; and
2. **Where the edge claim lives** — the firm's stated source of profit is that its *price* is
   better, not that its *reaction* is first; operationally visible as holding risk for
   minutes-to-hours instead of running the book flat second-to-second.

Contrast the poles: Virtu's IPO filings described a near-flat, no-speculation book — inventory
half-lives of seconds-to-minutes, profits from enormous fill counts; XTX's own client language is
the exact inverse — "low market impact liquidity **by holding risk for meaningful periods**."
Same industry label ("market maker"), opposite state variables.

## 2. The speed game's economics — a tournament with a fixed prize **[T + measured]**

The mechanism (Budish–Cramton–Shim, *QJE* 2015). Correlated instruments — ES futures and the SPY
ETF are the canonical pair — are near-perfectly correlated at minutes but **uncorrelated at
milliseconds** (the Epps effect: measured correlation falls toward zero as the sampling interval
shrinks, because information reaches related instruments asynchronously). Every time one leg
jumps, the other leg's resting quotes are *mechanically* stale for a few milliseconds — a
riskless pickoff for whoever gets there first. That structure fixes the game's payoff shape:

- **Rank-order payoff.** Only the first arrival wins the race; second place paid the same costs
  for nothing. Economically an all-pay tournament: rents dissipate into infrastructure spend.
- **The pie doesn't grow — the entry fee does.** BCS's decisive measurement: from 2005 to 2011
  the median ES–SPY race duration collapsed ~97ms → ~7ms (a 14× speed escalation), while the
  profit per race and the total annual arbitrage pie stayed roughly constant (~$75M/yr in that
  single pair). Competition in a tournament doesn't compete away the prize; it raises the bar to
  claim it. Red Queen economics: you spend to stand still.
- **The physical floor has been reached.** The Chicago↔New Jersey microwave network converged to
  ~4ms one-way — within a few percent of the vacuum speed-of-light bound. Each further generation
  (hollow-core fiber, better geodesics, FPGAs → ASICs at the gateway) buys nanoseconds at rising
  cost. Meanwhile the industry's revenue compressed as the race matured: US equity HFT revenues
  fell from roughly $7B (2009) to on the order of $1B by the mid-2010s (TABB estimates).
- **The whole pot is small.** Aquilina–Budish–O'Neill (*QJE* 2022), from LSE message data: races
  occur constantly (~20% of volume), are won by ~5–10 *micro*seconds, disproportionately by a
  handful of firms, and the global latency-arbitrage "tax" extrapolates to **≈$5B/yr across all
  equity markets**. Hold that number: XTX's *single-firm* revenue in 2025 was ≈$5B. The entire
  measured prize pool of the global speed tournament is the same order as one prediction firm's
  top line. That one comparison is the design choice justified in a sentence.

Note also who *pays* the sniping tax: resting quotes — i.e. market makers — which is why quoting
firms that don't win races (XTX's structural position) rationally lobby for **latency floors,
randomized batching (ParFX), speed bumps (IEX's 350μs), and frequent batch auctions**: designs
that convert speed rank back into price competition. The lobbying is the business model's
revealed preference — same lesson as on the [XTX page](../../shared/people-firms/xtx-markets.md).

## 3. The prediction game's economics — why *minutes-to-hours* specifically **[T]**

The capture arithmetic. A forecast with information coefficient IC (correlation between signal
and realized move) applied at horizon h captures, per decision, roughly

> **expected edge ≈ IC · σ√h** (σ√h = the size of the move there is to predict at that horizon)

Run the numbers for EURUSD (σ_day ≈ 50bp, 24h market, uniform-time approximation — flagged as
order-of-magnitude):

| Horizon h | σ√h (the predictable pot) | IC = 2% captures | Verdict |
|---|---|---|---|
| 1 ms | 0.005 bp ≈ $0.5 per $1M | $0.01/M | Nothing to forecast — only *deterministic* races pay here |
| 100 ms | 0.05 bp ≈ $5/M | $0.11/M | Fee-scale; the defensive-repricing zone |
| 10 s | 0.5 bp | $1/M | Marginal — flow/imbalance signals start to work |
| **10 min** | **4.2 bp** | **$8/M** + you *earned* ~0.1–0.3bp spread on entry | **The sweet spot: edge clears costs, and entry is paid, not paid-for** |
| 1 day | 50 bp | $100/M | Real money — but N collapses, overnight risk, and you now fight every stat-arb fund |

Read the table's logic: **below seconds there is nothing statistical to predict** — price
dispersion is smaller than fees, so the only profitable "foresight" is knowing a quote is
*already* stale (a race, not a forecast). **Above hours you're a stat-arb fund** — larger pots
per position but far fewer independent decisions per day (Grinold: IR ≈ IC·√N, and N ∝ 1/h), plus
overnight risk and a much more crowded competitor set. In between sits a band — roughly minutes
to hours — where four conditions hold simultaneously:

1. σ√h is large enough that a realistic IC (1–5%) clears costs;
2. N per day is still huge (thousands of decisions × 50,000 instruments), so the CLT compounds
   tiny edges into near-daily profitability;
3. **entry is paid**: as a market maker you collect the half-spread to *enter* positions your
   model likes — a prediction MM is a stat-arb book whose entries earn the spread instead of
   paying it (the r ≈ S + ν/ρ − qγσ²τ machinery on the
   [prediction-first page](prediction-first-market-making.md)); and
4. **capacity lives here**: at this horizon inventory is recycled through the client-flow
   franchise (internalization ~80%+ per BIS), so size scales with flow share — the GLFT skew
   constant C ∝ σ√(γ/2kA) falling in franchise flow A — rather than with stale-quote depth,
   which is the speed game's tiny and fixed capacity.

And the payoff structure is proportional, not rank-order: a model 10% better than the field earns
~10% more per decision — every improvement pays, nobody's spending obsoletes yours overnight, and
research capex *accumulates* (this year's features and data pipelines still work next year;
last year's microwave route is scrap the day a straighter one lights up).

## 4. Why 2015 — three curves crossed **[I, well-grounded]**

The founding moment wasn't arbitrary. (i) The speed race hit the physics floor and commoditized
— by 2013–15 the microwave routes were built, the marginal microsecond cost more and paid less,
and the tournament's consolidation was visible in shrinking industry revenue. (ii) The deep
learning + GPU curve inflected (2012–15) — exactly the technology that converts full-tape,
cross-asset data into forecast IC at industrial scale. (iii) Banks retreated from principal
risk-warehousing (post-2008 capital rules, the 2013–15 FX-fixing scandals), vacating the FX
dealer seat that internalization economics reward most. A firm optimized for the *new* binding
constraint — forecast quality and risk-warehousing capital, not reaction time — founded at the
crossover, by the person who had run the bank version of the same book. That is the actual
content of "XTX is the opposite of HFT": not slower, but *built for the game that opened when
the speed game closed*.

## 5. How you can tell it's real — a firm's horizon is readable from outside **[P]**

Marketing aside, three public signals identify where a trading firm actually lives, and all
three point the same way for XTX:

- **Capex allocation.** 25,000+ GPUs, 650PB, €1B+ of Finnish data centre — research compute at a
  scale no reaction-time business needs; speed pure-plays put that money into radio networks and
  tower rights. A firm's balance sheet is its revealed strategy.
- **Venue and product behavior.** Disclosed bilateral client streams, top-of-industry
  internalization, zero-hold-time last look, the largest-SI seat in European equities — all
  relationship/warehouse structures, none of them speed-sensitive; a latency shop lives on
  anonymous CLOBs where speed converts to queue position.
- **Lobbying.** Consistent support for latency floors, batching, and last-look abolition — a
  firm whose edge was speed would fight these; a firm that *pays* the sniping tax and wins on
  price wants them. (The self-interest reading and the public-interest reading are both true;
  that's exactly why the letters are informative.)

Honest verification limits: "minutes-to-hours" as the holding period comes from the firm's own
statements plus the BIS internalization-horizon evidence for top FX dealers generally; there is
no independent public measurement of XTX's inventory half-life specifically.

## 6. The honest boundaries of the dichotomy

- **Everyone at the top is fast *and* smart.** Citadel Securities, Jump, HRT, Optiver all run
  serious ML; XTX runs serious low-latency engineering. The taxonomy is about the **binding
  constraint** — the axis a firm would defend to the death (flow access / network / models),
  where its marginal dollar goes, and which loss would kill it. It is not a claim that speed
  firms don't model or that XTX doesn't race defensively.
- **The speed tier is not dead — it's *decided*.** ABO's finding is that races persist and a
  stable handful of firms win them; the rents are real but capped and consolidated. "Bad game to
  *enter*" ≠ "unprofitable for incumbents."
- **The dichotomy blurs at the boundary.** Sub-second flow forecasting (queue dynamics, sweep
  anticipation) is prediction that only pays if you're fast enough to act on it — the zones
  shade into each other around seconds.

## 7. The horizon ladder — who wins at each timescale

The [landscape](algorithmic-trading-landscape.md)'s industry map, re-cut along the horizon axis
with the economics attached:

| Horizon | The game | Payoff shape | Who wins | Capacity gate |
|---|---|---|---|---|
| < 1 ms | Deterministic races to stale quotes | Rank-order tournament | Jump/HRT/CitSec-class racers | Stale-quote depth (tiny, fixed) |
| ms – s | Queue position, defensive repricing | Mixed | All serious quoting firms (table stakes) | Queue priority |
| s – min | Flow/imbalance forecasting | Graded by IC | Prediction MMs, fast stat-arb | Turnover |
| **min – hr** | **Forecast + warehouse + internalize** | **Graded by IC × flow franchise** | **XTX-class prediction MMs** | **Client-flow share (the moat loop)** |
| hr – days | Cross-sectional stat-arb | Graded by IC·√breadth | RenTec/DE Shaw/pods | AUM vs impact |
| **days – wks** | **Cohort/constraint flows, event windows** | **Graded, niche** | **Patient niche players — this desk's corner** (alpha benchmark) | Patience + smallness |
| months + | Factor premia, fundamental repricing | Premium harvest | AQR-class, long-only | Nearly unlimited |

The desk-relevant line: the same arithmetic that sends XTX to minutes-to-hours sends a
zero-latency-budget, verification-rich retail desk to **days-to-weeks** — the horizon where its
measured cohort prints (KR/TW) still contain forecastable structure, N is still adequate for
honest inference, and no speed or franchise gate applies. Choosing your horizon by where your
actual assets bind is the transferable design rule; XTX is just its most famous execution.

## Relationships

- The firm: [XTX Markets](../../shared/people-firms/xtx-markets.md) · [Alex Gerko](../../shared/people-firms/alex-gerko.md).
- The math this plugs into: [prediction-first market making](prediction-first-market-making.md)
  (the r = S + ν/ρ − qγσ²τ machinery and the GLFT moat constant this page's §3 leans on).
- The industry map re-cut here: [algorithmic-trading landscape](algorithmic-trading-landscape.md);
  the rents measured: [industrialization of edge](../../synthesis/industrialization-of-edge.md) §3b.
- The desk's own horizon choice: the alpha benchmark.

## Open questions

- If US/EU equity markets ever adopt frequent batch auctions at scale, how much of the ~$5B/yr
  sniping tax converts into tighter spreads vs into prediction-firm margins? (XTX's lobbying
  implies they expect to win that world.)
- Measured Epps curves on the desk's own instruments (SMH/SOXX/ES at 1m–1d) — where does
  correlation "complete" for the semis complex, i.e. at what horizon does cross-asset lead–lag
  stop being exploitable?
- Is there a public way to estimate a firm's inventory half-life (e.g., from SI/off-exchange
  print patterns) — the missing outside verification of holding periods?

## References (external; key ones)

Budish, Cramton & Shim (2015), *The High-Frequency Trading Arms Race*, QJE. · Aquilina, Budish &
O'Neill (2022), *Quantifying the High-Frequency Trading "Arms Race"*, QJE. · Epps (1979). ·
Laughlin, Aguirre & Grundfest (2014) on the Chicago–NJ microwave buildout. · TABB Group US equity
HFT revenue estimates. · Virtu Financial S-1 (2014). · Schrimpf & Sushko, BIS Quarterly Review
(Dec 2019). · Guéant–Lehalle–Fernandez-Tapia (2013) for the skew constant used in §3.
