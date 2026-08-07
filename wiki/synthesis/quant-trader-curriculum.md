---
type: overview
title: The Quant Trader's Curriculum — What to Learn, Ranked by ROI
description: Every topic a winning quant trader needs, ranked by return on study time — built for a long-term tech holder who wants to read short-term action instead of being swept by it.
tags: [systematic-trading, derivatives, ml-stats, curriculum, learning-roadmap]
timestamp: 2026-07-04T00:00:00Z
status: active
sources: []
---

# The Quant Trader's Curriculum — What to Learn, Ranked by ROI

Filed 2026-07-04 from a session Q&A. Written for this desk: long-term theses in technology
stocks, a KRX + US footprint, an engineering background, and one recurring frustration —
getting swept by short-term swings and only understanding them after the fact.

## The diagnosis

If you hold fundamental theses but keep getting blindsided by short-term moves, the problem is
usually not that you know too little about the companies. It is that short-term price action is
written in a different language than value: **flows, positioning, and expectations**. Over hours
to weeks, price mostly moves because someone has to trade — not because the business changed.
See [who sets price](../shared/concepts/who-sets-price.md) and
[price formation and the float identity](../shared/concepts/price-formation-and-the-float-identity.md)
for the mechanics behind that claim.

So this curriculum front-loads the topics that teach you to read *who has to trade, when, and at
what size*. The ranking rule: how much a topic improves your results, times how long the
knowledge stays true, divided by the hours it takes to learn. The result is deliberately
unglamorous. The highest-ROI topics are the ones most traders skip on their way to the exciting
stuff — which is exactly why they still carry edge (see
[who wins — the empirical record](../shared/concepts/who-wins-empirical-record.md)).

One warning before the list: topics are raw material. What actually makes someone world-class is
the practice loop at the end of this page, run against these topics for years.

---

## Tier 1 — the core five

Do these first. Roughly 60% of the result for 20% of the effort.

### 1. Risk management and position sizing

First because it is the only topic where ignorance kills the account, and also the cheapest to
learn. The graveyard is full of traders with the right thesis and the wrong size.

What to learn:

- The difference between expected value and expected *growth*: volatility drag, why a 50% loss
  needs a 100% gain, and why oversizing turns a winning strategy into a losing one. See
  [risk of ruin](../shared/concepts/risk-of-ruin.md).
- The [Kelly criterion](../shared/concepts/kelly-criterion.md), and why in practice everyone
  sane runs a fraction of it: your edge estimate is always noisier than you think.
- Correlated-bet accounting. A book of AI and semiconductor names is not ten positions; it is
  roughly one bet with ten tickers. Cluster limits and portfolio heat follow from that.
- The two-book firewall: long-term thesis capital and short-term trading capital get separate
  rules, separate sizes, separate exits. The classic blowup of a thesis holder is averaging a
  trading loss into "long-term conviction." Write the boundary down before you need it.
- Stops as invalidation levels — the reason for the trade broke — rather than round percentages,
  and where stops don't belong at all. See
  [stop-losses and exits](../shared/concepts/stop-losses-and-exits.md).
- Back-solving: start from "the biggest drawdown I can survive, financially and psychologically,"
  and derive position sizes from it.

Budget 40 to 60 hours to competence, then discipline forever; it pays back the first time it
stops you from oversizing. Start with *The Missing Billionaires* (Haghani & White), *Systematic
Trading* (Carver), and *Fortune's Formula* (Poundstone). This wiki's
[Navigating Nonlinear Markets](navigating-nonlinear-markets.md) covers the same ground from the
survival side. You have this topic when your worst drawdown is a number you chose in advance,
not one you discovered.

### 2. Positioning and flows — who is forced to trade

The single highest-leverage topic for the original complaint. Most violent short-term moves are
not opinion changes; they are mechanical, and mechanical flows can be anticipated in direction,
rough size, and timing. The core skill: for any move of 2% or more, split it into who *had* to
trade and who *chose* to.

What to learn:

- Dealer gamma. Market makers who sold options must hedge. When they are short gamma, their
  hedging pushes price in the direction it is already going; when long gamma, it dampens moves.
  Learn the monthly expiration calendar, and the newer 0DTE intraday version of the same loop.
- Systematic funds with public rulebooks: volatility-target funds mechanically sell the day
  after realized volatility rises; trend followers (CTAs) have flip levels that banks publish;
  risk parity de-levers when stocks and bonds fall together; leveraged ETFs rebalance at the
  close in the direction of the day's move (see
  [leveraged-ETF decay](../shared/concepts/leveraged-etf-decay.md) — large in semis).
- Margin cascades and forced liquidation. This desk has already mapped the Korean version in
  detail: [KRX session clocks and forced liquidation](../shared/concepts/krx-session-clocks-and-forced-liquidation.md)
  and [liquidity cascades and V-reversals](../shared/concepts/liquidity-cascades-and-v-reversals.md).
  Add short-squeeze plumbing: borrow cost, recalls, days to cover.
- Calendar flows: buyback blackout windows before earnings (the corporate bid disappears exactly
  when event risk peaks), month- and quarter-end pension rebalancing, index adds and deletes,
  lockup expiries.
- Reading positioning data, and its limits: futures positioning (COT), put/call ratios and skew
  as crowding gauges, short interest, and KRX investor-type flows — see
  [informed vs. uninformed flow](../shared/concepts/informed-vs-uninformed-flow.md) and the live
  worked example in the
  [Jun-2026 unwind duration note](../market-research/positioning/unwind-duration-and-flows-2026-06-30.md).

Budget 80 to 120 hours of study plus a quarter of daily observation; within one or two expiry
cycles, "no news" moves stop being mysteries. Start with Corey Hoffstein's *Liquidity Cascades*
(free, and almost written for this exact question), SqueezeMetrics' gamma papers, *The Rise of
Carry* (Lee, Lee & Coldiron), and Mike Green's work on passive flows. You have this topic when
an 8% no-news drop in one of your names stops feeling like injustice: within an hour you can
name the two or three most likely mechanical sellers and what would confirm each. Note that
Signal C in [Engine v3](engine-v3/index.md) is this topic turned into code — evidence that this
desk's edge already lives here.

### 3. The expectations game — what is priced in

Price is not a fact about the company; it is a bet about expectations. "Great quarter, stock
down 12%" only confuses people who compare results to the past instead of to the priced-in
future. This is the interface between the long-term theses and short-term price. See
[mispricing and expectations](../shared/concepts/mispricing-and-expectations.md).

What to learn:

- Reverse-engineering the expectations embedded in the current price (Mauboussin's reverse-DCF
  discipline), so your thesis is always stated *against* the market, not in a vacuum.
- The earnings machine: consensus versus whisper numbers, the guidance walk-down game, why
  crowded longs sell off on good news, and post-earnings drift when the market underreacts.
- The implied move: read the straddle before every known event, compare it to your own scenario
  range, and grade yourself afterward. This is the cheapest calibration practice in trading —
  the Micron print post-mortem
  is exactly this rep.
- Estimate-revision dynamics: revision breadth and momentum, and how sell-side updates propagate.
- Reflexivity and the narrative lifecycle: ignition, amplification, crowding, exhaustion, unwind.
  In technology, reflexivity is real — price changes hiring, capital access, and customer
  confidence. Exhaustion tells are cataloged in
  [distribution and pullback tells](../shared/concepts/distribution-and-pullback-tells.md).
- Catalyst mapping: keep a calendar of known events, and hold separate rules for pre-positioning
  versus reacting. The [V-day checklist](../systematic-trading/checklists/catching-the-v-day-checklist.md)
  and the [new-high checklist](../systematic-trading/checklists/new-high-trade-checklist.md) are
  the operational ends of this topic.

Budget 60 to 100 hours plus two earnings seasons of deliberate reps. Start with *Expectations
Investing* (Mauboussin & Rappaport) and *The Alchemy of Finance* (Soros, for reflexivity). You
have this topic when the post-print move rarely surprises you, even when it costs you money.

### 4. Market microstructure and plumbing (US and Korea)

The substrate under topics 2 and 3: how trading actually works determines how moves travel.

What to learn:

- The limit order book: queue priority, adverse selection, why liquidity vanishes exactly when
  you need it, and why "stop hunts" are mostly mechanical liquidity events, not conspiracies.
- Auctions: opening and closing auction mechanics and imbalance information, and why the close
  is the institutional benchmark. KRX specifics: call auctions, VI halts, the ±30% daily limits,
  the forced-liquidation morning sequence, and the recurring short-sale ban regimes — much of
  this is already mapped in
  [KRX session clocks](../shared/concepts/krx-session-clocks-and-forced-liquidation.md).
- Cross-asset plumbing: futures lead cash; ETF creation and redemption; premiums and discounts.
- Time-of-day structure: overnight versus intraday returns, the 10:00 Korea inflection, opening
  ranges, witching days.
- Modern tape reading: volume profile, VWAP behavior, block prints, retail flow signatures.
- Short-sale plumbing: locates, borrow fees, recalls, buy-ins.

Budget 100 to 150 hours plus screen time; exchange mechanics change slowly, so this knowledge
barely depreciates. Start with *Trading and Exchanges* (Harris — still the standard), *Algorithmic
Trading and DMA* (Johnson) for practical plumbing, and the KRX rulebook itself: reading primary
exchange rules is an underrated edge. You have this topic when you can narrate the session as it
happens — why it gapped, why 10:00 turned it, what the closing auction will do — and be right
more often than not.

### 5. Statistics as self-defense

Not academic statistics. Protection against the number-one quant failure mode: believing your
own noise. The engine work makes this urgent, not optional.

What to learn:

- Fat tails and volatility clustering: what breaks when returns are not normal — Sharpe ratios,
  stop distances, mean estimates.
- Bayes and base rates: how to evaluate "crash signals" that fire constantly.
- Effective sample size: how many *independent* bets a backtest really contains. A ten-year
  daily backtest may hold only a handful of true observations of the thing that matters.
- Multiple testing: why the thirtieth variant you try "works," deflated Sharpe ratios, and
  pre-registration. The falsifier habit already used on this desk (the checklists, the H6
  hypotheses) is the same discipline under another name.
- Nonstationarity: why strategies decay, and why parameter plateaus beat parameter peaks.
- Monte Carlo and bootstrap for the questions that actually matter: drawdown distributions,
  and "could this be luck?"

Budget 100 to 150 hours given existing coding skill, then continuous use. Start with
*Evidence-Based Technical Analysis* (Aronson — the best book on data-mining bias in trading),
*Fooled by Randomness* (Taleb), and the validation chapters of *Advances in Financial Machine
Learning* (López de Prado), which are valuable even if you never run ML. You have this topic
when your reflex questions for a Sharpe-2 backtest are: how many independent bets, how many
things were tried, and which regime carried it.

---

## Tier 2 — the craft

**6. Volatility and options literacy.** Even if you never trade options, volatility is the
market's native language for risk, and you cannot read dealer flows (topic 2) or implied moves
(topic 3) without it. Learn the greeks as practical objects, the volatility surface and why
equity skew exists, implied versus realized volatility and the variance risk premium, the VIX
complex and its feedback loops (February 2018 is the case study), and how to read options data
as the market's published probability map. For this book specifically: collars and put spreads
as a hedging overlay, and why covered calls on high-growth names quietly sell the exact right
tail the thesis depends on. Budget 100 to 150 hours. Start with Natenberg (*Option Volatility
and Pricing*), then Sinclair (*Volatility Trading*).

**7. Research methodology and backtesting hygiene.** The craft of not fooling yourself,
applied. Hypothesis-first workflow with a required economic mechanism —
[who pays you](../shared/concepts/who-pays-you.md), and why do they keep paying? Point-in-time
data, survivorship, look-ahead traps, session alignment across KRX and US; walk-forward and
purged cross-validation; honest cost models (see
[transaction costs](../shared/concepts/transaction-costs.md) and
[cost-aware trading](cost-aware-trading.md)); regime slicing; pre-registered kill criteria; and
a paper-to-small-live graduation protocol. [Engine v3](engine-v3/index.md) and
[trading-system fundamentals](trading-system-fundamentals.md) are this topic in practice on this
desk. Budget 60 to 100 hours of study — the real cost is the discipline.

**8. Market history as a pattern library.** The cheapest wisdom per hour on this list. Method:
one page per episode — the setup (crowding, leverage), the spark, who was forced, how it spread,
what stopped it, and the false lesson people took away. Core set: 1929; 1987 portfolio insurance
(the direct ancestor of today's vol-target flows); 1997–98 Asia and LTCM (Korea's own crucible);
the 2000–02 dot-com bust (this sector's blueprint: real companies, 90% drawdowns); 2008; the
2010 flash crash; the 2010 Kospi "11/11" options-expiry crash; February 2018 Volmageddon; March
2020; GameStop 2021; Archegos; the 2022 rate-driven repricing of tech; SVB 2023; the August 2024
yen-carry unwind; and the 2025–26 episodes this desk traded live — the DeepSeek capex scare, the
tariff shock, and the Jun–Jul 2026 memory unwind (see the
[unwind duration and flows note](../market-research/positioning/unwind-duration-and-flows-2026-06-30.md)).
Budget 60 to 100 hours of reading spread over months. Start with *Devil Take the Hindmost*
(Chancellor), *When Genius Failed* (Lowenstein), and *A Demon of Our Own Design* (Bookstaber).

**9. Macro and liquidity regimes.** Hard rule: regime *identification* is high ROI; macro
*forecasting* is negative ROI. Learn real versus nominal rates and why duration compresses
growth multiples — and the limits of that model (2023–24: rates stayed high and the AI narrative
won anyway). Central-bank plumbing heuristics, credit spreads as the adult in the room, the
yen-carry channel into tech, CPI and FOMC event mechanics, and stock-bond correlation regimes.
The Korea angle is an advantage: monthly Korean export data is a genuinely leading indicator for
the global semiconductor complex, published in this timezone. Budget 60 to 100 hours plus a
couple of hours a week ongoing. Start with *Capital Wars* (Howell) and Dalio's debt-crisis
template, then move to primary sources.

**10. Psychology as process.** Two halves. Defense: your own biases, handled structurally
rather than by willpower — the [disposition effect](../shared/concepts/disposition-effect.md),
recency, and the thesis-holder's disease where every headline confirms the thesis. The working
countermeasures are a decision journal with pre-written falsifiers, post-loss size lockdowns,
and a quarterly rewrite of each thesis from scratch. Offense: other people's biases are where
durable patterns come from — underreaction (drift), herding (momentum), extrapolation (cycle
tops). Budget 20 to 40 hours of reading; all of the value is in the protocols. Start with *The
Hour Between Dog and Wolf* (Coates) and *Thinking in Bets* (Duke).

---

## Tier 3 — multipliers, and this desk's specific edges

**11. Korea market structure and flow data.** Treat this as Tier 1 for the KRX book, because it
is the moat. KRX publishes daily investor-type flows per name — an information advantage US
traders simply do not have. Learn foreign-flow persistence, the Kospi200 derivatives ecosystem,
won sensitivity channels, MSCI review flows, the value-up reform trade, and Korean retail
theme-rotation as an adversary model. The 반대매매 and KOFIA margin work already done here is the
right thread; keep pulling it. Primary sources are the edge — no canonical book exists.

**12. Portfolio construction and hedging for a concentrated book.** The applied question: how
does a concentrated, correlated tech book survive its own drawdowns without selling the thesis?
Honest correlation math (the effective number of bets in the book), index puts versus collars
versus simply trimming, the tax asymmetry (Korea taxes overseas-equity gains at about 22% above
a small annual exemption, which materially changes hedge-versus-sell arithmetic), and the basis
risk of hedging US exposure with Korean instruments. Budget 40 to 60 hours. *Expected Returns*
(Ilmanen) for depth, Carver for practice.

**13. Tech-sector mechanics — the fundamentals-to-price interface.** Not "learn tech"; that
knowledge is already here. Learn the machinery that turns tech facts into price: the
semiconductor cycle loop (capex to capacity to price to inventory), memory spot versus contract
and HBM allocation, hyperscaler capex guidance as the master variable, per-company guidance
norms, revision breadth, and inventory as a cycle tell. The
[semiconductor monitoring system](semiconductor-monitoring-system.md) and the
H2-2026 navigation playbook already
operate this. Budget about 50 incremental hours. *Chip War* (Miller) for structure; filings and
earnings calls as primary sources.

**14. Execution and transaction costs.** Implementation-shortfall thinking, limit-versus-market
policy by liquidity regime, auction usage on KRX, and the free money: measuring your own
slippage. Small at current size; grows with size. See
[cost-aware trading](cost-aware-trading.md) and
[transaction costs](../shared/concepts/transaction-costs.md). Budget 20 to 40 hours.

**15. Data landscape literacy.** Know the menu: what exists (tick data, options flow, short
interest, 13F filings, ETF flows, borrow rates, alternative data), what it costs, what is free
(KRX and KOFIA give this desk more than most US retail gets), and what professionals see that
you don't — so you can model your blind spots instead of being surprised by them. Budget 20 to
30 hours.

**16. Machine learning, properly scoped — gated behind topic 7.** The honest hierarchy for a
solo quant: first regime classification feeding signal gates; then meta-labeling, where a model
filters and sizes rule-based signals rather than inventing them (a natural fit for Signal C's
triggers); then language models for extracting deltas from filings and transcripts, validated
like everything else. Never let ML originate the hypothesis — nonstationary, low signal-to-noise
data destroys naive fits. Deep networks on raw prices: skip. Budget 100+ hours when its turn
comes, not before.

**17. Adversarial thinking.** A stance more than a topic: who is on the other side of this
trade, and why are they there? Adverse selection on your limit fills, the crowded-trade game
(consensus is dangerous when positioning capacity is exhausted — measurable with topic 2), and
stop-cluster mechanics. Six months of serious poker is legitimate training for sizing under
uncertainty and tilt control. *The Mathematics of Poker* (Chen & Ankenman) if you want it formal.

---

## Tier 4 — know the shape, skip the depth

One weekend each, no more:

- **Deep derivatives pricing theory** (stochastic calculus, exotics): months of effort, near-zero
  P&L for this seat. The greeks as actually used come from Natenberg and Sinclair.
- **HFT and latency engineering**: unwinnable from this seat; the conceptual fluency you need
  comes free with topic 4.
- **Classical technical-analysis taxonomy** (Elliott waves, Gann, harmonics): the useful tenth —
  levels as stop clusters, volume, trend versus range, VWAP behavior — already lives inside
  topics 2 and 4, with real mechanisms attached.
- **Academic portfolio theory** beyond the hedging needs of topic 12, and factor-model deep dives
  beyond knowing the book's own exposures (long-duration growth, high beta, momentum — and when
  momentum crashes; see [factor premia and alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md)).
- **Crypto microstructure** (unless it gets traded) and exotic alternative data.

## The anti-curriculum — negative ROI, actively avoid

- **Macro forecasting as an edge.** Predicting the Fed or calling recessions means competing
  with people who are also wrong, but cheaper. Identify the regime; don't forecast it.
- **News-flow trading without a mechanism framework.** Maximum activity, zero accumulation. News
  matters only through the lens of "who is now forced to do what."
- **Guru and flow-copying services consumed as answers** rather than as raw data. Builds
  dependency, not skill.
- **Indicator stacking** and pattern-taxonomy collecting.
- **The platform trap:** over-engineering trading infrastructure before a single edge is
  validated. For an engineer this is the most seductive failure mode of all. The current
  spec-and-tests discipline is right; resist generalizing the engine before Signal C proves out
  live.
- **Research that never trades.** Paper-perfectionism. Small live size produces data nothing
  else can.

## A 24-month sequence

This was the patient default, kept for reference. The desk rejected the timeline and chose
compression instead: see the July-2026 sprint — the same curriculum run
at 10+ hours a day for one month, with live reps and graded exit criteria.

- **Months 0–3:** written risk constitution in force (sizing rules, cluster limits, the two-book
  firewall, uncle points). Flows literacy plus a daily 15-minute flow journal. Natenberg-level
  options.
- **Months 3–9:** Harris plus the KRX primary documents. The expectations machinery through two
  earnings seasons, with implied-move checklists written before each print. Statistical
  self-defense, retro-fitted onto the engine's backtests.
- **Months 9–18:** Sinclair-level volatility. Methodology hardening (purged cross-validation,
  deflated Sharpe, kill criteria) applied to Engine v3. One crisis one-pager per week. A
  macro-regime dashboard.
- **Months 18–24:** the Korea flow edge productionized. A hedging overlay live on the thesis
  book. Meta-labeling experiments. The teach-back test: write the synthesis page — if it won't
  write clearly, it isn't owned yet.

## The loop that turns topics into skill

World-class is a practice pattern, not a reading list:

1. Every week, take the move that most surprised you and reconstruct it with the Tier-1 toolkit
   until the explanation is mechanical — named actors, named flows, named expectations gap.
   File it.
2. Before every known event, write down the implied move and your own distribution; grade
   yourself afterward.
3. Every "swept" moment becomes a named pattern within 24 hours. The
   Micron post-mortem and
   the [V-day checklist](../systematic-trading/checklists/catching-the-v-day-checklist.md) are
   exactly this practice — keep it.
4. Everything trades at a size chosen by topic 1, including experiments.

Two years of that loop, stacked on this desk's three real advantages — Korea data fluency,
genuine tech-domain depth, and engineering discipline — is a credible path to world-class,
because that combination is rare even inside funds. Nothing guarantees winning. The ranking
simply puts the effort where the swept crowd never looks; the order is the edge.

## Relationships

- [Trading-system fundamentals](trading-system-fundamentals.md) — the Edge × Risk ×
  Implementation frame this curriculum feeds.
- [Navigating nonlinear markets](navigating-nonlinear-markets.md) — the survival-first
  philosophy behind Tier 1.
- [Semiconductor monitoring system](semiconductor-monitoring-system.md) — topics 2, 3 and 13
  wired into a live dashboard.
- [Engine v3](engine-v3/index.md) — topics 2, 5 and 7 turned into code.
- Quant/engineer proof-of-value program — the career
  companion: same skills, viewed as evidence for doors.
