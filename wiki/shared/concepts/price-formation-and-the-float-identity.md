---
type: concept
title: Price Formation & the Float Identity — Why Prices Move When Nobody Can "Get Out"
description: Every share is always held by someone (the float identity) — so "everyone sold" is impossible and all aggregate adjustment happens in PRICE, not quantity. Price is a mark set by the marginal trade, not a vote of holders — and it can move on zero volume (revised willingness moves price; trades only test it). The recruitment mechanism (order-book ladder, urgency asymmetry, depth withdrawal); "more sellers than buyers" really = "sellers more urgent than buyers," and the concession they pay = an immediacy fee + adverse-selection premium. The machinery (execution algos & the √-impact law, flat-book market makers who transmit rather than absorb, internalization, ETF/index-arb transmission, dealer hedging, margin reflexivity, the auctions). Why tiny net flow moves price hugely (inert float → steep short-run demand; inelastic-markets ~5×). Temporary impact reverts, permanent (information) impact doesn't — the whole flush-buying edge and its risk in one line.
tags: [systematic-trading, derivatives, microstructure, market-research, behavioral]
timestamp: 2026-07-02T00:00:00Z
status: active
sources: []
---

# Price Formation & the Float Identity — Why Prices Move When Nobody Can "Get Out"

The paradox: institutions own ~80% of a name like MU, so they cannot collectively "sell their
position" — yet the price falls 13% in a day. The resolution requires separating two things markets
blur together: **trades (flows)** and **prices (marks)**. Price is not a measurement of how much was
sold; it is the *current terms of exchange* — and it can move with no trading at all.

## 1. The float identity — all adjustment happens in P, none in Q

MU has ~1.1B shares outstanding. Every second of every day — before, during, and after any crash —
each share sits in someone's account. The aggregate market **cannot reduce its holdings**; it can
only pass them around. (Two precise boundaries, for honesty: the **issuer** can change Q — buybacks,
issuance, cash M&A are the one true aggregate exit/entry — but slowly, quarters not days; and
**short selling** creates gross long positions above N while *net* exposure stays exactly N — the
lender, the new buyer, and the short net to one holder per share. Derivatives likewise net to zero
between counterparties. The identity is a **net, ex-issuer** statement, which is all the argument
needs.) So when quantity is fixed, a change in aggregate *willingness to hold* has
exactly one variable left to adjust: **price must move until the marginal participant is again
willing to hold every share.** "A selloff is a redistribution between cohorts at whatever price
recruits the next willing holder" is this identity in one sentence — and on a −13% day, printed
volume might be 3–5% of the float, most of it the *same* shares hot-potatoed between intermediaries;
the durable handoff is often ~1–2%. **95%+ of holders did nothing, yet every account is marked down
13%** — because price is a mark, not a vote.

## 2. Price is a mark set at the margin — and it moves without trades

The visible price is just the last print (or the current best bid/ask midpoint). It reprices two
ways:
- **Repricing (volume-free):** news breaks; every bidder lowers their bid and every holder raises or
  lowers their reserve. The quote gaps with zero volume — overnight gaps and opening indications do
  this literally (Jul-1 US trade repriced Samsung/SK Hynix holders' wealth hours before Seoul
  opened; on **Jun-23 the KOSPI circuit breakers twice paused matching entirely** while willingness
  kept collapsing — prices reopened lower with no intervening trades). *Corrected on same-day
  verification: the Jul-2 **sidecar** is only a 5-minute program-trading pause, not a matching halt
  — this page originally mis-cited it.* This is pure
  [expectations revision](mispricing-and-expectations.md).
- **Flow (paid-for):** some holders must convert shares to cash *now* (margin, mandate,
  quarter-end). Their urgency consumes the order book and pays a concession to whoever supplies
  immediacy.

Every selloff is a mix of the two. The Jun-23-2026 flush was mostly flow (forced leveraged-ETF
unwind); the Jul-1 Meta-Compute day was mostly repricing plus a momentum-cohort flow tail — the
tripwires stayed 0-of-8
while the multiple moved.

## 3. The recruitment mechanism — the order book, literally

At any moment there is a ladder of *conditional* commitments:

```
          asks (resting offers)
 $1,100.40   1,200 sh
 $1,100.20     900 sh
 $1,100.00     600 sh   ← best ask
 ─────────────────────────────────
 $1,099.80     700 sh   ← best bid
 $1,099.60   1,100 sh
 $1,099.20   2,400 sh
          bids (resting orders)
```

A market sell of 5,000 shares eats the top bid rungs and prints down the ladder; "the price fell"
means *the remaining best bid is lower*. Three facts turn this into crashes:
1. **Depth near the touch is microscopic vs the float** — thousands of shares quoted against a
   billion outstanding. Price is set in the flow market and applied to the stock of holdings.
2. **Depth is withdrawn exactly when needed** — in stress, bids are pulled faster than they are
   consumed (E-mini top-of-book −33% m/m into Jul-1). Same selling, thinner ladder, bigger move.
   Illiquidity is a price multiplier.
3. **"More sellers than buyers" — *executed* quantities are always equal; *desired* quantities are
   not.** At the old price, desired sales exceeded desired purchases — this is literally measurable
   (exchanges publish auction *imbalance* data); price adjusts until desired quantities match, and
   only the matched part ever prints. On top of the quantity imbalance sits the **urgency**
   asymmetry: sellers cross the spread while buyers post conditional bids lower. The day's low is
   the level where cumulative willing demand met the supply that *had to* move that day — an
   auction sliding down a demand curve; nothing more mystical.

**Why buyers demand a concession at all:** immediacy has a cost (inventory risk) and the seller
might know something (adverse selection — the lemons discount; Glosten-Milgrom). The flush
discount = an insurance premium against catching an *informed* knife. If the flow turns out
mechanical, the discount was a free fee to the buyer (the [who-pays-you](who-pays-you.md)
Constraint payer); if informed, it was insufficient (the torpedo). **Ex-ante you cannot fully tell**
— the [identification problem](informed-vs-uninformed-flow.md); breadth is the cheapest tell.

## 4. What Wall Street actually does all day (the machinery)

- **Buy-side execution:** a pension selling 2M shares does not send a market order. A desk slices
  the parent order (VWAP/POV ~10% of volume, icebergs, dark pools, or a block *risk bid* from a
  bank). Impact cost scales ~√(order size / daily volume) — the square-root law — which is *why*
  institutional unwinds take days-to-weeks and have the measurable cadence the
  [unwind research](../../market-research/positioning/unwind-duration-and-flows-2026-06-30.md)
  documented.
- **Market makers / HFT** (Citadel Securities, Virtu, Jane Street, bank desks): flat-book inventory
  recyclers earning the spread. They buy from the urgent seller, hold seconds-to-minutes, and
  re-offer — and when flow is one-way they don't absorb it, they **mark price down and widen** so
  someone else is recruited. They *transmit* pressure; they are the shock's wiring, not its floor.
  ~40–50% of US volume executes off-exchange (retail internalization, dark crossing).
- **Derivatives desks:** mechanical delta-hedging of the options book — long-gamma dampens
  (buy dips / sell rips), short-gamma amplifies; post-print IV-crush unwinds hedges (supportive).
  Direction is estimate-grade from outside (the Jun-30 run left semis dealer-gamma *unresolved*).
- **ETF/index arbitrage — how Seoul reaches Boise:** SMH/SOXX selling → AP redemptions → the basket
  is sold → MU is offered with zero MU-specific news. Futures/cash/ETF arb welds everything into
  one global book, and global funds treat the memory complex as **one trade** — MU doubling as the
  most liquid US pure-memory expression (SK Hynix's US ADR only lists ~Jul 10). Nobody "decides"
  to sell MU on a Korea headline; the plumbing does it.
- **Prime brokerage — the reflexive layer:** marked prices feed collateral values, VaR, and stops;
  a flow-driven markdown *creates* margin calls and de-gross demands, i.e. more flow
  (price ↓ → collateral ↓ → forced sells → price ↓). This is why mechanical selloffs **overshoot
  fair value and then V-reverse**: price-insensitive selling doesn't stop at "cheap," it stops when
  the *constraint is satisfied* — and that overshoot is precisely the payer moment.
- **The auctions:** the open and (especially) the close — the deepest single-price liquidity events
  of the day (~10% of volume; far more on rebalance days). Rebalancers and
  [leveraged-ETF machinery](leveraged-etf-decay.md) trade there by design.

## 5. Why tiny net flow moves price so much

Most of the float is **inert**: indexers hold regardless of price, mandates cap deviations,
insiders are locked. The price-elastic crowd — the only people whose bids form the short-run demand
curve — is thin. Hence steep demand curves: the inelastic-markets estimate (Gabaix–Koijen) is that
$1 of net flow moves ~$5 of aggregate market value (a **macro** multiplier — single-name *permanent*
demand multipliers are far smaller, nearer ~1×, per the index-inclusion literature), and purely
informationless demand demonstrably moves single names. **Corrected arithmetic** (the original toy
over-attributed): the pension's 2M-share block — ~10% of one day's volume, spread over a week —
costs on the order of **0.5–1.5%** by the √-law on a 5–6%-daily-vol name, *mostly temporary*. A −7%
week is therefore never one order's doing; the marked swing is dominated by the **volume-free
repricing component plus every cohort's simultaneous flow.** The honest, *measured* version of the
marked-to-flow gap is the Jul-2 tape: Samsung's one-day marked loss was ~₩170T (common shares alone)
against **₩1.63T of total market-wide foreign net selling** — even attributing every won of it to
Samsung, the marked wealth change outran the net flow ~**100:1**. The reconciliation of that gap is
impact decomposition: **temporary impact (liquidity concession) reverts; permanent impact
(information) doesn't.** The
Jun-29 V-reversal ($1,023.65 low → $1,145.28 close) was temporary impact unwinding within hours of
supply exhaustion; a genuine demand crack would not have V'd. That one line — *temporary reverts,
permanent doesn't, and you can't perfectly tell which you're holding* — is simultaneously the
mean-reversion edge, its tail risk, and the case for
[sizing + falsifiers over conviction](../../synthesis/navigating-nonlinear-markets.md).

## Worked example (dated — the June–July 2026 memory tape)
- **Jun-23:** Korea FSS warning → leveraged single-stock-ETF cohort forced to de-lever →
  mechanical selling in Seoul → arb/proxy transmission → MU −13.18% *in lockstep with the complex*
  (breadth = the mechanical signature) while BofA **raised** MU to $1,500 the same day — the view
  layer and the flow layer visibly disagreeing.
- **Jun-29:** morning flush undercuts the prior panic low, forced supply finishes, no new supply at
  the low → patient bids + short-covering + MR algos reprice the discount within hours: +1.14%
  close. Supply exhaustion, printed.
- **Jul-2 (Korea):** the redistribution with receipts — **foreign −₩1.63T, retail +₩1.28T (KOSPI-wide
  session prints)** on a day Samsung fell −9.06% and SK Hynix −14.57%: shares moved from foreign
  institutional accounts to Korean retail (and domestic institutional) accounts at whatever prices
  recruited them. The float identity, measured by cohort.

## Same-day verification (2026-07-02) — challenged, re-derived, four walk-backs

The user pushed back ("are you sure?"); a first-principles re-derivation **confirmed the core**
(the float identity as a *net, ex-issuer* statement; marks-at-the-margin; imbalance + urgency
clearing; steep short-run demand; temporary-vs-permanent impact) and caught four overclaims, now
corrected in place above:
1. **Sidecar ≠ matching halt.** Korea's sidecar pauses *program-trading orders* for 5 minutes; the
   true zero-volume-repricing examples are the Jun-23 circuit breakers and any overnight gap.
2. **"Trades don't move price" was oversharp** (and contradicted the √-impact law cited later).
   Trades *do* move price — mechanically through depth, and informationally because order flow is
   read as evidence (Kyle's λ; Glosten-Milgrom): impact largely **is** belief revision caused by
   observing flow. The survivable claim: price needs no trades to move, and trades move it *by
   changing willingness* (inference + inventory), not via a conserved "selling pressure."
3. **The toy's causal attribution was inflated** — the √-law prices the 2M-share block at ~0.5–1.5%
   impact, not 7 points; replaced with the measured Samsung **~100:1** marked-to-flow ratio, which
   makes the point *more* strongly with honest numbers.
4. **Boundary conditions added to the identity** (§1): issuer actions (buybacks/issuance/cash-M&A)
   are the one true aggregate exit/entry, on a slow clock; shorting raises *gross* long positions
   while net exposure stays exactly N.

## Relationships
- **Who the cohorts are and who ends up paying:** [who pays you](who-pays-you.md) · the pools and
  clocks: [who sets price](who-sets-price.md).
- **Reading flow vs information on the tape:** [informed vs. uninformed flow](informed-vs-uninformed-flow.md)
  · [distribution & pullback tells](distribution-and-pullback-tells.md).
- **The event-scale anatomy these mechanics produce — straight crash legs, overshoot, and the
  same-day V:** [liquidity cascades & V-reversals](liquidity-cascades-and-v-reversals.md).
- **The costs this machinery charges you:** [transaction costs & market impact](transaction-costs.md);
  the microstructure canon: [Cartea–Jaimungal–Penalva](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md).
- **Why the elastic crowd is small:** [limits to arbitrage](limits-to-arbitrage.md).
- **The edge this mechanics implies for a small account:** buy-the-flush mean reversion —
  [small-account edge map](../../synthesis/retail-capital-edge-map.md) #1 — with the temporary-vs-
  permanent caveat above.
- Graduated from Part 3 of the captured discussion:
  trading fundamentals Q&A (2026-07-02).

## Open questions
- Can temporary vs permanent impact be *estimated live* for a single name (e.g., reversion half-life
  by flow-cohort type), rather than classified only after the bounce?
- How much of MU's daily beta to the Korea complex is arb plumbing vs shared-fundamental repricing —
  measurable via overnight-gap decomposition?
