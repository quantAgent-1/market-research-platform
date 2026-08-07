---
type: concept
title: The AI capex war — why cash machines borrow, why nobody can stop, and where the rents go
description: Answers "how can Big Tech be strained by AI capex when they print money?" — the rate-vs-stock arithmetic, the arms-race game theory that forbids stopping, why commoditization migrated the rents upstream to chips/memory, and why circular vendor financing appears exactly at this stage of every capex war.
tags: [market-research, semis, shared, financing]
timestamp: 2026-07-31T00:00:00Z
status: active
sources: [../../sources/deep-research-batch-2026-07-31-five-briefs.md]
---

# The AI capex war — why cash machines borrow, why nobody can stop, and where the rents go

Written 2026-07-31, prompted by the user's question after the credit-stack verification: "I thought
Big Tech could never run out of cash. Why is AI capex straining their financing? I thought Google
would dominate; instead everyone is entangled with massive capex and circular financing from
Nvidia. What is going on?" All numbers below are from the verified batch
([source page](../../sources/deep-research-batch-2026-07-31-five-briefs.md)) or this week's
verified prints.

## 1 · The arithmetic: a cash machine has a rate, and the bill outgrew the rate

The intuition "they earn so much they can never run out" confuses a *stock* with a *rate*. Nobody
ran out of money. What happened is that the *investment rate* crossed the *cash-generation rate* —
for the first time in Big Tech's history.

The pre-AI baseline: hyperscalers spent roughly 10–15% of revenue on capex. Alphabet's full-year
2023 capex was about $32B. Its 2026 guide is $195–205B — call it six times the old bill — against
operating cash flow that maybe doubled. The verified Q2 2026 snapshots make the crossing explicit:

- **Alphabet:** Q2 capex $44.9B vs operating cash flow $39.1B → free cash flow **−$5.9B**, the
  first negative quarter since IPO. Capex is running near 37% of revenue.
- **Meta:** Q2 capex $31.1B vs operating cash flow $31.9B → FCF **$784M**, ~zero. Capex ≈ half of
  revenue.
- **Microsoft:** Q4 capex ~$41B vs net income $35.8B — self-funding, but roughly 1:1.
- **Amazon:** Q2 capex $54.2B, full-year raised to $220B *citing memory prices*.

When capex exceeds operating cash flow, the difference must come from somewhere, and there are
only three somewheres: run down the cash pile (finite, and boards protect it), issue debt, or
issue equity. Hence the verified financing wave: Alphabet's $84.75B equity raise (the largest in
US corporate history) plus 100-year bonds, Meta's $55B of bonds and a $27B off-balance-sheet SPV,
Amazon's ~$62B of bonds this year, Oracle downgraded to one notch above junk. This is not
distress. It is what *any* industry looks like once capex-to-revenue passes ~30% — railroads,
telecoms, utilities: capital-markets-funded by arithmetic necessity, regardless of how profitable
the operator is.

Three things made the bill explode rather than grow:

1. **The unit of capacity changed.** A traditional data-center dollar bought buildings and CPU
   servers depreciating over 5–6 years. An AI data-center dollar is mostly accelerator hardware
   (GPUs plus HBM) with a 3–5 year economic life, plus gigawatt-scale power infrastructure. The
   spend is not one-time — the fleet must be *replaced* on a ~4-year cycle, so today's capex is
   tomorrow's permanent depreciation charge.
2. **Input costs are in a squeeze.** Memory pricing (+90% then +50–60% QoQ through 2026) feeds
   directly into the bill — Amazon raised its guide $20B explicitly for memory; Apple called it
   "a 100-year flood." The buyers' arms race bids up the very components the race consumes.
3. **Demand is genuinely there today.** Azure +43%, AWS +37% (fastest since 2021), Meta
   "demand-constrained for the foreseeable future," $496B AWS backlog. This is what makes the
   spending *defensible* quarter by quarter — and what makes stopping feel impossible.

## 2 · The game theory: why nobody can stop

The user expected a winner (Google) funding its capex from monopoly rents. What exists instead is
an **arms race among fortress-holders under a winner-take-most belief** — and that structure has a
brutal property: the loss function is asymmetric. If you underinvest and AI turns out to be the
platform shift, you lose your *existing* fortress (search, the OS, the social graph, the cloud
franchise) — an existential loss. If you overinvest and returns disappoint, you lose *money* — a
survivable loss. Every board doing that comparison chooses overinvestment. Alphabet and Meta have
both said versions of "the risk of underinvesting is dramatically greater than the risk of
overinvesting" on the record.

And no one can stop *unilaterally*: current AI demand is real and provable (the cloud growth
numbers above), so a capex cut today means visibly ceding workloads to the rival's cloud this
quarter — while the payoff of discipline arrives only if everyone else also stops. That is a
prisoner's dilemma with quarterly score-keeping. Cartel-style mutual restraint is illegal and
unenforceable. So the equilibrium is: everyone spends at the maximum fundable rate, and the
"fundable" constraint — not the "sensible" constraint — is what binds. Which is why the funding
mix, not the capex number, is where the strain first shows.

## 3 · Why there is no winner: commoditization moved the rents upstream

The reason Google didn't simply win is that the *product* being raced over — frontier model
capability — has commoditized faster than any platform product in tech history. The capability
gap between the leader and the pack is measured in months; open-weight releases (the Kimi-K3
class) collapse inference pricing from below; distillation lets followers ride leaders' work.
Meanwhile each giant owns a *different* distribution fortress, so nobody can be evicted either.
The result is mutual siege: no one dies, no one wins, everyone must keep paying.

Standard industrial economics says what happens next: **when an oligopoly arms-races over a
commoditizing product, the economic rent migrates to the bottleneck suppliers.** That is exactly
the observed 2026 income statement: Nvidia at ~75% gross margin, TSMC at record revenue, SK Hynix
printing a 76% operating margin and Samsung's DS division ₩89T in a quarter — while the *payers*
grind toward zero free cash flow. The rent went to the ammunition makers. (This is why the memory
thesis and the "Big Tech is strained" observation are the same fact, not a contradiction — and
why the equity market spent this week rationing the payers by funding quality: Microsoft and
Amazon rewarded, Google and Meta punished, exactly along the self-funding line.)

There is also a sharper possibility the desk should hold: **even the eventual winner may earn
ordinary returns**, because competitive investment dissipates the prize ex ante — everyone pays
the entry fee, the fee keeps rising, and much of the surplus ends up with input suppliers and
consumers (cheaper intelligence) rather than shareholders. Nobody in the race can act on that
possibility, because dropping out loses the fortress. That is what "no clear winner, everyone
entangled" is: not confusion, but the stable equilibrium of the game.

## 4 · The circular financing: what the Nvidia web actually is

Circular financing is not an exotic conspiracy; it is what *always* appears at this stage of a
capex war, for one reason: **the marginal buyer of capacity is credit-constrained.** The
hyperscalers can fund themselves (at rising cost). But the fastest-growing buyers — OpenAI-class
labs and the neoclouds — are non-investment-grade or private. Debt markets balk (lenders demanded
the guarantee *because* OpenAI is not creditworthy at this scale). So the vendor with the deepest
pockets and the most to gain steps in:

- Nvidia invested ~$30B in OpenAI's $122B round (closed Mar-31 at $852B post-money) and is *in
  talks* — still unsigned — on ~$250B of lease/construction guarantees plus ~$350B of chip
  financing for the Ohio campus.
- The xAI structure is the purest form: a $20B round split ~$7.5B equity + ~$12.5B SPV debt,
  where the SPV *buys Nvidia chips and rents them to xAI*.
- CoreWeave and peers borrow >$20B against GPU collateral whose residual value depends on…
  Nvidia's own product cadence. Their CDS trades at ~855bp (~50% implied five-year default odds)
  even as one facility achieved the first investment-grade GPU-backed rating.

Everyone is simultaneously everyone else's customer, supplier, investor, and creditor: Microsoft↔
OpenAI, Amazon↔Anthropic (an $8B stake now marked at a $53.4B gain — Anthropic buys AWS capacity),
Google↔Anthropic, Oracle carrying an OpenAI-concentrated $638B backlog, Nvidia touching all of
them. The circularity means the demand signal is partially *endogenous* — Nvidia's revenue is in
part its own balance sheet coming back to it — and it means equity and credit markets
double-count the same underlying exposure.

The historical template is telecom 1999–2002: Lucent and Nortel financing their own customers,
circular revenue, overbuild, then a two-year unwind when demand *timing* missed — note that
internet traffic really did explode; the bust was about leverage meeting a schedule, not about
the technology being fake. The verified differences this time: the core borrowers are AAA cash
machines rather than startup carriers (better core), GPUs depreciate far faster than fiber
(faster residual risk), power scarcity caps the overbuild rate, and the leverage sits in SPVs and
private credit rather than on vendor balance sheets (same risk, different legal form, less
visible). That mix — better core, worse tail, less visibility — is the honest one-line grade.

## 5 · How it ends, and what to watch

Capex wars end one of three ways: a winner emerges and the losers' budgets collapse (the
concentration outcome); ROI evidence forces budget discipline payer by payer (the market already
started this — the funding-quality split of Jul-29/30 is its first tape print); or the credit
channel breaks first at the weakest link and forces it (the T2 path — which is why the five
tripwires from the credit report matter: Oracle losing IG, CoreWeave CDS >1,000bp or a failed
refinancing, the Nvidia guarantee signed-then-called or abandoned, the data-center ABS window
closing, a private-credit vehicle gating). For the memory position specifically: the war *is* the
demand; the order book's quality now varies by payer; and the same autumn window that sets 2027
capex budgets (Sept–Oct) is when the war's continuation gets re-underwritten. Until then, the
strain shows up not in capex cuts but in *how the checks are funded* — which is now a monitored
dashboard, not a vibe.

## Relationships

- Verified numbers: [deep-research batch 2026-07-31](../../sources/deep-research-batch-2026-07-31-five-briefs.md)
  (credit stack §1) · the week's prints in the
  adjudication-week live thread §9/§13.
- Sibling concepts: [equity duration & narrative regimes](equity-duration-and-narrative-regimes.md)
  (how this reprices) · [after the earnings game](../../synthesis/after-the-earnings-game.md)
  (why the 2027 budgets are unknowable in advance) ·
  [second-derivative cycle trading](second-derivative-cycle-trading.md) (the memory-side cycle
  machinery this war feeds).
- The desk's standing risk articulation: T2 in the
  [state of play](../../market-research/semis-ai-state-of-play-2026-07-09.md); the Lucent mechanic
  first named in the live thread §7.
