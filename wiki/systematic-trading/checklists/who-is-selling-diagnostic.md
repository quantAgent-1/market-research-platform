---
type: checklist
title: The "Who Is Selling?" Diagnostic — reading institutional flow on a red day
description: A 15-minute run-the-list procedure for any big down day — decide whether the selling is forced/mechanical flow or real information, using only observable data, before making any decision. Built from the July 2026 cascade, where every step had a live receipt.
tags: [systematic-trading, market-research, positioning, korea]
timestamp: 2026-07-31T00:00:00Z
status: active
sources: []
---

# The "Who Is Selling?" Diagnostic

You cannot see Citadel's book. Nobody outside Citadel can. What you *can* do is answer a better
question on any red day: **is this selling forced/mechanical, or is it informed?** Big institutions
are rule-bound machines — pod stop-outs, margin formulas, CTA thresholds, rebalance calendars — and
rules leave fingerprints in public data. This list finds the fingerprints. Run it in ~15 minutes
before touching the position.

The point of the exercise, learned the hard way in July 2026: the answer decides which mistake you
are most at risk of. Forced selling means the risk is *capitulating at the low*. Informed selling
means the risk is *holding through a thesis break*. You cannot protect against both at once, so
find out which day you are in.

## Step 1 — The dispersion test (2 min)

Compare the single names to the index. Are your names down 5–10% (3σ+ moves) while the index is
down ~1% and the VIX is under ~22? That combination — **exploding single-name vol inside a calm
index** — is the signature of deleveraging and positioning, not information. Real information
events (macro shocks, credit events) move everything together and spike index vol.

*July receipt: SK Hynix had −9% to −15% days while the VIX never crossed ~21 the entire month.
That was the tell, visible every single day, that this was a positioning event.*

## Step 2 — The Korea cohort check (3 min, free)

For KRX names, pull the day's per-name net flows by investor type (KRX/Naver Finance, published
daily): foreigners, institutions by subtype, retail. Then check the KOFIA margin-balance data
(신용융자, published daily) for the leveraged-retail fuel gauge.

- Foreigners dumping + retail absorbing = distribution or rotation. Ask what mechanical channel
  could explain the foreign print (index rebalance, ADR conversion arb, a global fund de-grossing)
  before assuming a view.
- High margin balance + consecutive down days = a 반대매매 (forced margin liquidation) conveyor
  belt is loaded for tomorrow's open. Morning weakness that follows is *mechanical*.

*July receipt: foreigners net-sold ₩4.98T on the breaker day while individuals bought ₩4.32T on
margin — which loaded the forced-selling cascade that ran for the following four sessions.*

## Step 3 — The news-reaction test (2 min)

Did good news get sold today — or recently, repeatedly? A record print sold hard is not "the
market is stupid"; it says positioning is heavy and holders are using liquidity events to exit.
Track the *streak*, not the single day. A good-news-sold streak = narrative/distribution regime.
The streak *breaking* (good news finally bought) is a regime-change marker worth more than any
single print.

*July receipt: every rally attempt from June 22 on was sold within 1–3 sessions — until July 30–31,
when capex raises were finally bought. The break coincided exactly with the forced seller clearing.*

## Step 4 — The mechanical calendar (1 min)

Check the forced-flow calendar: options expiry, quarter/month-end rebalancing, index
adds/deletes, levered-ETF rebalance pressure, lockup expiries, futures roll. If today sits on one
of these, a chunk of the selling has a boring explanation with a known end date.

## Step 5 — Stress markers (5 min)

Scan the wires for the leverage chain waking up. These are all public, usually same-day or
same-week:

- **PB flow notes leaking into Reuters/Bloomberg** ("hedge funds net sold semis for a 4th week" —
  that exact headline ran July 6, 2026, three weeks before the climax).
- **Margin call / de-grossing headlines** (Hedgeweek had Goldman/JPM auto-triggered margin calls
  on July 29 — the day before the auction).
- **Published CTA threshold levels** (banks publish the index levels where trend followers flip;
  Goldman's note flagged the Nasdaq breach on July 19).
- **Crowding data** (Hazeltree's 53%→70% semis net-long print ran July 16 — crowding is not a
  direction signal, it is a *fragility* signal: it tells you how much forced supply exists if
  price falls).
- **Breakers, sidecars, halts, block trades, record short interest, borrow spikes.**

## Step 6 — Verdict and the standing rules

Call it: **FLOW day** or **INFORMATION day** (or honestly mixed). Then apply the rules:

1. **Flow is not information.** No thesis exit on a flow verdict. The exit triggers are the
   pre-committed tripwires (capex language, revision clusters), never the tape alone.
2. **Never buy the middle of a cascade.** Forced selling ends discretely — a cleared auction, a
   seller-exhaustion print (down-open/up-close on record volume, a V-reversal, a limit-move
   reversal). Wait for the seller-removed signature; it is violent and hard to miss.
   The [V-day checklist](catching-the-v-day-checklist.md) is the entry procedure for that morning.
3. **Crowding today is forced flow tomorrow.** When the crowding data is extreme, cut leverage
   *before* the fragility expresses — that is the only time the information is cheap.
4. **If you cannot tell, size as if it's information and act as if it's flow** — hold the thesis,
   but only at a size that survives being wrong.

## Honest limits

This diagnostic protects your *judgment*, not a account. Reading July correctly as
flow-not-information did not tell anyone the cascade would run −55% peak-to-trough on the leader —
depth is unknowable because remaining supply is unobservable. Only sizing protects the account.
The diagnostic's real job is preventing the two expensive mistakes: capitulating into a forced
low, and dip-buying a genuine thesis break because "it's just flow."

## Relationships

- The month this list is built from: the Situational Awareness unwind note
  (the five-act mechanism the fingerprints belong to).
- Entry procedure for the exhaustion morning: [catching the V-day](catching-the-v-day-checklist.md).
- Exit machinery on the information side: [the tripwire exit machine](tripwire-exit-execution.md).
- The observability ladder (what flow data exists at what lag, Korea vs US): the positioning
  sections of the trading-fundamentals session record.
- The tool that automates steps 2/4/5: [the semis institutional flow map](../../designs/semis-institutional-flow-map.md)
  + the [forced-flow calendar](../../designs/index.md).
- Ledger rows this exercises: M7 (KRX plumbing) · M15 (forced-unwind plumbing) · M16 (nowcast/alt-data boundaries).
