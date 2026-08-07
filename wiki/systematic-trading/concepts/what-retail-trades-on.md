---
type: concept
title: What Retail Actually Trades On — The Signal Set and Why It Is Forecastable
description: The conditioning information behind manual retail trading (attention, chart levels, sentiment, dip-buying), the measured sign of the flow it generates at each horizon, and who monetizes it.
tags: [systematic-trading, behavioral, market-microstructure, flow]
timestamp: 2026-07-15T00:00:00Z
status: active
sources: []
---

# What Retail Actually Trades On — The Signal Set and Why It Is Forecastable

The casual version of the question is "retail trades on intuition, charts, and sentiment — what
are the actual signals?" The practitioner version is sharper: **what conditioning information
generates retail order flow, what sign does that flow carry at each horizon, and who gets paid
for knowing the answer?** The reframe matters because the economically important fact about
retail signals is not whether they work for the retail trader (mostly they don't, and that is
measured), but that **almost every one of them is a deterministic function of public, salient,
mostly price-derived information**. If you can see the same chart, the same headline, and the
same social feed, you can forecast the flow before it arrives. That forecastability — not the
signals themselves — is the traded product: it is what a wholesaler buys with payment for order
flow, what a [prediction-first market maker](prediction-first-market-making.md) feeds into its
fair-value model, and what the desk's own [Korea Flow Sleeve](../strategies/korea-flow-sleeve.md)
fades at the weekly horizon.

Everything below is tagged the way the S46 pages are: **[T]** for results with a formal model
behind them, **[M]** for measured empirical findings in the academic record, **[D]** for the
desk's own measured evidence.

---

## 1. The master signal is attention, and it only works in one direction [M]

Underneath charts, memes, and news sits one asymmetry, established by Barber and Odean (2008,
"All That Glitters"). A retail investor deciding what to **buy** faces a search problem over
thousands of stocks and can only evaluate what crosses their screen. A retail investor deciding
what to **sell** searches only their own handful of holdings — and, since most retail accounts
cannot short, an attention spike cannot generate retail selling in a stock they don't own. The
consequence: **anything that grabs attention produces net retail buying, regardless of the sign
of the news.** The three attention triggers Barber–Odean measured are news coverage, an extreme
one-day return (in either direction), and abnormal trading volume. Da, Engelberg and Gao (2011)
made the mechanism directly observable: spikes in Google search volume for a ticker predict
retail buying, a short-lived price bump, and then reversal over subsequent weeks.

This is the master key for reading every other retail "signal": a moving-average crossover, a
52-week high, a Reddit thread, and an earnings headline are not four different signals — they
are four channels through which a name gets into the retail field of view. The signal content
is mostly *salience*, and salience-driven buying is, on the academic record, a negative
predictor of returns at the weeks-to-months horizon (Hvidkjaer 2008; Barber–Lee–Liu–Odean 2009
on Taiwan's complete audit-trail tape, where individual investors transfer roughly 2% of GDP
per year to institutions).

## 2. The chart signals — what technical analysis actually is [M]

The concrete TA menu retail trades from is short, and every item on it is a function of past
price and volume:

- **Moving averages and crossovers** (the 50/200-day "golden cross" and its variants), and
  trend-following entries generally.
- **Support and resistance** — prior highs/lows and, above all, **round numbers**. This one has
  the best microstructure evidence: Osler (2000, 2003) showed FX limit orders cluster *at* round
  numbers and stop-loss orders cluster *just beyond* them, so a price touching the level
  triggers a mechanical order cascade. Support/resistance "works" not because the level means
  anything but because enough people placed orders there — self-fulfilling coordination that is
  measurable in the order book.
- **Breakouts to new highs**, especially the 52-week high. This is one of the few TA-adjacent
  signals with genuine cross-sectional content: George and Hwang (2004) showed proximity to the
  52-week high predicts returns, interpreted as anchoring — traders under-react near a salient
  price ceiling. (The desk's new-high checklist lives on the same fact.)
- **Oscillators** — RSI, MACD, Bollinger bands — used almost entirely as "oversold, buy the
  dip" triggers.
- **Chart patterns** (head-and-shoulders, flags, cup-and-handle). Lo, Mamaysky and Wang (2000)
  found kernel-smoothed versions of these patterns carry *some* conditional information —
  distributions of returns differ after patterns — but nothing resembling a tradable edge
  after costs.

The honest verdict on TA as alpha: Brock–Lakonishok–LeBaron (1992) found the classic
moving-average rules worked in the Dow — up to 1987. Sullivan, Timmermann and White (1999)
then ran the full universe of ~7,800 classic rules with a data-snooping correction and found
the apparent performance does not survive out of sample; in modern US equities the classic
rule set is dead. The two survivors are narrow: 52-week-high anchoring (a cross-sectional
factor, not a chart trade) and intraday round-number cascades in FX (a flow effect, not a
forecast).

But notice what death-as-alpha leaves alive: **a TA signal is a deterministic function of the
public tape, so conditional on the tape, retail flow is predictable.** When SOXL closes within
1% of a round hundred, or a KOSPI name prints a 52-week high on volume, you know — before it
happens — that a specific crowd will send market orders in a specific direction. TA is a weak
return forecast and a strong *flow* forecast. That is the version of TA that professionals
actually use.

## 3. The sentiment and social layer [M]

Three measured facts organize this layer:

1. **Retail herds.** Barber, Odean and Zhu (2009) showed retail trades are correlated across
   accounts — retail is not offsetting noise that nets to zero; it is a coordinated flow with
   a common driver (the attention channel above). This is precisely what makes retail flow a
   *factor* rather than a nuisance: it moves prices, and its imbalance is measurable.
2. **Retail prefers lotteries.** Kumar (2009) documented the profile — low nominal price, high
   idiosyncratic volatility, high skewness — and the modern expressions are short-dated
   out-of-the-money options (zero-days-to-expiry options are now roughly half of S&P option
   volume, with retail a heavy share), leveraged ETFs (the desk's own SOXL and KODEX 레버리지
   tape), and micro-cap themes. Lottery demand is a *price* — these instruments trade
   persistently rich, and the sellers (option market makers, LETF counterparties) collect.
3. **The social feed is an attention accelerant with a derivatives amplifier.** The meme
   episodes (GME 2021 the archetype) are attention cascades where call buying forces dealer
   hedging that amplifies the move — the crowd's signal was the crowd itself. Downstream of
   this sits a copy-trading layer: "unusual options activity" feeds and flow-following services
   that retail uses to chase what it believes is institutional flow — flow-following the
   flow-followers.

## 4. The part the framing misses: most retail flow is contrarian, and the sign depends on the path [M] [D]

"Momentum riding" describes the visible meme tail, not the statistical bulk. On aggregate
tapes, **retail is a short-horizon contrarian**: Kaniel, Saar and Titman (2008) showed
individuals net-buy after price declines, and their weekly imbalance *positively* predicts
returns — because dip-buying limit orders supply liquidity to institutions demanding it, and
liquidity provision earns a compensation. The disposition effect (Odean 1998 — selling winners
too early, riding losers) puts retail on the providing side in rallies too. So retail flow has
two regimes with opposite signs:

- **Into-weakness buying** = paid liquidity provision → *positive* short-horizon forward
  returns (the Kaniel–Saar–Titman channel).
- **Into-strength buying at attention extremes** = salience chasing → *negative*
  weeks-to-months forward returns (the Barber–Odean/Hvidkjaer channel).

The resolution is conditioning on the price path that generated the flow — and this is not
just literature: the desk's [Korea Flow Sleeve](../strategies/korea-flow-sleeve.md) built its
R component exactly on this split and **measured it on KRX investor-type data: retail net-buy
z ≥ +2 into strength carries IC −0.0126 forward, strongest in the most-liquid tercile
(−0.0231, t = −2.93)** — the attention-extreme fade validated as a negative signal, while
naive "retail bought, short it" fails because it shorts the paid-provision regime. [D]

The same conditioning shows up in the US identification literature: Boehmer, Jones, Zhang and
Zhang (2021) — who identify retail prints from sub-penny price improvement — find retail
imbalance positively predicts returns out to weeks, consistent with the provision-plus-
persistence side (with the caveat that Barardehi et al. have contested the identification's
accuracy; the measurement layer is itself an open fight).

## 5. The Korean retail signal set has one extra item: the cohort prints themselves [D]

KRX publishes daily (and intraday) net-buy tables by investor type, so Korean retail's signal
menu includes **"what did foreigners buy yesterday"** — the same disclosed flow data the
desk's sleeve runs on. Add the 테마주 rotation culture (theme-of-the-week baskets), the
신용융자 margin-loan cycle whose forced-liquidation belt the engine already tracks (S10), and
the KODEX leveraged-ETF pair as the lottery instrument of choice, and you get a market where
retail flow is even more legible than in the US — the flows are printed, the margin fuel is
printed, and the levels retail watches are the same disclosed prints the desk reads. The
reflexivity is a feature, not a bug: a signal retail also reads tells you where retail's
orders will be.

## 6. Why this is the market-making story from the other side [T] [M]

Put the pieces together and the S46 thread closes a loop:

- Every input to retail's decision is **public and salient** — the tape, the level, the
  headline, the feed. Therefore retail flow is forecastable from data everyone has.
- **Payment for order flow is the market pricing that forecastability at the millisecond
  horizon**: a wholesaler pays for retail orders precisely because they carry no information
  about the next few seconds of price (no adverse selection at fill horizon) — the
  revealed-preference proof that retail signals are uninformed at short horizon (see
  [who pays you](../../shared/concepts/who-pays-you.md) and
  [the industrialization of edge](../../synthesis/industrialization-of-edge.md)).
- At the **minutes-to-hours** horizon, the same flow's autocorrelation (herding + order
  splitting) is exactly the "flow predicts flow" family inside a
  [prediction-first market maker's](prediction-first-market-making.md) fair-value engine.
- At the **weeks** horizon, the attention-extreme component reverses, and fading it is a
  documented cross-sectional signal — the desk's R component is a live instance.

One flow, three horizons, three different players getting paid — the
[horizon ladder](speed-vs-prediction.md) applied to a single counterparty class. The retail
trader's losses are not mostly the spread (that leak is small); they are self-inflicted via
turnover, timing, and lottery-instrument selection (Taiwan: ≈2.2% of GDP per year — the
number that made the [industrialization page](../../synthesis/industrialization-of-edge.md)
walk back "wholesalers harvest retail" to "retail mostly self-plays").

## 7. Honest limits

- **Retail is not monolithic.** Kelley and Tetlock (2013) found retail *limit* orders predict
  returns positively — the passive, patient sliver of retail is informed-or-paid, and a
  minority of retail accounts (earnings anticipators, industry insiders' networks) is
  genuinely informed. Every statement above is about the aggregate flow, not every account.
- **Era drift.** The canonical attention studies are 1991–2010 US data; zero commissions,
  0DTE, and social feeds have plausibly increased both the herding correlation and the speed
  of the attention cycle. Magnitudes should be re-estimated, and the desk's KRX measurement
  (2026 data) matters more than the US papers' point estimates.
- **The measurement layer is contested.** BJZZ sub-penny identification vs the Barardehi
  critique means US "retail flow" series carry identification error the KRX investor-type
  prints do not — one more reason the Korea anchor is the desk's better lab.
- **TA-works-in-FX is narrow**: intraday, round-number cascades, order-cluster driven — it
  does not rehabilitate chart trading as a return forecast.

## The stack in one picture

A compressed model of the whole page (proposed by the user in the S47 discussion, corrected
here in four places: the two-family split in Layer 1 carried down through the sign of Layer 3;
the marketable/limit split in Layer 2; the flow being *bought*, not just modeled; the
feedback arrow that makes the flow autocorrelated):

```
Layer 0 — Public, salient information (the tape, headlines, feeds)
              ↓ selects what gets seen (attention — the one-directional master signal)
Layer 1 — Two heuristic families: chase ("it's running") | dip-buy ("it's cheap")
              ↓ coordinates (the heuristic need not be true — only shared)
Layer 2 — Correlated retail flow — split: marketable (chase) | limit (provision)
              ↓ modeled by some institutions (prediction-first MMs),
                BOUGHT by others (PFOF — the flow is an asset with a price)
Layer 3 — Prices & rent:
              • short-term: impact in the flow's direction
              • mid-term: the chase component reverts (fade-worthy at weeks — R);
                the provision component gets paid (KST channel)
              • transfers: a SMALL toll to intermediaries (retail's per-trade terms
                are near best-ever), a LARGE self-inflicted loss via turnover,
                timing, and lottery instruments (Taiwan ≈ 2.2% of GDP/yr)
              ↺ price moves feed back into Layer 0 as attention — the loop that
                makes flow autocorrelated ("flow predicts flow") and, at the
                extreme, the meme cascade with the dealer-gamma amplifier
```

The one-sentence use of the model: the sign of Layer 3 is decided in Layer 1, so read the
price path that generated the flow, not the flow alone.

## Relationships

- Supplies the counterparty-side view of [prediction-first market making](prediction-first-market-making.md)
  (the flow being forecast) and of [who pays you](../../shared/concepts/who-pays-you.md) /
  [the industrialization of edge](../../synthesis/industrialization-of-edge.md) (the flow being purchased).
- The two-regime sign result is operationalized and measured in the
  [Korea Flow Sleeve](../strategies/korea-flow-sleeve.md)'s R component.
- The horizon decomposition instantiates [speed vs prediction](speed-vs-prediction.md)'s ladder
  for one participant class.
- 52-week-high anchoring connects to the desk's new-high checklist
  ([holding & exiting at new highs](../checklists/new-high-trade-checklist.md)).

## Open questions

- Has the zero-commission/0DTE era changed the *sign horizon* of attention flow (faster
  reversal?) — testable on the KRX retail panel the engine already archives.
- Where exactly does into-weakness provision flip to falling-knife averaging-down in the KRX
  data (the M component's territory — margin-flush conditioning)?
- Can round-number/stop-cluster cascades be measured on KRX single names the way Osler
  measured EURUSD (limit-order-book snapshots needed)?
