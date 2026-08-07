---
type: concept
title: KRX Session Clocks & Forced Liquidation (반대매매) — Why Korean Panic Mornings Bottom Around 10:00
description: The Korea-specific machinery under intraday V-reversals. Margin shortfalls are measured at each day's close, saved overnight, and force-sold at the NEXT morning's opening auction (D/D+1/D+2 conveyor belt, limit-down-priced orders, systematic overselling) — so a crash day manufactures the next morning's selling rather than executing its own. Around 10:00 KST three clocks converge — forced supply exhausts, execution algos rotate off the opening volume spike, Taiwan (TSMC) opens — which is why panic mornings so often turn there. Worked example - the July 3, 2026 KOSPI V (low 7,378 → buy-sidecar → close +5.37%).
tags: [systematic-trading, market-research, microstructure, korea, tail-risk]
timestamp: 2026-07-03T00:00:00Z
status: active
sources: []
---

# KRX Session Clocks & Forced Liquidation (반대매매) — Why Korean Panic Mornings Bottom Around 10:00

The [liquidity-cascades page](liquidity-cascades-and-v-reversals.md) explains *why* forced flow
prints straight legs that reverse abruptly: a flow-driven move ends at a **quantity**, not a
price, so price turns the moment the forced quantity runs out. This page explains the
Korea-specific machinery that decides *when* that quantity runs out — and why, on the Korean
market, the answer is so often "around 10:00 in the morning."

The short version: **Korean margin liquidation is measured at the close and executed at the next
open.** A crash day does not execute its own margin calls; it *manufactures a list* that gets
force-sold at the following morning's opening auction. That scheduling rule, plus two other
clocks that tick at the same hour, makes ~10:00 KST a recurring inflection point on panic
mornings.

## Part 1 — The forced-liquidation conveyor belt

"반대매매" (*bandae-maemae*, literally "opposite trade") is the broker force-selling a client's
shares to recover money the client owes. There are two kinds, and both run on a fixed calendar.

### Kind 1: unpaid settlement balances (미수거래)

An investor can buy shares putting up only part of the cash, owing the remainder on settlement
day (T+2). If the balance is unpaid, the broker force-sells on the **morning of T+3**: the order
is submitted automatically before the market opens and fills as a market order in the 9:00
opening auction.

### Kind 2: margin loans (신용거래) — the one that matters in crashes

This is stock bought with money borrowed from the broker, with the position itself as
collateral. The rules that matter:

1. **The collateral check happens once per day, against the closing price.** The account must
   maintain a collateral ratio of at least **140%** (position value ÷ loan). Intraday prices do
   not trigger anything for a standard credit account — only the close counts.
2. **A breach starts a countdown, not a sale.** Close below 140% on day D → margin-call notice →
   day D+1 to deposit cash or eligible securities → if uncured, forced sale on the **morning of
   D+2**. One important acceleration: at a representative broker (Eugene), falling below **120%**
   collapses the grace period to a single day. A violent enough session fast-tracks liquidation
   to the very next open.
3. **Execution is at the next opening auction, priced to guarantee a fill.** The broker's system
   submits the sell orders pre-market (before the 8:30–9:00 call auction). For collateral
   shortfalls the order quantity is computed **assuming the fill happens at the limit-down price
   (하한가)** — Eugene's published formula is literally *shortfall ÷ [limit-down × (1 − fees)]* —
   and the order is placed to execute unconditionally at the open.
4. **Depositing the full shortfall before the open cancels the sale.** Some brokers also let the
   client choose which security gets sold if requested early enough (Eugene: before 8:30).

### Three consequences of the design

- **Forced supply is front-loaded into the first 30–60 minutes of the session.** It is a fixed,
  pre-computed quantity submitted before the open. By roughly 10:00 it is simply *done* — the
  purest real-world case of "the move ends at a quantity."
- **The broker systematically oversells.** Because share count is sized assuming a limit-down
  fill, the actual (higher) fill price means more shares hit the tape than the shortfall strictly
  requires. Forced supply is conservative by construction, which amplifies the morning flush.
- **Heavy forced-sale mornings show limit-down indicative prices in the pre-open auction** before
  the rest of the book arrives — a visible tell that mechanical supply is queued (documented in
  the October 2021 retail-leverage episode).

### The conveyor belt, and how it breaks

Because shortfalls are measured at the close and sold at the next open, a multi-day decline gets
**quantized into daily installments**: down close → overnight breach list → next-morning forced
selling → weak morning → if the day *closes* down again, the belt reloads for the following
morning. Two corollaries:

- **An intraday crash that recovers by the close triggers nothing.** Circuit breakers and
  sidecars pause trading but neither execute nor cancel forced orders — and since only the close
  is measured, a scary intraday low that finishes recovered leaves the breach list small.
- **The first day that closes strongly up breaks the chain.** A big up-close cures collateral
  ratios en masse, so the next morning inherits almost no forced supply. This is why V-days tend
  to *end* these cascades rather than merely interrupt them.

### Exceptions to "next morning only"

- **Some brokers and products liquidate intraday.** Fintech brokers (e.g. Toss) and leveraged
  products (CFDs) run real-time forced liquidation on intraday breaches; traditional cash-equity
  credit accounts at legacy brokers generally do not.
- **Derivatives margin is a different regime entirely** — futures/options margin is marked and
  called intraday.
- **The rules soften in systemic crashes.** Regulators have leaned on brokers to extend grace
  periods or pause 반대매매 (done in the COVID crash) — the machinery can be suspended exactly
  when it would bite hardest, a caveat before extrapolating the pattern into the largest tails.
- Grace periods and ratio tiers are broker-terms specifics; the numbers above (140%/120%, D+2)
  are representative documentation (Eugene, Shinhan, KB), not statute.

## Part 2 — Why ~10:00 KST specifically: three clocks converge

There is no secret 10:00 switch inside institutional sell algorithms. Instead, three independent
and entirely mundane clocks tick at roughly the same minute, and on a panic morning they all
point the same way.

**Clock 1 — the forced supply runs out.** Per Part 1, the morning's 반대매매 quantity was fixed
last night and front-loaded into the open. Somewhere in the first hour the last forced order
fills, and supply switches off discontinuously — it does not fade.

**Clock 2 — execution algorithms rotate off the open.** Intraday volume follows the classic
U-shape (heavy open, quiet midday — Admati–Pfleiderer 1988, confirmed in Korean VWAP studies),
and participation algorithms are calibrated to it: they trade heavily into the opening surge and
throttle down as volume normalizes. Meanwhile the cautious money — domestic institutions and
pension-type buyers — conventionally waits out the opening chaos and starts deploying once "a
full market cycle is established after 10 o'clock," a heuristic old enough to be standard Korean
trading-education material. Sell intensity fades and scheduled buying ramps at roughly the same
minute, with nobody having set a timer.

**Clock 3 — Taiwan opens at exactly 10:00 KST.** The Taiwan Stock Exchange opens at 9:00 Taipei
time, and TSMC's opening print is the single most-watched cross-read for the Korean memory
complex — Samsung Electronics and SK hynix are roughly half of KOSPI market value the way TSMC is
~40% of the TAIEX, twin semiconductor monocultures that trade as one complex. A not-catastrophic
Taiwan open resolves the [identification problem](informed-vs-uninformed-flow.md) — "is this
informed selling, or just flow?" — and the sidelined buyers reclassify simultaneously. (China's
open at 10:30 KST is a second, smaller checkpoint on the same morning.)

The result: on a morning where the selling was constraint-driven, ~10:00 is where the forced
seller finishes, the algorithmic sell pressure decays, and the strongest cross-market information
of the morning arrives — all at once. That is a *schedule collision*, not a configuration.

## When the 10:00 turn does NOT come

The clocks only matter when the forced supply is **local and morning-scheduled**. When the
constraint is bigger than Seoul's first hour, the morning bounce fails:

- **August 5, 2024 ("Black Monday"):** the KOSPI fell all day into a circuit breaker with no
  10:00 rescue, because the constraint — the global yen-carry unwind — was neither Korean nor
  finished by mid-morning.
- **A multi-day de-grossing** (like late June 2026) reloads the conveyor belt every down close;
  each morning flushes, but the afternoon can fail again until the larger constraint clears —
  the "V lasts as long as the constraint lasts" rule from the
  [cascades page](liquidity-cascades-and-v-reversals.md).
- **Genuine information** does not care about the clock at all: a real repricing holds its lows
  regardless of when the margin calls finish.

## Worked example — July 3, 2026

After a brutal week of AI-complex selling (down closes on consecutive days = a fully loaded
conveyor belt), the KOSPI opened +1.2%, reversed hard to a low of **7,378** during the first
hour — the overnight breach list clearing at and after the open — then **began rebounding around
10:00 a.m.** The rebound compounded all day: through 8,000 at 1:39 p.m., a *buy-side* sidecar
(KOSPI-200 futures +5% sustained one minute) at 1:47 p.m., close **+5.37%** at 8,058. Samsung
Electronics finished **+9.27%**, SK hynix **+9.69%**.

The flow data identified the actors: foreigners net **sold** ₩1.48T and individuals net sold
₩1.26T, while **domestic institutions net bought ₩2.65T** — morning forced/foreign supply
exhausting into a scheduled institutional bid, the textbook Constraint payer handing the
[immediacy concession](price-formation-and-the-float-identity.md) to whoever stood at the low.
And per the conveyor-belt corollary, the +5.4% close cured collateral ratios en masse: the chain
was broken, not paused.

## What this means for trading

- **On a Korean panic morning, the low has a schedule.** If the breadth test says flow (whole
  complex down together, no news scaled to the move), the first hour is when the forced quantity
  clears and ~10:00 is where exhaustion, algo rotation, and the Taiwan cross-read stack. That is
  the highest-probability window for the turn — *conditional* on the constraint being local and
  morning-sized.
- **Watch the close, not the low.** Today's close writes tomorrow morning's forced-supply list.
  A recovered close disarms the next open; a weak close reloads it. The single most informative
  print for the next morning's mechanics is tonight's closing collateral arithmetic.
- **The pre-open auction is a free look at queued forced supply.** Limit-down indicative prices
  before 9:00 on no news = mechanical supply waiting.
- **The usual tail applies.** All of this is the flow case. A genuine demand crack does not turn
  at 10:00, and ex ante the discrimination is probabilistic — breadth first, size accordingly
  ([navigating nonlinear markets](../../synthesis/navigating-nonlinear-markets.md)).

## Verification note (2026-07-03, at writing)

Written the same day as the July 3 session it describes, from a live query. The 반대매매
mechanics (140% close-price test, D/D+1/D+2 calendar, sub-120% acceleration, pre-open submission,
limit-down-based quantity formula, pre-8:30 substitution window) are from broker documentation —
[KB](https://kbthink.com/stock/stock-forced-liquidation.html) ·
[Eugene](https://www.eugenefn.com/serv/svlo/svlo107p.do) ·
[Shinhan](https://open.shinhansec.com/mobilena/html/ma/nama000301.html) ·
[Korea Investment](https://blog.koreainvestment.com/%EB%AF%B8%EC%88%98%EA%B8%88-%EB%AF%B8%EC%88%98%EA%B1%B0%EB%9E%98-%EB%B0%98%EB%8C%80%EB%A7%A4%EB%A7%A4-%EC%A6%9D%EA%B1%B0%EA%B8%88%EB%A5%A0-%EB%9C%BB/) ·
[Toss](https://corp.tossinvest.com/en/business?tab=forcedLiquidation) — and are representative,
not universal (terms vary by broker). The July 3 timeline and flow data are from
[Korea JoongAng Daily](https://www.koreajoongangdaily.com/business/kospi-buyside-sidecar-activated-as-benchmark-stages-dramatic-rebound-above-8000/12754253)
and [Bloomberg](https://www.bloomberg.com/news/articles/2026-07-03/south-korean-stocks-jump-5-after-turbulent-week-on-ai-swings).
Two honesty flags carried on-page: (1) whether Taiwan's July 3 open specifically was strong was
**not verified** — Clock 3 is structural, its role *that particular day* is plausible rather than
confirmed; (2) "institutions bought ₩2.65T" is the exchange's investor-type aggregate — how much
was pension money vs. other domestic institutions was not broken out in the sources read.

## Relationships

- The general anatomy this page localizes:
  [liquidity cascades & V-reversals](liquidity-cascades-and-v-reversals.md) — this is the
  Korea-specific answer to that page's open question "can the constraint's clock be named?"
  (here: yes — it's literally on a calendar).
- Telling flow from information at the open: [informed vs. uninformed flow](informed-vs-uninformed-flow.md).
- The payer at the morning low: [who pays you](who-pays-you.md) (Constraint); the concession
  mechanics: [price formation & the float identity](price-formation-and-the-float-identity.md).
- The sector this matters most for: [semiconductors](../instruments/semiconductors.md) — the
  Korea/Taiwan twin-monoculture linkage is why Clock 3 exists.
- Risk framing for trading the window:
  [navigating nonlinear markets](../../synthesis/navigating-nonlinear-markets.md).
- The run-the-list operational version of this page (condition → fuel → calendar → 9:00–10:30
  trigger sequence → falsifiers):
  [catching the V-day checklist](../../systematic-trading/checklists/catching-the-v-day-checklist.md).

## Open questions

- Can the queued forced quantity be estimated *before* the open — from credit-balance statistics
  (금융투자협회 publishes daily 신용융자 outstanding), the prior close's breach arithmetic, and
  pre-open auction indicatives — well enough to size the morning-flush trade rather than merely
  anticipate it?
- Does the ~10:00 turn survive a formal event study (panic-morning sample, KOSPI minute bars,
  conditioned on prior-day close < −3%)? The folk wisdom is old; the wiki has not yet seen it
  measured.
- How often does Clock 3 dominate Clocks 1–2 — i.e., do Korean panic mornings where Taiwan opens
  *weak* still turn at 10:00, or does the Taiwan print gate the reclassification?
