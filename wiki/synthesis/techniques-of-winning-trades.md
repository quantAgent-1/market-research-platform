---
type: overview
title: How Winning Trades Are Actually Made — the Edge Taxonomy, Down to the Mechanics
description: Every durable way of winning, organized by mechanism — liquidity provision, flow anticipation, information speed, risk premia, relative value, behavioral counterparties — with the implementation-level models, formulas, and failure modes, plus the machinery (costs, backtest forensics, sizing) that decides who keeps the money.
tags: [systematic-trading, derivatives, ml-stats, edge, execution, risk]
timestamp: 2026-07-06T00:00:00Z
status: active
sources: []
---

# How Winning Trades Are Actually Made — the Edge Taxonomy, Down to the Mechanics

**What this page is.** A from-training synthesis (agent knowledge, cutoff Jan-2026), written in
answer to: *"what are the techniques of winning trades, all the way down to technical details?"*
The companion pages answer adjacent questions — [what elite traders actually
know](what-elite-traders-actually-know.md) covers *who knows what and how much*, and
[trading-system fundamentals](trading-system-fundamentals.md) gives the *frame* (Edge × Risk ×
Implementation). This page fills the frame in: technique by technique, mechanism by mechanism,
with the actual models and numbers practitioners use.

The organizing claim: every durable technique is a **transfer from an identifiable counterparty
who pays for a persistent reason**. There are six such reasons, and they give six families of
technique. Everything else — charts, indicators, narratives — either reduces to one of these or
is noise. The last sections cover the machinery (costs, backtest hygiene, sizing) that decides
whether a real edge survives contact with reality, and the one-question test that separates an
edge from a story.

---

## 0. The arithmetic everything reduces to

Four relationships govern every strategy, and most trading failure is a failure to respect one
of them.

**Expectancy, not win rate.** E = p·W − (1−p)·L per trade. Win rate is a *design variable*, not
a virtue: trend followers win 35–45% of trades with winners 2.5–4× losers; market makers win
51–55% of thousands of micro-bets a day; option sellers win 85–95% and occasionally lose ten
winners' worth in a night. All three shapes can be profitable and all three can be ruinous — the
shape you choose determines your psychology requirements and your tail risk, not your worth.

**The fundamental law of active management** (Grinold): IR ≈ IC × √BR. Your information ratio is
your skill per bet (IC = correlation between forecast and outcome) times the square root of the
number of *independent* bets per year. Professional-grade IC in cross-sectional equities is
0.02–0.05 — nearly indistinguishable from noise on any single trade. Medallion's reported hit
rate is ~50.75% ([documented](what-elite-traders-actually-know.md) via Mercer/Zuckerman). The
lesson cuts both ways: tiny edges become monsters through breadth (this is *why* HFT and stat-arb
work), and a low-breadth trader (a few macro bets a year) needs an enormous per-bet IC that
almost nobody has. Choose your breadth to match your honest IC.

**Kelly and its hazards.** Optimal growth fraction f* = edge/odds; for continuous returns
f* ≈ μ/σ². Nobody serious runs full Kelly: the growth penalty for overbetting is quadratic
(betting 2× Kelly gives *zero* long-run growth, beyond that negative), parameter estimates are
noisy, and distributions are fat-tailed and non-stationary. Practitioners run ¼–½ Kelly.
The deeper point: position sizing has an *optimum* — both under- and over-betting cost you, and
over-betting costs you your existence.

**Costs are linear, edge is fragile.** Net = gross − turnover × all-in cost per trade. A signal
worth 20bp per trade with daily turnover needs all-in costs well under 10bp to survive; most
retail backtests assume mid-price fills and die on this one line. Costs are the most knowable
quantity in trading, and the most ignored. ([Cost-aware trading](cost-aware-trading.md) covers
this in depth; the [small-account edge map](retail-capital-edge-map.md) shows it killing live
candidate edges at retail scale.)

---

## 1. Liquidity provision — get paid for immediacy

**Who pays and why:** impatient traders pay a premium to transact *now*; the resting counterparty
collects it. The permanent risk is adverse selection — sometimes the impatient trader is impatient
because they know something.

**Market making at the tick horizon.** The canonical model is Avellaneda–Stoikov (2008): quote
around a *reservation price* r = s − q·γσ²(T−t) — the mid, skewed against your inventory q so
that holding risk pushes your quotes to shed it — with optimal half-spread
δ ≈ γσ²(T−t)/2 + (1/γ)·ln(1 + γ/κ), where κ measures how fast fill probability decays as you
quote further from mid. In production the mid is replaced by the **microprice**,
P = (V_bid·P_ask + V_ask·P_bid)/(V_bid + V_ask) — the imbalance-weighted price that better
predicts where the next trade prints. Two further production realities: **queue position** (in
large-tick stocks, being early in the queue at a price level is worth a substantial fraction of
the spread — you enter queues early and defend position) and **adverse-selection filtering**
(classify flow toxicity; widen or pull when informed-looking flow arrives, e.g. sweeps across
venues, fills that immediately run against you, news-time flow).

**The microstructure signals that gate everything at this horizon.** Order-flow imbalance moves
price *linearly* with imbalance relative to depth (Cont–Kukanov–Stoikov 2014) — the cleanest
short-horizon relationship in microstructure. Top-of-book **queue imbalance** predicts the
direction of the next mid-price move well above chance in large-tick names (hit rates on the
order of 60–75% — *verify magnitude*). And **signed order flow is long-memory**: trade-sign
autocorrelation decays as a slow power law (Hurst ≈ 0.7) because institutions split parent
orders into child orders over hours and days. That persistence — metaorders leaking into the
tape — is arguably the single most robust statistical fact about markets, and it's what both
market makers (defensively) and flow-anticipators (§2, offensively) live on.

**Short-term reversal is the same trade run slowly.** Stocks that fell over the last day/week
bounce; the classic weekly reversal portfolio has high gross Sharpe. The mechanism is not
mispricing but *inventory*: someone's metaorder pushed price off equilibrium, and the bounce is
the payment to whoever absorbed it. Confirmation: reversal profits spike exactly when liquidity
is scarce (Nagel 2012 — reversal P&L tracks VIX). Net of costs it survives only for those already
at the table with near-zero marginal cost, netting reversal against their other flow. This is a
recurring pattern: **gross alpha that is really a wage for a service** (here, liquidity
provision) accrues to whoever provides the service cheapest.

**The variance risk premium is liquidity provision in the volatility dimension.** Implied vol
exceeds subsequently-realized vol on average (SPX: ~2–4 vol points; positive in the large
majority of months — *verify current magnitude*), because crash-insurance demand is inelastic
and the sellers who warehouse it demand a premium. Implementations, in increasing care:
put-writing (the CBOE PUT index), delta-hedged short straddles/strangles, short variance swaps,
defined-risk short structures (condors/flies) at retail. The failure mode is structural, not
incidental: short-vol P&L is itself short a liquidity option, and the blow-ups are reflexive —
Feb-2018 XIV lost 96% in an afternoon because the product's own rebalancing demand chased the
closing VIX-futures auction it was moving. If you sell vol, the technical discipline is: defined
tail (own the wing), sized to the *stress* vega not the calm vega, never short the front of a
panic.

---

## 2. Flow anticipation — trade ahead of price-insensitive demand

**Who pays and why:** some flows must trade *regardless of price* — index rules, daily-rebalance
mandates, dealer hedging mechanics, margin calls. Price-insensitive demand pays whoever positions
in front of it and supplies liquidity at the worse price. This family is the institutional core
of "knowing what happens next" — [the elite page](what-elite-traders-actually-know.md) documents
that flow visibility, not forecasting, is most of what elite desks actually have; this section
is the mechanics of using it.

**The physics: the square-root impact law.** A metaorder of size Q in a market trading ADV per
day moves price by approximately ΔP ≈ Y·σ_daily·√(Q/ADV), with Y ≈ 0.5–1 — remarkably universal
across equities, futures, FX, options, even crypto (Bouchaud/CFM's measurements, Almgren's
empirics, Ancerno institutional data). Three consequences worth memorizing: total execution cost
scales as Q^1.5 (superlinear — twice the size, ~2.8× the cost); strategy **capacity** falls as
the square of impact (capacity ∝ (alpha/impact)²); and roughly ⅔ of peak impact is *transient*,
decaying after the flow ends, with the remainder permanent. So: if you can estimate a coming
flow's size, its price effect and its decay are *computable*. That computation is the entire
trade in this family.

**Known calendars.** Index reconstitutions: the S&P inclusion effect has decayed from ~+7% in
the 1990s to under 1% now (verified on [the elite page](what-elite-traders-actually-know.md)) —
the *announced* flow is arbed to nothing, and the residual game is (a) predicting adds/deletes
*before* announcement from the published methodology rules, and (b) less-institutionalized
venues: Russell reconstitution's June sequence, MSCI country reviews, KOSPI200 changes, thematic
ETF rebalances. **Leveraged-ETF end-of-day rebalance flow** is exactly computable:
flow ≈ (L² − L)·AUM·r_day for leverage L — a −2× fund must *sell* into a down move — concentrated
into the close, known by 3pm. Crowded in the big US products; the technique survives in the less
watched ones. The generic method: read the rulebook, compute the flow, apply the square-root law,
position before, exit into.

**Dealer-gamma mechanics.** Options dealers hedge net delta continuously. When dealers are net
**short gamma** (customers own the options), hedging *amplifies* moves — they sell as price
falls, buy as it rises; net **long gamma** dampens and pins. Sign and size are estimable from
open interest plus assumptions on customer direction (GEX-style), sharpened materially with
trade-direction data (OPRA). Charm and vanna flows concentrate into monthly OPEX; 0DTE recycles
the whole cycle intraday now. This mechanism is the correct explanation for most "gamma
squeezes" (GME Jan-2021: call buying forced dealer short-gamma, whose hedge-buying fed the rise)
and for pinning at round strikes. The [present-state stack](present-state-stack.md)'s
dealer-gamma map is this desk's implementation.

**Liquidation cascades — the most price-insensitive flow of all.** Forced deleveraging has
signatures you can monitor: cash-futures **basis blowouts** (Treasury basis unwind, Mar-2020),
vol-target and risk-parity mechanical de-grossing (estimable: vol-control AUM × the exposure
change a vol spike mandates — the Feb-2018 and Aug-2024 sequences both ran on this), crypto perp
liquidation ladders (published liquidation levels). Two ways to be on the right side: front-run
the cascade once triggered (momentum into it), or provide the terminal liquidity at exhaustion —
the V-bottom bid — which requires an exhaustion signal (volume climax + failure to make new lows
+ basis/funding re-normalizing), not courage. The [cascade sentinel](present-state-stack.md) tool
and the [nonlinear-markets](navigating-nonlinear-markets.md) page's never-the-forced-seller rule
are the two halves of this desk's answer.

**"Technical levels" as flow objects.** Stops and limit orders cluster at round numbers and
prior swing highs/lows — documented directly in FX order-book data (Osler). A level break
triggers a short, self-limiting stop cascade; a defended level is a wall of resting liquidity.
This is the honest microfoundation for the parts of support/resistance that work: **levels are
maps of resting orders, not geometry.** The tradable implications are specific: breakouts work
when they detonate real stop clusters *and* fresh flow follows (volume confirms); they fail
("false breaks") when the cluster is thin — and the failure itself is a trade, because the
trapped breakout traders' stops become the fuel for the reversal.

---

## 3. Information speed — be first to what's knowable

**Who pays and why:** prices incorporate public information over minutes to months, not
instantly. Whoever processes first trades against whoever processes later. The family splits by
*what kind of "first"* you can be.

**Latency arbitrage** (to mark the boundary, not to recommend): stale-quote sniping across
venues, SIP-vs-direct-feed gaps, the ES→SPY lead-lag at millisecond scale. Modern races resolve
in tens of microseconds; the aggregate "latency tax" on liquidity has been measured around a
half basis point of volume (Budish et al. and the FCA study — *verify magnitude*). Closed to
anyone without colocation and hardware; its retail relevance is purely defensive — never rest
marketable orders through scheduled releases, because you are the stale quote.

**Complexity arbitrage — the speed game retail can actually play.** Unscheduled and
hard-to-parse information diffuses slowly: 8-K footnotes, court rulings, clinical-trial design
subtleties, regulatory filings, foreign-language disclosures (KRX filings in Korean are a live
example for this desk). The bottleneck is reading comprehension, not fiber. The robust
empirical facts about news generally: *novelty* matters (the first story moves price, echoes
don't), small caps drift for days while large caps absorb in minutes, and LLMs have now
commoditized the easy sentiment layer — the surviving edge is in judgment-heavy interpretation,
which is precisely what doesn't commoditize.

**Post-earnings-announcement drift and the revision cascade.** PEAD — sorting on standardized
unexpected earnings (SUE) and riding the 60-day drift — is the grandfather anomaly, much decayed
in large caps but residual in small/neglected names. The live modern version is **analyst
revision momentum**: revisions autocorrelate (one raise begets more, because analysts anchor and
under-adjust), and estimate-revision signals remain among the more robust cross-sectional
predictors. The desk-level implementation of this whole idea is an [expectations
tracker](present-state-stack.md): the tradable object is never the number, it's the gap between
the number and the expectation embedded in price — see the MU episodes in
[the monitoring system](semiconductor-monitoring-system.md).

---

## 4. Risk-premia harvesting — get paid for holding what others must shed

**Who pays and why:** persistent premia exist where a constrained or fearful class must pay
someone to hold what they can't: insurance premia (vol, crash risk), funding premia (carry),
leverage-constraint premia (low-beta), hedging pressure (commodity curves). These are the
slow-capital techniques — capacity is huge, Sharpe is moderate, and the payment for the premium
is occasional participation in exactly the event being insured.

**Trend / time-series momentum — the full implementation, because the details carry half the
value.** Per market: signal = sign (or scaled z) of price versus a blend of EWMA crossover pairs
— the classic set is something like 8/32, 16/64, 32/128 days — or simply the sign of the trailing
12-month return (Moskowitz–Ooi–Pedersen 2012). Position = signal × (target vol)/(σ̂ ×
√N_effective), with σ̂ an EWMA of realized vol (~20–60 day). Run it across 50+ liquid futures —
equities, bonds, FX, commodities — each vol-weighted, book targeted to ~10% vol. The documented
record (MOP; AQR's "A Century of Evidence"): gross Sharpe ~0.7–1.0 over a century, more like
0.4–0.6 net in the crowded modern era (*verify current*), with the *positive skew and crisis
convexity* being the actual point — trend was up big in 2008 and 2022 precisely because it
mechanically flips short as everything de-grosses. Two implementation details matter more than
the entry rule: **(1) vol-scaling is itself alpha** — position ∝ 1/σ̂ automatically cuts size as
vol rises into losses, an anti-martingale that manufactures the skew; **(2) the speed blend is
the real design decision** — fast trend alone dies of chop and costs, slow alone gives back too
much at turns.

**Carry, in every asset class** (Koijen–Moskowitz–Pedersen–Vrugt showed it's one phenomenon):
FX carry (fund low-yielders, hold high-yielders; UIP fails; historical Sharpe ~0.6–0.9 pre-2008,
roughly half that since — *verify*; deeply negatively skewed, crashes when funding currencies
rally in risk-off — the Aug-2024 yen unwind is this desk's [replay episode #1](replay-gym.md));
commodity carry (curve shape — long backwardation, short contango; the microfoundation is
hedging pressure); rates carry (rolldown on steep curves); and vol carry (the VRP of §1 —
carry's purest form). The design fact: **carry and trend are the canonical complementary pair**
— carry is short-vol-shaped (steady collect, crash tail), trend is long-vol-shaped (steady
bleed, crisis payoff) — which is why the classic managed-futures book is a blend.

**The cross-sectional equity factors that survive honest replication** (Jensen–Kelly–Pedersen's
replication study; Hou–Xue–Zhang's): momentum 12-1 (skip the most recent month — it reverses;
crash-prone when the market snaps back after a crash: the 2009 WML crash — Daniel–Moskowitz;
vol-scaling roughly doubles its Sharpe), profitability/quality (gross-profits-to-assets,
Novy-Marx — robust), value (weak standalone in large-cap US post-2007, alive internationally
and as a conditioner), low-beta / betting-against-beta (real, with a leverage-constraints
microfoundation — Frazzini–Pedersen — but watch the embedded sector tilts), and
investment/asset-growth. What did *not* survive: size alone (net of costs, mostly gone) and the
long tail of the factor zoo (Harvey–Liu–Zhu: demand t > 3 given the number of trials;
McLean–Pontiff: anomalies lose ~26% of in-sample returns out-of-sample and a further ~32% after
publication). Implementation notes that decide the net result: monthly rebalance with turnover
bands (not daily), sector- and beta-neutralize the cross-sectional signals, and at retail scale
harvest slow factors through cheap ETFs or not at all — the DIY version's costs eat the premium
(the [small-account edge map](retail-capital-edge-map.md) measured exactly this).

---

## 5. Relative value — price the same cashflow two ways and trade the gap

**Who pays and why:** segmentation, constraints, and inventory pressure make near-identical
payoffs trade at different prices. You short the rich leg, long the cheap leg, wait. The defining
risk: the gap widens before it closes — every convergence trade is **short a liquidity option**,
and the family's disasters (LTCM) all trace to that one clause plus leverage.

**Pairs / stat-arb, the actual pipeline.** (1) Candidate selection by *cointegration* — Engle–
Granger two-step on log prices, Johansen for baskets — or by factor-model residual correlation;
never by raw price correlation (correlated prices with no error-correction just wander apart).
(2) Fit the spread to an Ornstein–Uhlenbeck process, dX = κ(θ−X)dt + σdW; the half-life of
mean-reversion is ln2/κ. Tradable half-lives are roughly 5–60 days — faster is costs, slower is
capital-inefficient and structurally fragile. (3) Enter at |z| ≥ 1.5–2, exit near z = 0, and
stop on *structural break*, not just price: half-life blowing out, cointegration test collapsing,
a corporate event changing the relationship. (4) Size by spread vol, not leg vol. The public
record is the pattern for the whole family: the distance method earned ~11%/yr over 1962–2002
(Gatev–Goetzmann–Rouwenhorst), then decayed toward zero as it industrialized. The technique
survives where it moved: intraday horizons, less-crowded markets, and residual space —

**modern equity stat-arb = residual reversion + flow.** Strip a risk model out of returns
(α = r − Xβ against market, sector, and Barra-style factors: size, value, momentum, vol,
liquidity), then trade the *residual* with reversion plus short-horizon flow/news signals,
holding hours to days, with the book neutralized to near-zero factor exposure. **Neutralization
is the technique**: un-neutralized "alpha" is usually disguised factor beta — crowded, crash-y,
and already owned by everyone. This is also why naive retail stat-arb fails: without the risk
model, you're trading factors while believing you're trading idiosyncratic spreads.

**Vol-surface relative value.** The no-arbitrage constraints define the tradable geometry:
butterflies ≥ 0 (call prices convex in strike), calendars ≥ 0 in *total variance* (σ²T
non-decreasing in T). Fit a parametric surface — SVI per expiry: total variance
w(k) = a + b[ρ(k−m) + √((k−m)² + σ²)] in log-moneyness k, or SSVI across expiries — and trade
residual rich/cheap points delta-hedged, exiting when the surface refits. Adjacent structures:
**skew RV** (risk-reversals against realized skewness when the skew is at historical extremes)
and **dispersion** — short index vol vs long single-name vol, which is a short position in
*implied correlation*; implied correlation is chronically rich because index puts are the
world's default hedge. Trade it vega-weighted, and respect the earnings calendar, which is where
single-name vol realizes.

**Basis trades.** Cash-vs-futures (the Treasury basis trade: long cash bond, short future,
repo-financed at 50–100× leverage, collecting single-digit basis points — profitable machinery
until repo breaks: Sep-2019, Mar-2020), ETF-vs-NAV (AP arbitrage; retail sees it only as stress
prints), ADR-vs-local, dual-listings. The generic content: **basis = funding + friction**, so
every basis trade is implicitly short funding stress, and it inverts exactly when funding
spikes. Size for the inversion, not for the carry.

**Merger arbitrage.** Long target at the spread to deal price (cash deals; for stock deals,
short the acquirer at the exchange ratio). The win rate is ~90%+ because most deals close; the
entire skill is handicapping the breaks: regulatory map (HSR second requests, CFIUS, EU Phase 2
timelines), financing outs, MAC clauses, and the downside measured as distance-to-unaffected
price. Run as a portfolio of 20–40 deals whose binary risks are mostly independent — *except* in
systemic stress, when spreads triple together as arb capital de-grosses (2008): part of the
premium is a deleveraging-risk premium, which is §2's cascade mechanics showing up inside an
"uncorrelated" strategy.

---

## 6. Behavioral counterparties — harvest the predictable errors

**Who pays and why:** aggregate retail and constrained-institutional behavior is predictable in
specific, documented ways, and the predictability is slow to arbitrage away because the flows
renew (new cohorts, same biases).

The load-bearing documented effects: the **disposition effect** (holders sell winners too early
and ride losers — one mechanical driver of both momentum *and* post-earnings drift:
under-reaction comes from anchored holders supplying stock into good news); **lottery
preference** (overpayment for positive skew: high-MAX stocks earn *negative* subsequent returns
— Bali et al.; far-OTM single-name calls are systematically overpriced, most extremely around
attention events); **attention chasing** (retail buys what's on the front page; attention spikes
predict short-term reversal — Da–Engelberg–Gao's search-based measures); and **anchoring on the
52-week high** (George–Hwang: proximity-to-high is itself a momentum signal, because anchored
holders sell too early as price approaches the high, damming up the move — then supply exhausts
and price runs).

The professionalized expressions: sell the lottery premium in defined-risk structures around
attention spikes (where borrow and options pricing permit); fade attention-driven gaps with
strict risk; supply liquidity into disposition-driven drift rather than chasing it. The honesty
clause: this family is **small-capacity and vicious in the tails** — being short a meme squeeze
means being short a §2 stop-cascade; borrow gets pulled and costs 50%+ annualized exactly when
the trade is best. Defined-risk structures only, sized as if the squeeze happens.

---

## 7. The machinery that decides who keeps the money

Everything above is the *gross* side. The families are real; most people still lose. The
difference is machinery, and it has four rooms. (The frame is
[trading-system fundamentals](trading-system-fundamentals.md); this is the equipment list.)

**The cost stack, itemized.** Per round trip: half-spread if you cross (or adverse selection if
you rest — you never escape both); impact per the square-root law (starts mattering around 0.1%
of ADV); fees/rebates; **borrow** on shorts (hard-to-borrow names routinely 5–50%/yr — this
single line deletes many published anomalies, which concentrate in exactly the unshortable
names); financing/margin; and implementation shortfall measured against decision price (Perold's
decomposition: delay cost + trading cost + opportunity cost of the unfilled remainder). Working
rule: a strategy is real if gross alpha per trade exceeds ~2× your *modeled* all-in cost,
because your cost model is optimistic in precisely the states where you trade most.

**Backtest forensics — the checklist that catches ~90% of fake edges.** Point-in-time
everything: as-reported fundamentals (no restatements), index membership as of the date,
delisted stocks included (survivorship bias alone adds ~1–4%/yr of phantom equity alpha). No
look-ahead: signals computed on bar t trade on t+1's prices, never same-bar closes. Costs and
borrow modeled per above. For anything ML: **purged K-fold with embargo** (López de Prado) —
overlapping labels leak between train and test folds, and that leakage is the #1 bug in
ML-finance. And multiple-testing honesty: the expected *maximum* Sharpe of N independent
worthless trials grows like √(2·ln N), so after 1,000 configurations a backtest Sharpe of ~2 is
the *null hypothesis*, not a discovery — deflate accordingly (Bailey–López de Prado's deflated
Sharpe ratio), or better, **pre-register** the hypothesis and spec before running the test.
(This wiki's own engine practice — pre-registration + DSR — exists because of this paragraph;
see the [engine-v3 docs](engine-v3/index.md).)

**Sizing and survival mechanics.** Fractional Kelly (¼–½) as the ceiling, not the target.
Vol-targeting at sleeve and book level — Moreira–Muir showed vol-managed versions of most premia
raise Sharpe, because volatility clusters (predictable) while returns don't scale with it, so
constant-vol exposure buys more return per unit of risk. A **pre-committed drawdown protocol**
(the multi-manager standard is brutal and correct: around −5% halve the book, around −7.5%
flat) — the point is truncating both the left tail *and* the tilt-denial spiral that generates
it. Assume **correlation goes to one**: in stress, everything long-risk is a single trade;
stress-test at ρ = 0.8–1.0 with 2008/2020 vol, not at sample correlations. And the forced-seller
test from [nonlinear markets](navigating-nonlinear-markets.md): structure the book so that no
one else's margin call can become your liquidation.

**Stops are strategy-specific — using the wrong kind converts edge into anti-edge.** For
trend/breakout systems the stop *is* the payoff shape: an ATR-trailing stop (2–3× ATR)
manufactures the positive skew — cut losers at 1R, let winners run to 3R+. For mean-reversion,
**price stops are anti-edge** — they systematically sell at the very extremes the strategy
exists to buy; risk is controlled instead by position size, time stops, and structural-break
triggers (§5's cointegration collapse, half-life blowout). For event/RV trades the stop is
thesis invalidation (deal breaks, basis regime change), enforced through hard capital-at-risk
caps set at entry.

**Decay, crowding, and the pipeline.** Alphas are perishable — the McLean–Pontiff numbers above
are the base rate, and crowding is partially measurable (pairwise strategy correlations rising,
factor-flow betas, 13F clustering, spread compression in the trade's own market). The
meta-technique — the one that distinguishes firms that last from trades that worked — is a
continuously running research pipeline: hypothesis intake → point-in-time test → cost gate →
paper trading → small live → scale or kill, with replacement rate ≥ decay rate. A durable desk
is a factory for edges, not a museum for one.

---

## 8. What "technical analysis" actually is, stripped to the load-bearing parts

Tested honestly, most named chart patterns carry no exploitable net edge: Lo–Mamaysky–Wang
(2000) — the most sympathetic rigorous study — found some patterns are statistically
"informative" but did not demonstrate net profits, and later replications are mostly negative.
What *does* survive, survives because it's an interface to a real mechanism from the sections
above:

trend and momentum (§4 — the one premium classical TA had right all along); the 52-week-high
effect (§6, anchoring); volume-confirmed breakouts (§2 — the volume spike marks genuine
metaorder flow detonating a stop cluster, versus a thin false break); support/resistance at
round numbers and prior extremes (§2 — maps of resting liquidity, documented in FX order books);
VWAP as an intraday attractor (institutional execution benchmarks VWAP, so their algos create
mean-reversion around it); and opening-range/overnight structure (the overnight session carries
the bulk of equity total return; the first hour reveals institutional participation for the
day).

So the honest restatement: **TA works where it reads flow and positioning, and fails where it
worships geometry.** A discretionary trader with a genuine edge is almost always doing manual
flow-reading — catalyst selection (§3), tape and level reading (§2), behavioral counterparties
(§6) — wrapped in enforced asymmetry: risk 1R to make 2.5R+, win 40–50%, exit the instant the
level that defined the trade fails. The §0 arithmetic closes the loop: 45% × 2.5R − 55% × 1R =
+0.575R per trade before costs. The entire game is holding the average loss at 1.0R — no
averaging down, no revenge trades, no "it'll come back." At that point the discipline *is* the
edge, because the counterparties (§6) demonstrably cannot hold the asymmetry. This is what the
[new-high checklist](../systematic-trading/checklists/new-high-trade-checklist.md) and the
[replay gym](replay-gym.md) are actually training.

---

## 9. The one-question edge test

Every durable technique above is a transfer with a **nameable payer paying for a persistent
reason**: hedgers pay for insurance (§1 vol, §4 carry); the rule-bound pay for immediacy at
known times (§2); the slow pay the fast (§3); the constrained pay for balance sheet (§4
low-beta, §5 basis); the emotional pay the disciplined (§6, §8). The macro version is
Gabaix–Koijen's inelastic-markets estimate — a dollar of flow moves ~five dollars of aggregate
equity value — flows move prices, so knowing flows *is* knowing returns.

The test, for any proposed trade at any scale: **who is paying me, why do they keep paying, and
what is my evidence that I'm early in the queue rather than the exit liquidity?** If the answer
names a mechanism on this page, you have a candidate edge — send it through §7's machinery. If
the answer is "the chart looks strong" or "it went up after the last three prints," you haven't
found the payer, which usually means you *are* the payer.

---

## Confidence & verification flags

From-training synthesis, knowledge cutoff Jan-2026. **High confidence:** the mechanisms, model
structures, formulas, and the core results of named papers (Avellaneda–Stoikov,
Cont–Kukanov–Stoikov, MOP 2012, Daniel–Moskowitz, Gatev et al., Frazzini–Pedersen, George–Hwang,
Bali et al., McLean–Pontiff, Harvey–Liu–Zhu, Bailey–López de Prado, Moreira–Muir,
Gabaix–Koijen, Budish et al., Nagel, Osler, Novy-Marx, Lo–Mamaysky–Wang). **Medium confidence
(flagged "verify" inline):** current post-decay magnitudes — the latency-tax bp figure, current
carry and trend net Sharpes, VRP monthly-positive rate, queue-imbalance hit rates. These are
lint-pass candidates, per this wiki's verification culture.

## Relationships

- [What elite traders actually know](what-elite-traders-actually-know.md) — who knows what and
  the honest bounds; this page is how that knowing becomes P&L.
- [Trading-system fundamentals](trading-system-fundamentals.md) — the Edge × Risk ×
  Implementation frame this page fills in.
- [The quant trader's curriculum](quant-trader-curriculum.md) — what to study to execute these,
  ranked by ROI.
- [Cost-aware trading](cost-aware-trading.md) — §7's cost stack, in depth.
- [Small-account edge map](retail-capital-edge-map.md) — which techniques survive at ~$1.4k scale
  (measured, not assumed).
- [The present-state stack](present-state-stack.md) — the tooling that makes §2's flows visible
  at retail cost.
- [Navigating nonlinear markets](navigating-nonlinear-markets.md) — §7's survival layer as a
  standalone doctrine.
- [The replay gym](replay-gym.md) / July-2026 sprint — training reps for
  §8's discretionary skill stack.

## Open questions

- Which §2 flow techniques are measurably *less* arbed in KR markets than US (KOSPI200 rebalance,
  KRX short-sale rule changes) — a live desk-relevant research question.
- The §1 queue-imbalance and VRP magnitudes need current-data verification (flagged above).
- Where exactly is the §3 complexity-arbitrage frontier moving as LLM ingestion commoditizes
  layers of it — what stays human-hard longest?
