---
type: concept
title: Prediction-First Market Making — Reverse-Engineering the Machine
description: The mathematical reconstruction of the XTX-style market maker from public literature — the fair-value engine (microprice, OFI, flow memory), quoting as stochastic control (Avellaneda–Stoikov reservation price + alpha term, the GLFT skew formula and the franchise-flow moat loop), the internalize-vs-hedge decision (Barzykin–Bergault–Guéant three-zone policy, Butz–Oomen queue view, BIS ~80% internalization ratios), toxicity pricing and last look as an option, the multi-asset risk book, and the P&L ledger — each layer tagged published-theory / documented-practice / inference.
tags: [systematic-trading, market-making, microstructure, stochastic-control, ml-stats, fx]
timestamp: 2026-07-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md]
---

# Prediction-First Market Making — Reverse-Engineering the Machine

**In plain language.** This page rebuilds, from published mathematics, the machine sketched on the
[XTX Markets](../../shared/people-firms/xtx-markets.md) page: forecast where the price is going,
center your quotes there, let the position breathe when the forecast says it's safe, and exit by
*shading* your prices so other people's trades carry your risk away. None of XTX's actual models
are public — but the *shape* of the machine is forced by the economics, the way an engine's shape
is forced by thermodynamics, and almost every component has an open-literature version with a
closed-form solution. Each section below is tagged: **[T]** published theory, **[P]** documented
industry practice, **[I]** inference.

The whole machine compresses to three equations and one decision rule:

1. **A forecast:** fair value now = observed price + what the order flow, book and correlated
   markets say the price will do next.
2. **A quote rule:** quote center = fair value **+ alpha term − inventory-penalty term**; spread
   set by volatility and flow elasticity.
3. **A skew formula:** the inventory penalty per unit held shrinks as your franchise flow grows —
   which is the moat, written as math.
4. **A decision rule:** internalize (hold + skew) while inventory is inside a band whose width the
   forecast sets; hedge externally only past the band.

---

## 0. Why forecasting is the only clean escape — the quote is a written option **[T]**

A resting two-sided quote is a pair of free options granted to the market (Copeland–Galai 1983):
anyone may trade at your price *after* observing things you haven't reacted to yet. The value you
give away per fill is the **adverse-selection cost**, measured by the **markout**:

> m(h) = E[ direction-signed price move over horizon h | you got filled ]

— read: "after someone sells to me, how far does the price keep falling, on average?" A maker
earns, per fill, **half-spread − m(h\*) − fees**, where h\* is the horizon at which the position
is actually closed. Empirical markout curves rise and plateau; the plateau is the information
content of the average counterparty. Three ways to stop the bleeding, which are the three
businesses on the [landscape](algorithmic-trading-landscape.md):

- **React faster** (speed): cancel before the informed can hit you; m falls because the option's
  time-to-expiry shrinks. Arms race; the marginal microsecond decays in value.
- **Select the counterparties** (flow access): buy retail flow whose m ≈ 0 by construction (PFOF).
- **Re-strike continuously** (prediction): replace the observable mid with a forecast fair value
  ŝ = E[S_{t+h} | everything observable]. If ŝ is the true conditional expectation, the
  *predictable* component of m vanishes — fills against you are only informative about what
  *nobody* could compute. Most short-horizon adverse selection **is** predictable (it comes from
  autocorrelated order flow, not secrets), which is why this works.

---

## 1. The fair-value engine ŝ — what the forecast is actually made of **[T] + [P]**

The estimator stack, from static to learned. Write the general form as

> **ŝ_t(h) = S_t + Σ_k β_k(h)·x_{k,t} + f_θ(x_t)** — one forecast *per horizon* h,

because different decisions consume different horizons: quote-centering needs 100ms–10s, the
hold-vs-hedge decision needs 1min–1h. A real desk maintains a **term structure of forecasts**.

**The canonical features x_k (all published):**

- **Book imbalance → microprice.** The mid is biased when the book is lopsided. First fix: the
  size-weighted mid, M_w = I·P_ask + (1−I)·P_bid with I = Q_bid/(Q_bid+Q_ask) — note the
  inversion: heavy *bid* size pushes fair value *up* toward the ask. Second fix: Stoikov's
  **microprice** (2018) — the fixed point ŝ = E[mid at the next quote change | imbalance, spread],
  i.e. the price purged of predictable bid-ask bounce. This alone is a usable 100ms–1s forecast.
- **Order-flow imbalance (OFI).** Cont–Kukanov–Stoikov (2014): the net of size added/removed at
  the best quotes explains contemporaneous price changes with R² ≈ 60–70% in 10-second buckets,
  with slope λ ∝ 1/depth — the tape-level version of Kyle's lambda. Flow moves price *mechanically*;
  measuring it precisely is half the forecast.
- **The long memory of order flow.** Trade signs autocorrelate with a power-law decay,
  ρ(τ) ~ τ^{−γ}, γ ≈ 0.5 (Lillo–Farmer 2004) — because institutions split parent orders into
  hours-to-days of child orders (the [√-law footprint](../../shared/concepts/transaction-costs.md)).
  Plain consequence: **recent net buying predicts future buying**, and since future buying moves
  price, flow-history is a genuine return forecast. This is the single most load-bearing feature
  family, and it is public physics, not secret sauce.
- **Cross-asset lead–lag.** Futures lead cash; EUR and JPY majors imply EURJPY within a no-arb
  tolerance; indices lead constituents; the primary FX venues (EBS/LSEG) lead secondary pools.
  At XTX's breadth this becomes one *global* state: a Chicago futures tick re-prices a London
  spot quote. Reacting to public cross-asset ticks is the *defensive* speed layer (table stakes);
  the edge component is the part of ŝ others can't compute from the same ticks.
- **Urgency signatures.** Sweeps (multiple levels consumed at once), quote-fading by other LPs,
  venue-of-origin, time-of-day/session, event flags (data releases, the 4pm WM/R fix window —
  mechanical flow you stand aside from or price for).

**What the ML layer adds [P schematically, I in detail].** The linear-β version of ŝ was the
2010s state of the art and is still the backbone. Industrial scale changes three things: (i)
**pooling** — one model family fit across thousands of instruments with instrument embeddings
(more data per parameter; a new listing inherits the physics of all others); (ii) **interactions**
— imbalance × volatility-regime × session × queue-state nonlinearities that linear βs miss;
(iii) **sequence encoders** over raw event streams instead of hand-bucketed features (the
"deep-LOB" literature made public versions of this). The honest magnitudes: per-event R² is tiny
— IC (signal-return correlation) of **1–5% at seconds-to-minutes** is realistic and *sufficient*,
because [Grinold](../../shared/concepts/factor-premia-and-alpha-decay.md) does the rest:
IR ≈ IC·√N with N = millions of quote decisions/day across 50,000 instruments. The 25,000 GPUs
buy breadth-times-frequency, not oracle accuracy on any single tick.

---

## 2. Quoting as stochastic control — the reservation price and the skew formula **[T]**

The canonical model (Avellaneda–Stoikov 2008, on Ho–Stoll 1981; textbook treatment
Cartea–Jaimungal–Penalva ch. 10; the [HJB machinery](../../shared/concepts/stochastic-optimal-control.md)
underneath). Setup: mid dS = σ dW; you choose bid/ask offsets δ_b, δ_a; fills arrive Poisson with
intensity λ(δ) = A·e^{−kδ} (A = franchise flow rate at zero offset, k = clients' price
sensitivity); inventory q; CARA risk aversion γ; horizon T. Two famous outputs:

> **Reservation price:** r(q,t) = S − q·γσ²(T−t)
> **Optimal total spread:** δ_a + δ_b = γσ²(T−t) + (2/γ)·ln(1 + γ/k)

Plain reading: your *personal* fair value slides **linearly against your inventory** — long one
more unit ⇒ value it γσ²(T−t) lower ⇒ your ask automatically becomes the street's most
aggressive and your bid the most passive. **Skew is not a heuristic; it falls out of the HJB as
the shadow price of inventory risk.** The spread has two parts: an inventory-risk part (γσ²) and
a flow-elasticity part (ln(1+γ/k)/γ — how much edge the client base lets you charge).

**Add the forecast [T].** Let the mid drift: dS = ν_t dt + σ dW, with ν_t the ML alpha
(mean-reverting at speed ρ — alphas decay). The Cartea–Jaimungal class of solutions shifts the
quote center by the *integrated expected drift*:

> **r(q,t) ≈ S + ν_t/ρ − q·γσ²(T−t)**   (constants model-specific; the structure is general)

ν_t/ρ = "the total move my current signal still has in it." This one line **is** the
prediction-first market maker: center = price + alpha − inventory penalty. Set ν=0 and you are a
classic inventory MM bleeding predictable markouts; set γ→large and you are a nervous hedger; the
machine is the balance of the three terms. It also *is* the sentence "the forecast tells you it's
safe to hold": conditional on ν_t ≥ 0, a long position has non-negative drift — holding costs
only variance; conditional on ν_t ≪ 0, the same inventory is a losing lottery ticket and the
optimal control hedges it *now*.

**The infinite-horizon closed form and the moat loop [T].** Guéant–Lehalle–Fernandez-Tapia (2013)
solve the stationary version exactly. The asymptotic quotes are

> δ_b(q) ≈ c₀ + (2q+1)/2 · **C**,  δ_a(q) ≈ c₀ − (2q−1)/2 · **C**, with
> **C = √( (σ²γ)/(2kA) · (1+γ/k)^{1+k/γ} )** and c₀ = (1/γ)ln(1+γ/k)

so the quote center sits at **S − q·C**: the skew per unit of inventory is the single constant C.
Look at what C depends on: **C ∝ σ·√(γ/(2kA))** — *decreasing in franchise flow A*. Plain
consequence, and it is the deepest line on this page: **the more client flow you attract, the
less you must skew per unit of risk, so your quotes are tighter, so you attract more flow.** The
moat is a fixed point of that loop. XTX at ~$300B/day sits near the fixed point; a new entrant
with 1% of the flow needs √100 = 10× the skew to bear the same inventory — visibly worse prices.
This formula is why "just copy the strategy" fails even with the models in hand.

---

## 3. Internalize vs hedge — the decision rule with numbers **[T] + [P]**

Inventory q arrives (the worked example: client selling leaves you long $80M EURUSD). Two exits:

**(a) Externalize now:** cross the interdealer market. Cost = half-spread + √-law impact
(≈ Y·σ_day·√(Q/ADV), Y ≈ 0.5–1) + **footprint** — your hedge print both moves the market against
the rest of a book and shows predators a position. For $80M in EURUSD (ADV ≈ $0.6T,
σ_day ≈ 50bp): impact ≈ 0.7·50bp·√(80M/600B) ≈ **0.4bp ≈ $32K**, plus spread — an all-in **$35–65K
certain cost**, before the signaling externality.

**(b) Internalize:** hold, and shade both quotes lower by a fraction of C·q so natural buyers
lift your offer. You *earn* the client half-spread on the way out instead of paying the market's.
The price of waiting is inventory variance: σ ≈ 1.3bp/√min on EURUSD ⇒ over a ~10-minute offload,
1σ ≈ 4bp ≈ **$33K of noise, mean ≈ zero conditional on ν_t ≈ 0**. A risk-neutral desk would
*always* wait (zero-mean noise beats a sure cost); a risk-averse desk waits inside a band; and
the forecast is the triage — ν_t sufficiently negative (the flow that filled you was informed)
flips the answer to "pay the $50K and hedge now."

The published formalizations of exactly this problem:

- **Butz–Oomen (2019)** model internalization as a risk *queue*: offsetting client arrivals
  service your inventory; the probability of internalizing before your risk limit forces a hedge
  is increasing in franchise flow and decreasing in clip size — the queueing-theory version of
  the moat loop. **[T]**
- **Barzykin–Bergault–Guéant (2021–23)** solve the full FX-dealer control problem — controls =
  per-client quote skews *and* an external hedging rate with impact costs — and the optimal
  policy comes out **three-zone**: |q| small → pure internalization (skew only); |q| middling →
  skew + trickle external hedging; |q| past a threshold → aggressive externalization. The band
  edges widen with franchise flow and tighten with volatility. This paper series is, in public
  math, the machine the quoted paragraph describes. **[T]**
- **The measured reality:** BIS studies of FX dealing (Schrimpf–Sushko, BIS Quarterly Review 2019)
  report top-tier dealers internalizing on the order of **80%+ of flow in liquid pairs** — i.e.
  only a small minority of client risk ever touches the visible interdealer market. The lit FX
  tape is the exhaust pipe, not the engine. **[P]**

**Why the skew must be *discreet* [P].** A skewed price is itself information — broadcast it on an
anonymous venue and sharp counterparties reverse-engineer your inventory and trade ahead of your
exit ("skew leakage," a named problem in e-FX practice). Hence the structure of the modern dealer:
**disclosed bilateral streams** (OTC FX legally allows different prices to different clients),
full-amount quoting, and skew shown only to counterparties whose markouts prove them benign. The
equities version of the same need is the systematic-internaliser / wholesaler mechanism. This is
why internalization at scale is a *relationship* business wrapped around a control problem.

---

## 4. Toxicity pricing and last look — the counterparty dimension **[P] + [T]**

The maker's realized adverse selection is a flow-weighted average of per-counterparty markouts —
so improving the *mix* is worth as much as improving the forecast. Practice, documented in the
e-FX ecosystem's own scorecard culture: tag every fill by counterparty/venue/size/session,
maintain **markout curves per segment** (m_c(h) for client c), and price discriminate — tighter
spreads and more size to flow that doesn't run you over; wider, smaller, or nothing to flow that
does. This is the [informed-vs-uninformed identification problem](../../shared/concepts/informed-vs-uninformed-flow.md)
run live with a measurable answer, because the maker sees its own fills' outcomes — the luxury an
outside observer never has.

**Last look** is the FX convention that lets a liquidity provider reject a trade in a hold window
*after* seeing it — economically a free option on the price move during the window: value/fill ≈
E[(adverse move during τ − tolerance)⁺], modeled in Oomen (2017). Tiny per trade, enormous ×
volume, and it protects *lazy quoting* (you can stream stale prices and reject the fills that
would have punished you). XTX's public zero-hold-time stance is thus exactly what the
prediction thesis predicts: **a firm whose ŝ is good enough doesn't need the option and profits
from a regime where rivals lose it.** Doctrine and mechanism are one piece.

---

## 5. The multi-asset book — risk exits through the cheapest door **[T] + [I]**

Everything above, vectorized: inventory **q**, covariance **Σ**, penalty γ·**q**ᵀΣ**q**, and the
reservation price of instrument i becomes

> r_i ≈ S_i + (alpha_i) − γ·(Σ**q**)_i·(horizon factor)

The skew on *each* instrument depends on the **whole book** through Σq (Bergault–Guéant's
multi-asset closed-form approximations). Three consequences: (i) an $80M EURUSD long can be bled
off through EURGBP, futures, or any correlated stream — whichever client flow shows up first;
(ii) client flows across correlated instruments net in *risk space* even when they never cross in
the same instrument — so internalization capacity scales with **breadth**, a second moat term on
top of the flow loop; (iii) the practical hedge hierarchy: keep idiosyncratic legs internalized,
hedge the common **factor** (USD beta, equity beta) in the single most liquid future when the
band is breached. The 50,000-instrument, single-global-risk-book design is this equation's
architecture, not a stylistic choice. **[I at XTX specifically; T in structure]**

---

## 6. The P&L ledger the desk actually runs **[P]**

Management accounting of a market maker, per day:

> **PnL = Σ fills × half-spread  −  Σ fills × markout(h*)  +  (alpha earned on held inventory)
> − external hedging costs − fees/infra**

Every term is measured (markout curves at several h are the daily report card), and each maps to
a lever: spread capture (pricing), adverse selection (forecast + toxicity mix), inventory alpha
(the ν_t/ρ term — a prediction MM's inventory is a *paid* position, not an accident), hedging
(the three-zone policy). Unit economics check against the [XTX record](../../shared/people-firms/xtx-markets.md):
2025 revenue ≈ $5B on ≈ $75T of annual turnover ≈ **0.6–0.7bp of notional** — same order as
Citadel Securities' ≈ 0.8bp — i.e. the take rate of a toll booth, turned into £1.7B of profit
purely by volume and near-daily positivity (the CLT arithmetic already on the
[industrialization page](../../synthesis/industrialization-of-edge.md): thousands of small
positive-mean bets a day ≈ a Virtu-style 1-losing-day-in-1,238 profile).

**The pricing loop, as pseudocode [I — reconstruction]:**

```
on every market event (any venue, any correlated instrument):
    update features x_t                       # book, OFI, flow memory, cross-asset
    for h in horizons: fair[h] = S + beta(h)·x_t + f_theta(x_t)
    for each (instrument i, client tier c):
        half = base_spread(i, size) * toxicity_mult(c)      # markout-calibrated
        center = fair[h_c] - gamma * (Sigma @ q)[i] * horizon_i   # alpha + inventory skew
        stream quote_c = center ± half                      # disclosed, per-client
    if |(Sigma @ q)| outside band:                          # three-zone policy
        schedule external hedge (factor future first, AC-style trajectory)
    # zero hold time: no last-look option to manage
```

---

## 7. What the 25,000 GPUs are actually for **[I, flagged]**

Not latency — training. The inferable jobs: (i) pooled sequence models over raw event streams at
650PB scale; (ii) the forecast term structure as multi-task heads; (iii) continuous retraining
against nonstationarity; (iv) **counterfactual policy evaluation** — you cannot A/B-test a quote
policy on the live market without paying for the experiment, so you need order-book simulators
(queue-reactive models in the Huang–Lehalle–Rosenbaum line) faithful enough to score candidate
policies offline; (v) plausibly, direct **policy learning** — parametrize the skew/hedge policy
and optimize a risk-adjusted objective end-to-end, which is precisely the *deep hedging*
methodology of XTX's own co-CEO Hans Buehler (2019: replace closed-form hedging with an RL-trained
policy under frictions). His hire is the strongest public hint that the derivatives version of
this page (options market making with learned hedging) is the firm's next act. Speculation,
labeled as such.

---

## 8. Epistemic scorecard — how solid is each layer?

| Layer | Status |
|---|---|
| Quote = written option; markout accounting | **[T+P]** Copeland–Galai; universal desk practice |
| Microprice / OFI / flow long-memory / lead–lag | **[T]** Stoikov; Cont–Kukanov–Stoikov; Lillo–Farmer |
| Reservation price + skew from HJB | **[T]** Ho–Stoll; Avellaneda–Stoikov; CJP ch. 10 |
| Alpha term in quotes | **[T]** Cartea–Jaimungal alpha-MM variants |
| Skew constant C, moat ∝ 1/√A | **[T]** Guéant–Lehalle–Fernandez-Tapia closed form |
| Internalize-vs-hedge three-zone policy | **[T]** Barzykin–Bergault–Guéant; Butz–Oomen queue |
| ~80% internalization; skew leakage; per-client pricing | **[P]** BIS QR 2019; e-FX practice |
| Last look as option; zero-hold doctrine | **[T+P]** Oomen 2017; GFXC record |
| Multi-asset Σ-coupled skew | **[T]** Bergault–Guéant; **[I]** as XTX's actual book |
| ML specifics, GPU allocation, RL quoting | **[I]** — inference from scale, hires, physics |

What this page is **not**: an account of XTX's features, weights, horizons, or risk limits — those
are in nobody's public record. The claim is narrower and stronger: *given* the published theory,
the documented practice, and the firm's stated parameters, a machine of this shape is the unique
sensible design — and every visible fact (GPU capex, holding periods, zero-hold-time lobbying,
disclosed streams, single book, Buehler) is what that shape predicts.

## Relationships

- The firm this reconstructs: [XTX Markets](../../shared/people-firms/xtx-markets.md) ·
  [Alex Gerko](../../shared/people-firms/alex-gerko.md).
- The stub this deepens: [market making](../strategies/market-making.md); machinery:
  [stochastic optimal control](../../shared/concepts/stochastic-optimal-control.md); costs:
  [transaction costs & impact](../../shared/concepts/transaction-costs.md); the counterparty
  problem: [informed vs uninformed flow](../../shared/concepts/informed-vs-uninformed-flow.md).
- Where it sits in the industry: [algorithmic-trading landscape](algorithmic-trading-landscape.md) ·
  [industrialization of edge](../../synthesis/industrialization-of-edge.md) §3b.
- Why this horizon at all: [speed vs prediction](speed-vs-prediction.md) — the tournament-vs-graded-exam
  economics and the IC·σ√h arithmetic that select minutes-to-hours.
- The flow being forecast, from the counterparty's side: [what retail actually trades
  on](what-retail-trades-on.md) — the attention/chart/sentiment signal set whose public-input
  nature is exactly what makes "flow predicts flow" work.

## Open questions

- The FX-dealer control papers assume exponential fill intensities — how badly does the
  three-zone geometry deform under realistic fat-tailed clip sizes and clustered arrivals?
- Queue-reactive simulators good enough for policy evaluation: what fidelity is *sufficient*
  before sim-optimal ≠ live-optimal (the sim-to-real gap that decides whether RL quoting works)?
- Public markout benchmarks: can client-side TCA data (LP scorecards) reveal, from outside,
  whether a given LP prices on forecasts vs last-look optionality?

## References (external; key ones)

Avellaneda & Stoikov (2008), *High-frequency trading in a limit order book*. · Ho & Stoll (1981).
· Guéant, Lehalle & Fernandez-Tapia (2013), *Dealing with the inventory risk*. · Cartea,
Jaimungal & Penalva (2015), *Algorithmic and High-Frequency Trading*, ch. 10
([source page](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md)). · Barzykin, Bergault &
Guéant (2021–23), FX market making with hedging & impact series. · Bergault & Guéant, multi-asset
closed-form approximations. · Butz & Oomen (2019), *Internalisation by electronic FX spot
dealers*. · Oomen (2017), *Last look*. · Stoikov (2018), *The micro-price*. · Cont, Kukanov &
Stoikov (2014), *The price impact of order book events*. · Lillo & Farmer (2004), *The long
memory of the efficient market*. · Copeland & Galai (1983). · Schrimpf & Sushko, BIS Quarterly
Review (Dec 2019), FX execution & internalization. · Buehler, Gonon, Teichmann & Wood (2019),
*Deep hedging*.
