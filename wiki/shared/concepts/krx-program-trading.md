---
type: concept
title: KRX Program Trading (프로그램 매매) — Basket Flow, Not an Investor Type
description: What the HTS 프로그램 매매 table actually measures — a KRX order-flagging classification (차익/비차익 basket flow) orthogonal to the 개인/기관/외국인 investor-type stats; why the two tables overlap, and how traders read arb balance, expiry unwinds, and the sidecar.
tags: [systematic-trading, market-research, microstructure, korea]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: []
---

# KRX Program Trading (프로그램 매매)

The 프로그램 매매 table in a Korean HTS answers a different question from the 개인/기관/외국인
table. The investor-type table tells you **who** traded. The program table tells you **how** the
order was executed — specifically, whether it was flagged as a *basket* order. The two tables
overlap: the same trade can (and usually does) appear in both. That is why they are shown
separately and why you must never add them together.

## What gets flagged

"Program trading" on the KRX is a regulatory classification, not a marketing term. When a broker
submits an order that qualifies, it must be marked as a program order (프로그램매매호가 신고 —
a reporting obligation on the member firm). The exchange aggregates these flags and publishes the
statistics your HTS displays. Two buckets:

**차익거래 (index arbitrage).** Simultaneous, opposite-direction positions in a stock basket and
index derivatives (classically KOSPI200 futures) to capture the basis. When futures trade rich to
fair value, arbitrageurs buy the cash basket and sell futures — this prints as 프로그램 매수차익
(program buy-arb) and puts a mechanical bid under the cash market. When futures trade cheap, the
reverse. Crucially, every arb position opened is an unwind queued for later: the outstanding stock
of these positions is published as the **차익거래 잔고 (arbitrage balance)**, and it concentrates
its unwind into derivatives expiries.

**비차익거래 (non-arbitrage).** Basket trades *without* a derivatives arb leg — simultaneous
same-direction orders across many index constituents at once (the regulatory threshold has been a
basket of 15+ names; the exact definition has been revised over the years, so treat the number as
indicative). In the modern Korean market 비차익 flow is far larger than 차익 flow and is dominated
by foreign passive money. Detail in the next section.

What is **not** program trading: a single-stock algorithmic order, DMA/HFT flow in one name, or an
individual's API bot. "Program" here means *basket*, not *automated*. Equating 프로그램 매매 with
algorithmic trading in general is the most common misreading of the table.

## Inside 비차익 — what the basket flow actually is

The 비차익 print is a mixture of several distinct businesses. Roughly in order of size:

1. **Foreign passive tracking flow.** When money flows into or out of Korea-exposed index products
   abroad — MSCI EM/ACWI mandates, country ETFs like EWY — the executing broker buys or sells the
   Korean basket in Seoul. This is the single biggest component, it arrives via 외국인, and it is
   the reason multi-day one-way 비차익 streaks track global EM allocation shifts. It is
   country-level information, name-level noise.
2. **Index rebalancing events.** MSCI quarterly/semi-annual reviews, FTSE reviews, and the
   KOSPI200's own June/December reconstitutions execute at the closing auction of the effective
   day — enormous, fully pre-announced 비차익 prints concentrated in one auction. Watching the
   day's cumulative 비차익 spike at 15:20–15:30 on a review date is watching the trackers roll.
3. **Domestic ETF liquidity-provider hedging.** When a domestic ETF trades away from NAV, the LP
   trades the ETF against the underlying basket and creates/redeems to flatten. The cash-basket
   legs print as program flow (basket-vs-futures versions can print as 차익 instead). This
   component is intraday, two-way, and mean-reverting — plumbing, not opinion.
4. **Portfolio transitions and mandate moves.** NPS (국민연금) and other pensions/insurers moving
   money between external managers execute via transition baskets — lumpy, multi-day 기관
   (연기금) prints that have nothing to do with a market view at the stock level.
5. **Quant/systematic baskets.** Factor portfolios, stat-arb books, long-short baskets — any
   strategy rebalancing many names simultaneously through a basket engine. This is the one
   component whose *name-level* deviations carry a view: program flow in a stock far out of
   proportion to its index weight suggests a non-index basket touched it.
6. **Derivatives-adjacent hedging that misses the 차익 definition.** ELS/autocallable issuers'
   delta-hedging and index-option hedge adjustments trade mostly futures, but the basket legs that
   do hit cash can print as 비차익.

**The under-reporting caveat — read before trusting the level.** The flag attaches at order
submission, per broker, per linked basket order. A fund executing the *same* basket by slicing it
through per-name VWAP/POV algo orders (which is how much modern execution actually works) does
**not** get flagged. So 비차익 *understates* true basket flow, the understatement has grown as
execution moved from basket engines to algo wheels, and the visible program share of turnover is
partly an artifact of execution fashion. Treat the *sign and streaks* of 비차익 as meaningful, the
*level* as a floor.

**Timing texture.** Passive flow benchmarks to the close, so 비차익 skews to the closing auction
and the final hour; the intraday remainder is mostly VWAP-shaped. A large 비차익 number that
arrived steadily all day reads differently (systematic/transition) from one that landed at the
close (index tracking).

## Program vs. algorithmic trading — the Korean regulatory split

Korea regulates these as two different things. **Program trading** is the basket-reporting regime
described above — it exists so the exchange can see *coordinated multi-name flow*. **Algorithmic
trading** (알고리즘 매매) is about *how orders are generated*, and after the Citadel Securities
case (fined by the FSC in 2023 for 2017–18 high-frequency order patterns routed via Merrill Lynch
that were ruled market-disrupting), KRX moved to require registration of algo-trading accounts and
tightened DMA supervision. A single-name HFT market-maker is algo-registered but never prints in
프로그램 매매; an old-school basket program executed by a human desk prints in 프로그램 매매 but
isn't "algorithmic." The HTS table you watch measures only the former regime.

## Why it overlaps the investor-type table

A foreign index fund buying its KOSPI200 tracking basket shows up **twice**: as 외국인 순매수 in
the investor table and as 비차익 매수 in the program table. Program flow is a *subset* of
(mostly) foreign + institutional flow, viewed through a different lens. The useful decomposition:

- **외국인 순매수 − 비차익 순매수 ≈ discretionary foreign flow.** Crude, but it separates
  "passive/mechanical money arriving in a basket" from "an active foreign manager picking this
  stock." A day where foreign net buying is large but almost all of it is 비차익 is index flow,
  not a stock-specific vote — connect this to
  [informed vs. uninformed flow](informed-vs-uninformed-flow.md): basket flow is close to the
  definition of uninformed (price-insensitive, not name-specific) flow.
- Individuals essentially never appear in program stats; retail doesn't trade flagged baskets.
- Per-stock 프로그램 순매수 (shown in most HTS) is that stock's share of the day's basket flow —
  a mega-cap index heavyweight like Samsung Electronics receives program flow roughly in
  proportion to its index weight regardless of any company-specific news.

## The machinery traders actually watch

**Basis → mechanical flow.** Futures rich → buy-arb baskets lift the cash market; futures cheap →
sell-arb pressure. Program flow is the transmission belt described in
[price formation](price-formation-and-the-float-identity.md) (index-arb transmission): it moves
prices mechanically, at the margin, without anyone forming a view on the individual names.

**Expiry unwinds (만기일).** The arb balance must unwind, and it unwinds into the close of expiry
days — quadruple witching (네 마녀의 날: second Thursday of Mar/Jun/Sep/Dec) being the heaviest.
The closing auction's 예상체결가 swinging violently on an expiry afternoon is program unwind, not
news. The canonical disaster: **Nov 11, 2010 (옵션쇼크)** — Deutsche Bank's Seoul desk dumped
roughly ₩2.4tn of sell-arb baskets into the closing auction, the KOSPI200 fell ~2.7% in the final
ten minutes, and a positioned options buyer collected a fortune. The episode is why program
disclosure and expiry-day rules were tightened afterward.

**The sidecar (사이드카).** If KOSPI200 futures move ±5% and hold it for one minute (±6% on
KOSDAQ150 futures), *program orders only* are suspended for five minutes — the rest of the market
keeps trading. It fires at most once per day per direction and not in the last ~40 minutes. This
is distinct from the circuit breaker (which halts the whole market at −8/−15/−20% on the index).
The buy-side sidecar in the Jul-3-2026 V-day rebound is recorded in
[KRX session clocks & forced liquidation](krx-session-clocks-and-forced-liquidation.md).

**Shrunken 차익, dominant 비차익.** Classic cash-vs-futures index arb thinned out through the
2010s — Korea's securities transaction tax makes the cash leg expensive, so pure 차익 volume is a
shadow of its 2000s self (a live example of [limits to arbitrage](limits-to-arbitrage.md):
a friction, not a free lunch). What remains of the table's information content sits mostly in
비차익: it is the cleanest daily print of passive/index-driven foreign flow the KRX publishes.

## How to read the table, in one paragraph

Treat 프로그램 순매수 as "mechanical basket flow today": 비차익 tells you what passive money did,
차익 tells you what the basis forced, and the 차익잔고 tells you what's queued to unwind at
expiry. Cross it against the investor-type table to split foreign flow into passive vs.
discretionary. Ignore it as a stock-picking signal in index heavyweights (they get their index
weight's share regardless), respect it violently on expiry afternoons, and never confuse it with
"algorithms" in general.

## Honesty flags

- The 15-name basket threshold and reporting definitions have been revised by KRX over time
  (notably mid-2010s); the exact current legal definition was written here from memory and should
  be verified against KRX 업무규정 before being quoted.
- The Nov-2010 옵션쇼크 figures (₩2.4tn, ~2.7% in the final minutes) are from memory —
  order-of-magnitude right, decimals unverified.
- Sidecar parameters (±5%/±6%, 1 minute, 5-minute suspension, once per day, no late-session
  trigger) match the widely cited rule set but KRX has tweaked these historically.
- The Citadel Securities case details (FSC fine in 2023, conduct in 2017–18 via Merrill Lynch, and
  the subsequent algo-account registration push) are from memory; the fine amount and the exact
  scope of KRX's algo-registration rules should be verified before quoting.
- The ranking of 비차익 components by size is a practitioner's judgment call, not a published
  decomposition — KRX does not break 비차익 down by underlying business.

## Relationships

- Transmission mechanics: [Price Formation & the Float Identity](price-formation-and-the-float-identity.md)
- Reading the flow: [Informed vs. Uninformed Flow](informed-vs-uninformed-flow.md)
- Korea-specific session machinery: [KRX Session Clocks & Forced Liquidation](krx-session-clocks-and-forced-liquidation.md)
- Why the arb persists yet stays thin: [Limits to Arbitrage](limits-to-arbitrage.md)
