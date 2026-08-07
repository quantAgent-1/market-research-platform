---
type: firm
title: XTX Markets
description: London algorithmic market maker (Gerko, 2015) that wins on ML price prediction and inventory-holding rather than speed — 50,000+ instruments, >$250B/day, single global risk book, ~300 staff; 2025 net profit £1.71B (~£13M revenue per head, the highest in finance).
tags: [systematic-trading, ml-stats, microstructure, market-making, fx, derivatives]
timestamp: 2026-07-13T00:00:00Z
status: active
sources: []
---

# XTX Markets

**In plain language.** XTX is a London trading company that makes money the way a currency-exchange
booth does — it continuously offers to buy a little below fair value and sell a little above it, and
earns the gap — except it does this across more than fifty thousand stocks, currencies, bonds and
futures at over $250 billion of turnover a day, with no human traders making calls. The industry
assumption is that such firms win by being the fastest machine in the race. XTX is the famous
counterexample: it wins by *predicting prices better* (industrial-scale machine learning — it owns
one of the largest GPU clusters in finance) and by *holding the risk longer* (minutes to hours
instead of microseconds). It is, per revenue per employee, plausibly the most profitable company of
any kind on earth: roughly £3.9 billion of 2025 revenue from ~300 people.

The name is a quant joke that doubles as a mission statement: **XᵀX** is the matrix in the
least-squares normal equations (β = (XᵀX)⁻¹Xᵀy) — the firm is literally named after regression.

## The record (verified facts)

Founded January 2015 by [Alex Gerko](alex-gerko.md) as a spinout of GSA Capital's quantitative FX
desk, which Gerko had built since 2009. Gerko owns ~75%. Zar Amrolia — Deutsche Bank's former FX
boss, i.e. the client-franchise adult in the room — was co-CEO at launch and moved to deputy
chairman in 2017; since 2023 the co-CEO alongside Gerko is **Hans Buehler**, the ex-JPMorgan quant
best known as lead author of *Deep Hedging* (2019), the paper that reframed derivatives hedging as
reinforcement learning under transaction costs. Headquarters in King's Cross, London (since 2018),
with offices including Paris (the post-Brexit EU entity, 2018), New York and Singapore. Roughly 300
employees globally as of 2026 — overwhelmingly researchers and engineers; there are no
discretionary traders.

Scale and share, in sequence — the takeover of FX is the cleanest public record of a non-bank
eating a bank franchise:

- **2016** — first non-bank ever in the Euromoney FX top-10 (9th, 3.87% share); FCA-authorized that July.
- **2018** — 3rd-largest FX liquidity provider globally (7.36%); ~11.5% of European equities volume.
- **2019** — the **largest spot FX liquidity provider in the world**, ahead of every bank — in the
  world's largest market (~$9.6T/day turnover per the 2025 BIS Triennial). US equities entry the same year.
- **2019 onward** — the largest **systematic internaliser** (SI — a MiFID II firm filling client
  orders against its own book off-exchange) in European equities, for 3+ consecutive years.
- **2021** — XTX Direct launched (bilateral single-dealer streams to banks, retail brokers, real
  money and hedge funds in the US, via XTX Execution Services LLC).
- **Today** — ML price forecasts for **50,000+ instruments** across equities, FX, fixed income,
  commodities and (recently, cautiously) crypto; trading in ~35 countries on 80+ venues; daily
  volume reported above $250B and more recently ~$295B.

**Financials** (combined UK operating entities, per Companies House filings as reported; the group
sits under a Cayman holding company, so read these as the visible floor, not a group total):

| Year | Net trading revenue | Net profit | Note |
|---|---|---|---|
| 2022 | £2.5B | £1.1B | +68% / +64% — the volatility year |
| 2023 | £2.0B | £835M | the low-volatility down year — MM revenue breathes with vol |
| 2024 | £2.74B | £1.28B | +54% profit; Gerko's personal payout £682M |
| 2025 | £3.93B | £1.71B | record; £1.78B dividends upstreamed; the main entity returned 289% on opening net assets |

For calibration against the other machines (2024): Jane Street ~$20.5B net trading revenue with
~2,600 staff (~$8M/head); Citadel Securities ~$9.7B; XTX ~$3.5B with ~300 staff (**~£13M ≈ $17M per
head** — nothing else in finance is close). Same league, different machines — see the taxonomy below.

## The machine — how the money is actually made

Market making means quoting a two-sided price all day and earning the bid-ask spread. The P&L of
any market maker decomposes into one identity:

> **profit = spread captured − adverse selection − inventory risk cost − infrastructure cost**

**Adverse selection** is the term that kills you, so define it plainly: it is the loss from trading
with someone who knows more than your quote does — you sold to the buyer *just before* the price
rose, so the spread you "won" is dwarfed by the move you ate. A market maker's whole design problem
is: *how do I avoid being the fool at my own quote?* The modern industry is three different answers
to that one question:

1. **The speed answer** (classic HFT — Virtu, the latency-race tier): keep quotes barely-stale by
   cancelling faster than informed traders can hit them, and win the race to everyone *else's*
   stale quotes. Edge lives in microseconds; the moat is co-location, microwave towers, FPGAs.
2. **The flow-access answer** (Citadel Securities): buy retail order flow wholesale (PFOF) —
   retail flow is certified-harmless (uninformed, small, uncorrelated), so internalizing it means
   almost never facing an informed counterparty at all. The moat is the purchasing relationship.
3. **The prediction answer (XTX):** forecast short-horizon fair value well enough that your quote
   already sits where the price is going. Adverse selection shrinks not because you dodge informed
   flow but because your quote is rarely wrong enough to be worth picking off — and when you *do*
   accumulate inventory, the forecast tells you whether it's safe to hold. The moat is the research
   platform: data, compute, and models.

XTX's own one-sentence self-description confirms the third design: it supplies "low market impact
liquidity **by holding risk for meaningful periods**," priced by "machine learning technology
[that] produces price forecasts for over 50,000 instruments." Holding periods are minutes to hours
— geological time by HFT standards. Three consequences follow, and they explain everything visible
about the firm:

**Capex goes to GPUs, not microwave towers.** The research cluster exceeds **25,000 GPUs with 650
petabytes of storage**, and the firm is investing **over €1 billion in a 478-acre data-centre
campus in Kajaani, Finland** (first 22.5MW building completing 2026, four more planned, waste heat
donated to the town — sited for cheap green power and free cooling). No trading firm buys compute
at that scale for microsecond reflexes; you buy it to train forecasting models on the full
cross-asset tape. (Honesty note: XTX still runs professional-grade low-latency plumbing — being
*fast enough* is table stakes everywhere; the claim is that the marginal nanosecond is not where
its edge lives. The full economics of that choice — why the speed race is a fixed-prize
tournament and why prediction only pays above a horizon — are worked out in
[speed vs prediction](../../systematic-trading/concepts/speed-vs-prediction.md).)

**Inventory is warehoused and exited by skew, not panic-hedged.** Worked example: client selling
leaves XTX long $80M EURUSD. A flat-book market maker immediately dumps $80M into the open market —
paying the spread, moving the price against itself, and signalling its position to every predator.
XTX instead *shades both its quotes slightly lower*: its offer becomes the street's most attractive,
so the next wave of natural buyers lifts it, and the inventory exits at a *positive* spread with no
market footprint. That is **internalization** — matching your own clients' opposing flows across
time — and the better your forecast, the longer you can afford to wait for the match. The risk
book is the product: this is why the firm describes itself as the *opposite* of HFT.

**Breadth does the compounding.** One research platform amortized across 50,000 instruments is
Grinold's law (IR ≈ IC·√breadth) applied to market making: a forecast correlation that would be
useless on one name becomes a near-daily-profit machine across tens of thousands, which is how a
market maker prints 56% net margins (2025) and near-zero losing days without any single trade
being smart. Same arithmetic as the stat-arb machines in the
[algorithmic-trading landscape](../../systematic-trading/concepts/algorithmic-trading-landscape.md),
pointed at the spread instead of at alpha.

**The mathematics behind all of this** — the fair-value estimators, the reservation-price/skew
closed forms, the internalize-vs-hedge control problem, and the moat written as a formula — is
reconstructed layer-by-layer (with each claim tagged theory/practice/inference) in
[prediction-first market making](../../systematic-trading/concepts/prediction-first-market-making.md).

**Epistemic status, stated honestly:** XTX publishes nothing about model internals. The *record*
above (scale, rankings, financials, the firm's self-descriptions, the Finland/GPU numbers) is
public and verified; the *mechanics* (skew, internalization economics, toxicity pricing) are the
standard modern e-FX dealer playbook — which Gerko helped write at Deutsche Bank and GSA —
reconstructed at XTX's stated parameters. Treat the first as fact and the second as well-grounded
inference; nothing here is an inside account.

## Why FX first — the arena was structurally vacant

The choice of market is half the lesson. Post-2008 capital rules made warehousing FX risk
expensive for banks exactly when their best e-FX people (Gerko among them) were leaving; FX has
**no consolidated tape** (nobody can see the whole market, so information advantages persist), is
**quote-driven and bilateral** (a two-tier over-the-counter market of dealer streams above
anonymous central limit order books — internalization is legal, normal, and unmeasured), and
settled trades carry **last look** — the convention that lets a liquidity provider reject your
trade *after* seeing it, a free option that protected lazy quoting. A prediction-first non-bank
walked into that vacancy and, within four years, out-quoted every bank in the deepest market on
earth. The generalizable point for this desk: **edges concentrate where market structure recently
changed** — the firm is an existence proof of the [who-pays-you](../concepts/who-pays-you.md)
claim that the payer and the barrier, not the cleverness, decide who eats.

## The doctrine — read the lobbying as revealed preference

XTX is unusually loud in market-structure policy, and every position maps 1:1 onto its business
model — a firm lobbies *against the games it loses and for the games it wins*, which makes
regulatory letters a free X-ray of where a firm's edge actually lives:

- **Against the latency race:** supported latency floors and randomization (the ParFX/EBS-floor
  debates), sympathetic to batch-auction designs — the academic argument (Budish et al.) that
  continuous-time markets create a socially wasteful speed arms race, whose sniping rents
  Aquilina–Budish–O'Neill (QJE 2022) measured at ~$5B/yr globally. A prediction firm wins if speed
  is neutralized.
- **Against last look abuse:** pushed the Global FX Code toward zero hold times and disclosure —
  superior forecasts don't need the free option, and killing it raises rivals' costs.
- **Against PFOF:** Gerko is the industry's most vocal critic of payment for order flow; XTX
  competes for US retail-broker flow via disclosed streams *without* paying for it, and its SEC
  comment letters in the 2022–23 US equity market-structure debate were notably more
  reform-friendly than the incumbent wholesalers'.
- **Venue bets to match:** an equity stake in Aquis Exchange (2018), the subscription-priced venue
  that bans aggressive proprietary flow.

The honest counter-read: these are *also* self-interested positions — each reform would transfer
rents from speed- and flow-access-firms to prediction firms. Both readings are true
simultaneously; that is exactly what makes lobbying informative.

## Org design as strategy

One global risk book, no pods, no P&L silos, ~300 people, researcher-dominated, average pay at the
main UK entity ~£457k (2025). Contrast the two dominant institutional architectures in the
[landscape](../../systematic-trading/concepts/algorithmic-trading-landscape.md): pod shops
(Millennium/Citadel) apply Grinold breadth to *people* — hundreds of teams, ruthless stop-outs;
XTX applies it to *models* — one platform, 50,000 instruments, zero discretionary layer. Hiring
Buehler as co-CEO signals the next axis: derivatives — deep-hedging-style machinery pointed at
options market making, the one major asset class where the firm is not yet dominant. Gerko's
personal philanthropy (the $10M AIMO prize for an AI that wins IMO gold, ~£250M committed to
mathematics education — see [his page](alex-gerko.md)) doubles as the talent-pipeline strategy for
a firm whose entire moat is mathematicians plus compute.

## What this desk takes from XTX

- **The existence proof, correctly bounded.** Short-horizon ML prediction from market data
  *works* — at 25,000 GPUs, petabytes of full-tape data, 50,000 instruments of breadth, and
  quoting rights the desk will never have. It is evidence *for* "prices are forecastable at the
  margin" and evidence *against* "a retail GPU and daily bars can copy it" — the
  F6 discipline stands.
- **It confirms the printers decomposition.** XTX is the prediction-first variant of the
  Service-payer toll road in [the industrialization of edge](../../synthesis/industrialization-of-edge.md)
  §3b — the moat can be compute-plus-models, not only co-location and purchased flow.
- **It validates the desk's honest limit.** The flow-map's rule — *read the present, never race
  it* — is XTX's own doctrine, run at industrial scale: even the best-resourced prediction firm
  on earth chooses not to fight the latency war. The desk's version of the prediction answer is
  cohort prints at daily horizon (the KR/TW measured anchors), which is the same design instinct
  at the only scale retail can hold — cf. the alpha benchmark.
- **Toxicity pricing is the live version of the identification problem.** What XTX prices
  per-counterparty in real time — is this flow informed? — is exactly the
  [informed-vs-uninformed identification problem](../concepts/informed-vs-uninformed-flow.md) the
  desk faces from the outside; their solution (measure markouts per flow source, price
  accordingly) is copyable in miniature on the desk's own fills.

## Relationships

- People: [Alex Gerko](alex-gerko.md) (founder, 75%, co-CEO) · Hans Buehler (co-CEO, *Deep Hedging*).
- Mechanics: [market making](../../systematic-trading/strategies/market-making.md) ·
  [who pays you](../concepts/who-pays-you.md) ·
  [informed vs uninformed flow](../concepts/informed-vs-uninformed-flow.md) ·
  [limits to arbitrage](../concepts/limits-to-arbitrage.md).
- Industry map: [algorithmic-trading landscape](../../systematic-trading/concepts/algorithmic-trading-landscape.md) ·
  [the industrialization of edge](../../synthesis/industrialization-of-edge.md) ·
  the alpha benchmark.

## Open questions

- The Buehler act: does XTX become a top-tier *options* market maker (deep hedging productionized),
  and does that show up in OPRA market-share data?
- Does the Finland compute bet mark a transition from many micro-alpha models to fewer, larger
  foundation-model-style price predictors — and would that be visible from outside at all?
- Where does XTX rank in the post-2025 BIS/Euromoney FX structure — is the non-bank share still
  growing, or has the bank/non-bank boundary stabilized?

## Sources (web, as of 2026-07-13)

- [Wikipedia — XTX Markets](https://en.wikipedia.org/wiki/XTX_Markets) · [Wikipedia — Alex Gerko](https://en.wikipedia.org/wiki/Alex_Gerko)
- [Finance Magnates — 2024 results (£1.28B profit, +54%)](https://www.financemagnates.com/forex/xtx-markets-posts-50-profit-jump-to-128-billion-on-trading-surge/) ·
  [2025 results (£3.93B revenue, £1.71B profit)](https://www.financemagnates.com/forex/brokers/xtx-markets-revenue-rises-43-to-393-billion-in-2025/) ·
  [Gerko's £682M 2024 pay](https://www.financemagnates.com/forex/xtx-markets-alex-gerko-earns-682-million-as-profits-jump-54-report/)
- [Bloomberg — 2024 earnings +50%](https://www.bloomberg.com/news/articles/2025-04-04/gerko-s-xtx-markets-mints-3-53-billion-on-global-trading-surge)
- [XTX — Kajaani data-centre announcement (€1B+)](https://files.xtxmarkets.com/publications/kajaani/index.html) ·
  [DCD on the Kajaani campus (25k GPUs, 650PB)](https://www.datacenterdynamics.com/en/news/xtx-markets-to-build-data-center-campus-in-kajaani-finland/)
- [XTX — clients page ("holding risk for meaningful periods")](https://www.xtxmarkets.com/clients/) · [xtxmarkets.com](https://www.xtxmarkets.com/)
