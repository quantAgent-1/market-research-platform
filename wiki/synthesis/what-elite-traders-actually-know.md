---
type: overview
title: "What Elite Traders Actually Know — Prediction, Institutional Knowledge, and Who Moves the Market"
description: New knowledge on the three questions — the elite skill stack; the honest quantitative bounds on predictive knowledge (IC ~0.02-0.05, Medallion's 50.75% hit rate, sub-1% out-of-sample R²); the real institutional information hierarchy (flow visibility, alt data, expert networks) and the documented pockets of genuinely informed trading; and impact physics + cascade mechanics vs. the manipulation case record on who triggers moves.
tags: [systematic-trading, behavioral, microstructure, alpha, market-structure]
timestamp: 2026-07-05T00:00:00Z
status: active
sources: []
---

# What Elite Traders Actually Know — Prediction, Institutional Knowledge, and Who Moves the Market

Filed 2026-07-05 from a session Q&A. Three questions: what does a trader have to know to truly
win; is that knowledge *predictive* — how much do elite traders and institutions actually know
about coming moves; and do they *cause* the moves themselves? The one-paragraph answer: elite
edge is mostly not foresight. Measured honestly, the best predictive knowledge in the industry
is a correlation with next-period returns of a few hundredths — monetized through breadth,
sizing, and cost control, not through being right about the future in any human sense.
Institutions know the **present** — positioning, committed order flow, mechanical calendars —
far better than any outsider, and that present-state map constrains the near future enough to
look like precognition. And most violent moves are triggered mechanically by cascades of
rule-bound actors; deliberate triggering exists at the edges, legal and illegal, but a standing
cartel that paints the tape fails both the evidence and the competition test.

## 1. The skill stack the elite actually train

The public imagines prediction talent; the industry hires and trains something else. Across the
professional spectrum the same five-part stack recurs, and it matches this wiki's
[ROI-ranked curriculum](quant-trader-curriculum.md): sizing and risk first, then flow-reading,
the expectations game, microstructure, and statistical self-defense. What the elite add on top
of the topics is worth naming precisely:

- **Calibration, not conviction.** The measurable skill that separates good forecasters —
  Tetlock's superforecasting result — is not knowing more; it is knowing *how much* they know:
  probabilities stated in fine gradations, updated in small increments, scored against outcomes.
  Trading desks institutionalize this as forecast-vs-realized reviews; the retail equivalent is
  the [morning call sheet](../systematic-trading/checklists/morning-call-sheet.md) with a Brier
  score. Most losing traders have never once scored their own predictions.
- **Ruthless risk mechanics.** At the multi-manager platforms (Millennium, Citadel, Point72) a
  portfolio manager typically loses half the book at roughly −5% drawdown and the seat near
  −7.5% to −10%. Elite institutional trading is *designed* around the assumption that any PM can
  be wrong for months — the risk system, not the forecast, is what survives. The pods are also
  forced market-neutral and factor-neutral, which means the entire job is the residual: sizing
  many small idiosyncratic bets, not calling the market.
- **Asymmetry engineering.** The famous discretionary records are built on payoff shape, not hit
  rate. Paul Tudor Jones frames trades as 5:1 asymmetries — wrong four times out of five and
  still flat. Druckenmiller's stated method is liquidity and positioning over valuation for
  timing, with rare, enormous bets when both align. Soros's formulation: being right or wrong
  matters less than how much you make when right versus lose when wrong.
- **Specialization in one payer.** Real firms do not "trade markets"; they industrialize one
  income stream from the [four payers](../shared/concepts/who-pays-you.md) — Service (Citadel
  Securities, Jane Street, Optiver harvest spread and structural premia), Constraint (index and
  rebalance desks), Premium (asset owners), Mistake (stat-arb and event funds). Only the last
  is even nominally "prediction," and it is run as thousands of tiny bets, never one big call.

## 2. How much genuine predictive knowledge exists — the honest numbers

The quantitative bounds are public and remarkably consistent, and they are the real answer to
"how much do elites know about future movements":

- **The information coefficient.** In the Grinold-Kahn framework that quant desks actually use,
  skill is the correlation between forecast and outcome (IC), and performance follows the
  fundamental law **IR ≈ IC × √breadth**. A *professional-grade* IC is on the order of
  **0.02–0.05** — a 2–5% correlation with next-period returns, indistinguishable from noise to
  the naked eye. Nobody's IC is 0.3. The elite difference is applying that hair-thin correlation
  across thousands of independent bets (breadth), which is why a stat-arb shop with IC 0.03 can
  run Sharpe 2+ while a discretionary trader with the same IC on twelve trades a year cannot.
- **Medallion, the best that has ever existed.** Renaissance's Medallion fund — roughly 66%
  gross (≈39% net) annualized over three decades, capacity deliberately capped around $10B —
  was described from the inside (Zuckerman, *The Man Who Solved the Market*) as being right on
  about **50.75% of trades**. The most successful predictive machine in financial history gets
  the direction wrong ~49% of the time; it simply gets millions of at-bats, sized well, at
  near-zero cost.
- **Out-of-sample R².** The machine-learning asset-pricing literature (Gu-Kelly-Xiu and its
  successors) finds that even the best models predict individual-stock monthly returns with an
  out-of-sample R² of a few *tenths of a percent* (≈0.26% for penalized linear methods, ~0.4%
  for the neural nets, in the *RFS*-2020 benchmark). Campbell-Thompson-style market-timing
  regressions live in the same sub-1% territory. Prediction exists; it is real; it is tiny.
- **The documented anomaly inventory decays.** The edges that were public and real — the
  S&P-inclusion pop (7.4% average in the 1990s → a statistically insignificant 0.8% in the
  2010s; Greenwood-Sammon, *JF* 2025), the pre-FOMC announcement drift (>80% of the US equity
  premium earned in the 24h before scheduled FOMC announcements, 1994–2011, a Sharpe-1.14
  strategy by itself; Lucca-Moench, *JF* 2015 — faded after publication), post-earnings drift,
  classic momentum — lose
  roughly half their returns after publication ([alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md)).
  What survives tends to be flow-mechanical (overnight-vs-intraday return split, expiry
  hedging pressure, [the volatility risk premium](../derivatives/concepts/volatility-risk-premium.md))
  — paid by constraints and hedging demand, not by superior foresight.
- **Tails are out of bounds entirely.** For the moves that matter most, prediction is not hard
  but structurally impossible — the definitional/reflexivity/fat-tail argument in
  [navigating nonlinear markets](navigating-nonlinear-markets.md), with LTCM as the standing
  proof that maximum modeling depth plus leverage is the blowup mode. The partially
  forecastable object is volatility and regime, not direction.

So: is the key knowledge predictive? At the elite level, *predictive knowledge is an input
measured in hundredths of correlation*; the actual key knowledge is the machinery that converts
hundredths into compounding — breadth, sizing, costs, asymmetry, survival.

## 3. What institutions really know — the information hierarchy

Institutions demonstrably do not know outcomes: ~92% of active large-cap funds trailed the
S&P 500 over 20 years, top-quartile persistence measures at 0.00% (below chance), and hedge
funds in aggregate deliver roughly zero alpha after fees — a thin top tier shows persistence,
but it is thin ([the empirical record](../shared/concepts/who-wins-empirical-record.md)). What
they hold instead is a layered, mostly legal information advantage about the **present state of
the machine**:

1. **Flow visibility — the deepest moat.** Wholesalers internalizing retail orders see that
   flow before the market does; Citadel Securities alone executes roughly a quarter of all US
   equity volume and about 35% of US-listed retail flow (company disclosures and industry
   reporting). Dealers see their own
   client order books and their own gamma exposure; prime brokers see aggregate hedge-fund
   leverage, crowding, and de-grossing in real time and publish weekly positioning notes to
   clients. None of this is knowledge of *outcomes* — it is knowledge of **committed present
   demand**, which at short horizons is nearly as good. This is exactly why the
   intraday arena is unwinnable for outsiders (the horizon ecology in
   [who pays you](../shared/concepts/who-pays-you.md)).
2. **The mechanical calendar.** Index reconstitution estimates, quarter-end pension rebalance
   projections (banks publish dollar figures), option-expiry gamma maps, buyback blackout
   schedules, lockup expiries. Public to professionals, invisible to most retail.
3. **Bought information about the present.** Expert networks (GLG, Tegus) selling hour-long
   calls with former employees; channel checks; alternative data — credit-card panels, satellite
   parking-lot counts, app telemetry, web-scraped pricing — that nowcast revenue weeks before
   the print. The legal line is the mosaic theory: assembling non-material public and private
   fragments into a material picture is allowed; a single material non-public fact is not
   (Reg FD tightened the corporate side in 2000).
4. **Speed on public information.** Machine-read headlines, earnings NLP, satellite-to-trade
   pipelines. Detected "informed trading" around announcements is often just this — faster
   processing, not private knowledge
   ([informed vs. uninformed flow](../shared/concepts/informed-vs-uninformed-flow.md)).

And there are documented pockets where *genuinely* informed trading shows up in the data —
worth knowing because they calibrate how much true future-knowledge exists at the edges:
corporate insiders' **opportunistic** (non-routine) trades earn value-weighted abnormal returns
of **82 bp/month** — routine trades: essentially zero (Cohen-Malloy-Pomorski, *JF* 2012;
Lakonishok-Lee before them); fund managers' school-tie-connected positions outperform their
non-connected holdings by **up to 8.4%/yr**, concentrated around corporate news
(Cohen-Frazzini-Malloy, *JPE* 2008); US Senators' portfolios beat the market by **≈1%/month**
in the 1993–1998 sample (Ziobrowski et al., *JFQA* 2004) — an edge that disappears in every
later sample (2004–2008 and post-STOCK-Act studies find nothing). The pattern across all of them: real
informed edges are **local, small-capacity, and attached to specific access** — none of them
scale to "institutions know where the market is going."

The insider channel specifically — trading on MNPI ahead of events — is the *least* likely
explanation of most suspicious-looking pre-event moves: blackout windows bar insiders exactly
when it would matter, 10b5-1 plans are pre-scheduled, detected insider activity clusters
*after* announcements, and pre-event drawdowns in stretched names statistically predict
**reversion, not the outcome**. The desk's own worked example stands: MU −13.18% on
Jun 23, 2026 looked like "someone knows" and was a Korea-led leveraged-ETF forced unwind that
reverted +15.7% in two days.

## 4. Do they trigger the moves?

Three honest layers: physics, cascades, and intent.

**Physics: big money cannot help moving price.** Market impact follows a square-root law that
is one of the most robust empirical facts in microstructure (Kyle's lambda in theory; the
metaorder literature — Bouchaud, Tóth et al. — in practice): expected impact ≈ (0.5–1) ×
daily volatility × √(order size / daily volume). Executing just 1% of a day's volume moves
price on the order of 5–10% of a daily standard deviation — and the cost *rises with the square
root of size*, which is why big funds bleed alpha as AUM grows and why impact is a tax on the
trigger-puller, not a weapon. Institutions move markets constantly, mostly *against* their own
interest, as an unavoidable cost of being large.

**Cascades: the market triggers itself.** The violent moves are chains of rulebooks, not
decisions: realized vol rises → vol-target and risk-parity funds must de-lever; price crosses
published flip levels → CTAs reverse; the close approaches after a big day → leveraged ETFs
must rebalance in the day's direction; margin clocks fire on schedule (Korea's 반대매매
morning sequence — [KRX session clocks](../shared/concepts/krx-session-clocks-and-forced-liquidation.md));
dealers short gamma must hedge *into* the move. Each actor is individually rational and
compelled; nobody coordinates; the aggregate is a flush that overshoots any information content
and V-reverses when the forced flow exhausts
([liquidity cascades](../shared/concepts/liquidity-cascades-and-v-reversals.md)). 1987
(portfolio insurance), Feb-2018 (short-vol complex), Aug-2024 (yen carry), Jun-2026 (Korean
leveraged-ETF memory unwind) are the same machine with different fuel.

**Intent: real but bounded.** Deliberate, *legal* triggering is a standing business: activist
13D filings move targets ~7% on announcement (Brav et al.); short-seller reports (Muddy Waters,
Hindenburg) are engineered information releases; analysts' rating changes move prices; index
providers' add/delete decisions command flows; and central banks are the one actor that openly
announces it will move markets and does (QE, FX intervention). Deliberate *illegal* triggering
is documented, prosecuted, and niche: the LIBOR rigging (>$9B in fines), the FX "Cartel" chat
room (~$5.7B, 2015), spoofing prosecutions from Sarao (the flash-crash contributor) to
JPMorgan's record $920.2M precious-metals-and-Treasuries settlement (DOJ/CFTC, Sep-2020),
banging-the-close cases, microcap
pump-and-dumps. Note what the list has in common: reference rates, fixes, thin books, and
auction prints — the places where one actor's flow *can* dominate. In deep liquid equities, a
would-be tape-painter is donating money to every arbitrageur who fades him; the competitive
structure, plus the SPIVA record showing no one compounds abnormally at scale, is the disproof
of the standing-cartel story. The one true sense in which big money "makes" the future is
reflexivity: a rally that cheapens a company's capital genuinely improves its fundamentals —
Soros's loop, an emergent feedback, not a plan.

## 5. The synthesis

Elite trading knowledge is: **a present-state map** (who is positioned how, who is forced to
trade when) + **a tiny, real predictive correlation** (hundredths, harvested across breadth) +
**machinery that makes being wrong cheap** (sizing, asymmetry, cost control, risk stops at the
institution level). "Do they know the future?" — no, and the SPIVA/persistence/LTCM record
proves it at scale; the pockets of genuine foresight (opportunistic insiders, connected
networks) are small, local, and mostly closed to size. "Do they trigger moves?" — they move
prices constantly by physics and occasionally by intent, but the moves that hurt are
self-triggering cascades of forced flow, which is precisely why they are partially *readable*:
constraints are public in a way opinions never are.

For this desk, that is the whole strategic conclusion: the knowable layer is the
constraint-and-flow machinery — Signal C in [Engine v3](engine-v3/index.md), the
[V-day checklist](../systematic-trading/checklists/catching-the-v-day-checklist.md), the Korea
per-name daily flow data no US retail trader gets — plus the calibration loop that turns
guesses into scored, improving probabilities. That is the same stack the elite run, minus the
seats you cannot buy.

## Sources & documentation status

Filed from the assistant's training, then challenged same-day ("is this documented?") → a live
web-verification pass was run 2026-07-05 over the load-bearing figures. Grades: **[A]**
peer-reviewed paper or official/court record · **[B]** credible book, journalism, or company
disclosure (well-documented, but not an audited public record) · **[C]** practitioner
convention (documented in textbooks; no measured census). ✓ = verified against live sources
this pass; corrections found are noted.

- **[A]✓** Opportunistic-insider **82 bp/mo** value-weighted; routine ≈ 0 —
  [Cohen, Malloy & Pomorski, *JF* 2012](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2012.01740.x)
  ([NBER digest](https://www.nber.org/digest/apr11/decoding-inside-information)). Exact.
- **[A]✓** School-tie connected holdings outperform **up to 8.4%/yr**, concentrated around news —
  [Cohen, Frazzini & Malloy, *JPE* 2008](https://www.nber.org/papers/w13121). *Correction: page
  originally said ~7–8% from memory.*
- **[A]✓** Senate **≈1%/mo** abnormal, 1993–1998 —
  [Ziobrowski et al., *JFQA* 2004](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/abnormal-returns-from-the-common-stock-investments-of-the-us-senate/A39406479940758D59E09FDCB8EE9BEC);
  later samples null — Eggers-Hainmueller (2004–08) and
  ["Senators As Feckless As the Rest of Us at Stock Picking" (NBER w26975)](https://www.nber.org/system/files/working_papers/w26975/w26975.pdf).
- **[A]✓** Pre-FOMC drift: **>80%** of the US equity premium in the 24h before scheduled FOMC
  announcements (1994–2011; the strategy alone ≈ Sharpe 1.14) —
  [Lucca & Moench, *JF* 2015 / NY Fed SR512](https://www.newyorkfed.org/research/staff_reports/sr512.html).
- **[A]✓** Index effect: additions **+7.4%** avg (1990s) → 5.1% (2000s) → **0.8%, statistically
  insignificant** (2010s); deletions mirror —
  [Greenwood & Sammon, "The Disappearing Index Effect," *JF* 2025](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4294297).
  *Sharper than the from-memory "~5–8% → ~0."*
- **[A]✓** ML return prediction OOS R² a few tenths of a % monthly (≈0.26% penalized-linear;
  NNs higher) — [Gu, Kelly & Xiu, *RFS* 2020](https://academic.oup.com/rfs/article/33/5/2223/5758276).
- **[A]✓** JPMorgan **$920.2M** spoofing (record; precious metals + Treasuries, 8 years,
  DPA + admissions) — [CFTC release 8260-20](https://www.cftc.gov/PressRoom/PressReleases/8260-20) ·
  [DOJ](https://www.justice.gov/archives/opa/pr/jpmorgan-chase-co-agrees-pay-920-million-connection-schemes-defraud-precious-metals-and-us).
- **[A]✓** FX "Cartel": five banks, **$5.7B**, May-2015 guilty pleas (Barclays' $2.4B total the
  largest) — [contemporary report](https://www.financierworldwide.com/fw-news/2015/5/21/forex-five-fined-57bn-1);
  LIBOR fine totals **≈$9B** across banks — [case record](https://en.wikipedia.org/wiki/Libor_scandal).
- **[A]** Square-root impact law (impact ≈ Y·σ·√(Q/V), Y≈0.5–1) — Almgren et al. (2005), Tóth
  et al. (2011), the Bouchaud metaorder literature. Not re-verified this pass; robust across
  dozens of studies and venues.
- **[A]** SPIVA ~92%/20y · 0.00% top-quartile persistence · Taiwan day-trader census — already
  linked and verified in [who wins](../shared/concepts/who-wins-empirical-record.md).
- **[B]✓** Medallion: right **~50.75%** of the time ("but we're 100% right 50.75% of the time"
  — Mercer, quoted), **~66% gross** annualized, capacity-capped — Zuckerman, *The Man Who
  Solved the Market* (2019). A sourced WSJ-journalist account; RenTec publishes no audited
  public numbers. Quote verified against multiple excerpts.
- **[B]✓** Pod risk mechanics: **−5% halves capital, −7.5% terminates**, enforced
  algorithmically (Millennium the canonical case; ~15–20% annual PM turnover) — consistent
  multi-source industry reporting (e.g. [Net Interest, "Peak Pod"](https://www.netinterest.co/p/peak-pod));
  no regulatory filing documents these.
- **[B]✓** Citadel Securities ≈**¼ of all US equity volume**, ~**35% of US-listed retail** (some
  reports ~40%), DMM for ~62% of NYSE listings — company statements + industry reporting
  ([IFR](https://www.ifre.com/ifr-awards/2327839/flow-marketmaker-citadel-securities)).
- **[B]** Activist 13D announcement return ≈+7% — Brav, Jiang, Partnoy & Thomas, *JF* 2008
  (magnitude from memory, not re-verified this pass).
- **[C]** "Professional IC ≈ 0.02–0.05" — Grinold & Kahn, *Active Portfolio Management*
  convention (their worked examples treat IC 0.05 as a skilled manager); an order-of-magnitude
  practitioner norm, not a measured census.
- **[B]** PTJ's 5:1 asymmetry (Schwager, *Market Wizards*, 1989 interview) · Druckenmiller on
  liquidity-over-valuation (documented interviews) · Soros right/wrong-vs-make/lose (attributed
  via Druckenmiller) — documented self-descriptions by discretionary traders.

Still cited from memory without a live pass: Brav et al. magnitude, Lakonishok-Lee,
Kosowski/Jagannathan hedge-fund-persistence magnitudes, Lou-Polk-Skouras overnight-vs-intraday
split, Tetlock/GJP details. All name-checked [A]-grade literatures; a deep-research lint can
pin exact magnitudes if wanted.

## Relationships

- [The quant trader's curriculum](quant-trader-curriculum.md) — the ranked skill list; this
  page explains *why* its ordering matches what institutions actually train.
- [Who pays you](../shared/concepts/who-pays-you.md) — the four payers; §1's specialization
  point and §2's "only Mistake is prediction."
- [Who sets price](../shared/concepts/who-sets-price.md) — fast/slow/mechanical pools; the
  present-state map of §3 is a zoom-in on its mechanical pool.
- [Informed vs. uninformed flow](../shared/concepts/informed-vs-uninformed-flow.md) — the
  identification problem behind §3's insider-channel verdict.
- [Who actually wins — the empirical record](../shared/concepts/who-wins-empirical-record.md) —
  the scale-level disproof of outcome-knowledge.
- [Navigating nonlinear markets](navigating-nonlinear-markets.md) — the tail-impossibility
  result assumed in §2.
- [Liquidity cascades & V-reversals](../shared/concepts/liquidity-cascades-and-v-reversals.md) ·
  [KRX session clocks](../shared/concepts/krx-session-clocks-and-forced-liquidation.md) — §4's
  cascade anatomy, intraday version.
- [Price formation & the float identity](../shared/concepts/price-formation-and-the-float-identity.md)
  — why the marginal trade marks the whole float; the substrate of impact.
- [Transaction costs](../shared/concepts/transaction-costs.md) — the square-root law's desk-level
  consequence.

## Open questions

- Which slices of the institutional present-state map are recoverable at retail cost — KRX
  investor-type flows (already free), US options OI/gamma maps, ETF flows, short interest — and
  what fraction of the flow-visibility edge do they recover per won spent?
  *(Answered 2026-07-06 — the [present-state stack](present-state-stack.md): ten tools with
  build order, costs, and the unbuyable remainder named.)*
- ~~A verification lint over the hedged figures~~ *(done 2026-07-05 — live web pass: all
  load-bearing figures confirmed; two sharpened: school-ties → up to 8.4%/yr, index effect →
  7.4%→0.8%. Remaining unchecked magnitudes listed at the end of the sources section.)*
- Where exactly is the legal boundary on constraint-anticipation (rebalance front-running,
  expiry positioning) across US vs. KRX regimes?
