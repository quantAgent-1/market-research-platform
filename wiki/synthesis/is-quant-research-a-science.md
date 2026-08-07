---
type: thesis
title: "Is Quant Research a Science? — How Strategies Are Actually Found, and Why the Published Playbook Doesn't Pay"
description: The epistemics of strategy discovery, derived rather than asserted — alpha equals search cost (Grossman-Stiglitz), you cannot afford the evidence to justify your own backtest (t = SR·√T), and breadth not insight sets your ceiling (IR = IC·√BR). With the canonical factor playbook re-measured from Ken French data through May 2026: every published factor decayed 48-106% after its own publication, and not one clears t = 2 in its post-publication sample.
tags: [systematic-trading, ml-stats, methodology, synthesis, alpha, evidence, epistemics]
timestamp: 2026-07-20T06:00:00Z
status: active
sources: [../sources/deep-research-quant-discovery-validation-2026-07-20.md]
---

# Is Quant Research a Science?

**The question that produced this page** (2026-07-19): *"Is building a quant model and a profitable
strategy a scientific process of experiments — do you literally have to come up with your own ideas
and backtest them? Or is it an obvious playbook with simple risk appetite and stock choice?"*

The question offers two options. Both describe something real, and neither is where the money is.
The published playbook exists — value, momentum, carry, trend, quality, low-beta have been in the
open literature for thirty years. Original hypothesis-driven research exists too, and is what good
firms do all day. But the binding constraint in this field is neither idea generation nor risk
appetite.

**It is statistical power.** You cannot afford the evidence that would justify believing your own
strategy. Almost everything about how this industry is organized — pods, alpha factories, market
makers, the obsession with breadth — is downstream of that single fact. This page derives that
claim, measures it, and then says what survives it.

---

## 1. Three layers of derivation

### Layer one: the identity

Sharpe's *Arithmetic of Active Management* (1991) states that before costs, the return on the
average actively managed dollar equals the return on the average passively managed dollar; after
costs, it must be less. Sharpe was emphatic that this "depends only on the laws of addition,
subtraction, multiplication and division. Nothing else is required." It is an accounting identity,
not an empirical finding — it holds in every possible universe. The consequence is that **your
trading alpha is, by construction, someone else's negative alpha plus the frictions you both paid.**

The honest qualifier, which most people who invoke this arithmetic skip: Lasse Pedersen's
*Sharpening the Arithmetic of Active Management* (Financial Analysts Journal, 2018) shows the
identity is weaker than the slogan. The market portfolio is not static — indices reconstitute,
companies IPO, issue, buy back, and delist — so *somebody* must trade to keep passive portfolios
passive. Active management in aggregate is therefore not strictly doomed to underperform by its
full cost; a necessary volume of trading is doing real work. The identity constrains the game; it
does not close it.

### Layer two: the equilibrium

Grossman and Stiglitz (1980) resolved a paradox: if prices already reflected all information,
nobody would pay to gather information — so nobody would, so prices could not reflect it. The
equilibrium is that **markets stay inefficient by exactly enough to repay the cost of the search
that corrects them.** Alpha is not a free good lying around. It is priced, and its price is the
search.

Berk and Green (2002, *Mutual Fund Flows and Performance in Rational Markets*, NBER WP 9275) supply
the capital-flows version: skill can be entirely real while net-of-fee alpha to outside investors
is competed to zero, because money flows to skill until diminishing returns to scale exhaust it.
Fund size adjusts until the marginal investor earns nothing. Their empirical companion — Berk and
van Binsbergen, *Measuring Managerial Skill in the Mutual Fund Industry* (NBER WP 18184) — finds
exactly this: real value added by managers, not captured by the people who bought the fund.

Put those together and you get the actionable corollary, which is stronger than the theory sounds.
If the return to a search equals its cost, then your edge must come from **a search that is cheap
for you and expensive for everyone else.** That is a barrier, and there are roughly five:

- **Capital scale** — a niche too small to be worth an institution's attention.
- **Mandate** — they are not permitted to hold it.
- **Infrastructure** — they outspend you; you lose this one.
- **Access** — timezone, language, relationships, a data source you sit next to.
- **Patience** — they have redemption risk on a quarterly clock; you do not.

"Come up with your own ideas" is the wrong instruction. **"Find the arena where you hold a
structural asymmetry" is the right one.** Note that this desk's own [alpha map](alpha-map.md)
independently landed on the only two barriers it actually possesses — small size and Asia-session
flow access — which is a good sign the derivation is load-bearing rather than decorative.

### Layer three: the measurement

The t-statistic on a strategy's mean return is

```
t  ≈  SR · √T          (SR = annualized Sharpe, T = years)
```

which follows immediately: the standard error of an annual return estimate is σ/√T, and Sharpe is
μ/σ, so t = (μ/σ)·√T. Inverting for the years needed to clear t = 2 gives **T = (2/SR)²**.

Multiple testing then makes it much worse. If you tried N candidate strategies and kept the best,
the winner's Sharpe is drawn from the maximum of N draws, and the expected maximum of N standard
normals grows like √(2 ln N). So the years required become approximately

```
T  ≈  2·ln(N) / SR²
```

| True Sharpe | Years for t=2, one honest test | If you tried 100 ideas | If you tried 1,000 |
|---|---|---|---|
| 0.3 | 44 | 102 | 154 |
| 0.5 | 16 | 37 | 55 |
| 1.0 | 4 | 9 | 14 |
| 2.0 | 1 | 2.3 | 3.5 |

Read the top-left of that table, because that is where retail and most discretionary trading live.
A genuine Sharpe-0.5 strategy — better than most published factors — found after trying 100
variants needs **37 years of data** before the numbers alone separate it from luck. Nobody has
that. Not you, not Citadel. **The data does not exist.**

This is the fact that reframes everything below: the industry does not run on statistically
validated backtests, because those are unaffordable. It runs on ways of importing evidence from
outside the return series.

---

## 2. The playbook, re-measured

The "obvious playbook" hypothesis is testable, so this page tests it rather than citing anyone.
Using Kenneth French's own monthly factor data (file built from the 202605 CRSP database; sample
1963-07 through 2026-05, 755 monthly observations), each canonical factor was split at **its own
publication date** — the McLean-Pontiff design, run on primary data and extended to 2026.

| Factor | Published | Sharpe before | Sharpe after | Decay | t-stat after |
|---|---|---|---|---|---|
| SMB (size) | Fama-French 1992/93 | 0.36 | 0.07 | 80% | 0.43 |
| HML (value) | Fama-French 1992/93 | 0.58 | 0.19 | 67% | 1.09 |
| Mom (momentum) | Jegadeesh-Titman 1993 | 0.83 | 0.32 | 62% | 1.83 |
| CMA (investment) | Titman-Wei-Xie 2004 | 0.63 | −0.04 | 106% | −0.17 |
| RMW (profitability) | Novy-Marx 2013 | 0.42 | 0.22 | 48% | 0.81 |

Three findings, none of which required trusting a secondary source.

**First, the decay is universal and averages about 73%** across the five — worse than the ~58%
McLean and Pontiff measured in the published version of their study, which is what you would expect
if crowding continued in the decade after they wrote. Every single factor decayed. The one that
decayed least (RMW, 48%) is also the one with the least post-publication time to decay in.

**Second — and this is the sharpest result on the page — not one canonical factor clears t = 2 in
its own post-publication sample.** Momentum comes closest at 1.83. Value sits at 1.09. The
investment factor is negative. These are the most-studied, most-replicated, most-published effects
in all of empirical finance, and evaluated honestly on the data that arrived *after* they became
public knowledge, they are statistically indistinguishable from nothing.

**Third, the thing that needed no research at all won.** Over the last twenty years (2006–2025) the
market factor delivered Sharpe 0.65; over the last ten, 0.82. An equal-weight combination of all
five long-short factors delivered **0.15** over the last twenty years — 0.69% a year on 4.5%
volatility. Four of the five long-short factors were flat-to-negative. Buying and holding the index
beat the entire published playbook, decisively, for two decades.

And the playbook's drawdowns are not survivable by the people who would need to hold it. Value's
worst three-year stretch after publication was **−45.4%**; its maximum drawdown on the compounded
spread, **−57.8%**. Momentum's, likewise −57.8%. The reason the published playbook still "works"
for the handful who harvest it is not informational — it is that **holding it through that is the
actual barrier.** Patience is the payer's barrier, which is precisely the Grossman-Stiglitz result
wearing different clothes.

*Honest limits on these numbers.* These are academic long-short factor portfolios: gross of
transaction costs, financing, shorting fees, and taxes, so live implementations are worse, not
better. Publication dates are judgment calls — CMA in particular is sensitive to whether you date
the investment factor to Titman-Wei-Xie (2004) or to Fama-French's 2015 five-factor canonization,
and RMW's post-period is only ~13 years, so its low t-stat partly reflects a short sample rather
than pure decay. The drawdowns are on a dollar-neutral spread, not on an investable fund. None of
these caveats move the direction of the result.

---

## 3. What the replication literature says

The primary papers, read directly rather than summarized:

**Hou, Xue and Zhang, *Replicating Anomalies* (Review of Financial Studies, 2020).** With microcaps
handled properly (NYSE breakpoints, value-weighted returns), **65% of 452 anomalies fail to clear
even t ≥ 1.96** — and 96% of the trading-frictions category fails. At the multiple-testing hurdle of
t ≥ 2.78, the failure rate rises to **82%**. Their conclusion: "capital markets are more efficient
than previously recognized." The prior version of this claim on the wiki said "300+ factors";
452 and the 65%/82% split are the verified figures.

**Harvey, Liu and Zhu, *… and the Cross-Section of Expected Returns* (NBER WP 20592, 2014).** The
multiple-testing argument that made t ≥ 3 the recommended hurdle for a new factor, on the grounds
that hundreds of factors have been tested and only the winners get published.

**Feng, Giglio and Xiu, *Taming the Factor Zoo* (Journal of Finance, 2020).** Evaluating new factors
against the hundreds already proposed: most are redundant; a few retain significant explanatory
power. The zoo is mostly re-labelling.

**McLean and Pontiff, *Does Academic Research Destroy Stock Return Predictability?*** ⚠️ A vintage
trap worth recording: the working-paper version (May 2013) reports **82 characteristics, ~10%
out-of-sample decay (not statistically distinguishable from zero) and ~35% post-publication decay**.
The published Journal of Finance version (2016) reports **97 characteristics, 26% and 58%**. Cite
the published figures; the 58% number already on the wiki is correct, but the two vintages circulate
interchangeably and disagree by a factor of nearly two.

---

## 4. Why breadth, not insight, sets the ceiling

Grinold's fundamental law of active management:

```
IR  =  IC · √BR
```

IC is the *information coefficient*, the correlation between your forecast and the outcome. BR is
*breadth*, the number of genuinely independent bets per year. The intuition is that signal
accumulates linearly across independent bets while noise accumulates as the square root, so the
ratio grows as √N.

A genuinely good signal has IC of roughly 0.03 to 0.05 — you are right about 51.5% of the time.
Solve for what that requires:

- IC = 0.03 needs **1,111 independent bets a year** for an information ratio of 1.0, and **4,444**
  for 2.0.
- A concentrated book of 20 positions rebalanced monthly gives 240 nominal bets — and far fewer
  real ones, since same-sector positions are not independent. That is IR ≈ 0.03 × √240 ≈ **0.47**.
- Apply the transfer coefficient (Clarke, de Silva and Thorley's refinement: IR = TC · IC · √BR,
  where TC is the haircut from costs, constraints and imperfect implementation, typically 0.3–0.8)
  and you land at **0.15–0.35**.

So a brilliant analyst running a concentrated book cannot produce a high Sharpe from a
normal-quality signal. Not because they are not smart — **the arithmetic forbids it.** This is why
every high-Sharpe firm in existence is a breadth machine: market makers doing millions of trades a
day, stat-arb across thousands of names, alpha factories combining thousands of weak signals. It is
also why this desk's own sleeve pre-registered a ceiling of Sharpe 0.3–0.6: that is the arithmetic
being obeyed, not pessimism.

The critical caveat, routinely mangled in practitioner folklore: **breadth is not the number of
positions.** It is the number of independent bets. Two hundred stocks driven by one macro view is
breadth ≈ 1. Correlation collapses breadth faster than anything else you can do.

---

## 5. So — is it a science?

Yes, but the analogy people reach for is wrong. It is not physics. **It is high-throughput drug
screening.**

Both run enormous candidate libraries through a brutal phase-gated attrition funnel; both have hit
rates in the fractions of a percent; both suffer publication bias and a replication crisis; and in
both, the decisive test is always out-of-sample — the clinical trial, the live track record. The
research is genuinely experimental, but it is *industrial* experimentation, not inspiration. The
honest answer to "do you literally have to come up with your own ideas" is: **you have to come up
with hundreds, and expect nearly all of them to die.**

Where finance is harder than any natural science:

| | Physics / biology | Quant finance |
|---|---|---|
| Repeat the experiment | Yes, arbitrarily | **No — one history, run once** |
| Effect size vs noise | Often large | **IC ~0.03; signal is ~1% of variance** |
| Stationarity | Laws hold | **The process drifts and regime-shifts** |
| Observer effect | Negligible | **Acting on the finding destroys it** |
| Other researchers | Collaborators | **Adversaries competing your edge away** |
| Sample already mined | No | **Yes — globally, by everyone, before you** |

The last two rows have no analogue in the natural sciences. A drug does not become less effective
because a paper was published about it. A factor does — the table in §2 is that effect, measured.

---

## 6. What replaces statistical power

Since you cannot buy power with time, you buy it three other ways. This is what "the scientific
process" actually looks like in practice here.

**Mechanism.** A causal story constrains the hypothesis space *before* you touch the data, which is
the only real defence against multiple testing. This is why the [who-pays-you](../shared/concepts/who-pays-you.md)
test — name the payer, name the barrier, count N — is doing statistical work rather than philosophy.
A prior that rules out 99% of the hypothesis space is worth more than any amount of cross-validation
applied afterwards.

**Replication across independent samples.** If an effect holds in 20 countries, 5 asset classes and
3 eras, you have twenty-odd tests of one hypothesis instead of one test. This is the AQR/Ilmanen
standard, and it is the strongest available substitute for the decades of data you do not have.

**Breadth.** More independent bets per year makes the t-statistic clock run faster. A signal firing
10,000 times a year gets its verdict in a year; one firing 20 times a year never gets one. Breadth
buys returns *and* buys knowledge — this is the under-appreciated half of the fundamental law.

**Forward tracking.** The only genuinely uncontaminated sample is the one that has not happened yet.
Pre-registration, kill criteria and graded forward verdicts are worth more than any refinement of a
backtest, because the global price history is already in-sample *for the profession* even when it is
out-of-sample for you. This is the desk's existing comparative advantage and the reason it is worth
keeping.

The deeper argument for being systematic sits here, and it is not the usual one. Rules do not beat
judgment because rules are smarter. **Rules are the only way to ever find out whether you have an
edge.** A discretionary book is not wrong — it is epistemically closed. You will never know.

---

## 7. The counter-case, taken seriously

A page that stopped at §6 would be nihilism, and the evidence does not support nihilism.

**Skill exists and persists — bootstrapped.** Kosowski, Timmermann, Wermers and White, *Can Mutual
Fund "Stars" Really Pick Stocks?* (Journal of Finance, 2006) apply a bootstrap precisely because the
cross-section of alphas is non-normal, and find "a sizable minority of managers pick stocks well
enough to more than cover their costs. Moreover, the superior alphas of these managers persist."

**Skill is detectable by better instruments.** Cohen, Coval and Pastor, *Judging Fund Managers by
the Company They Keep*, evaluate a manager by how much their holdings resemble those of managers
with strong records — and find strong predictability of future returns that standard measures miss.
Alpha is hard to see with a t-test on returns; it is not invisible.

**The tests themselves lack power — which cuts both ways.** Harvey and Liu, *False (and Missed)
Discoveries in Financial Economics* (Journal of Finance, 2020) calibrate Type I *and* Type II
errors, and conclude that current methods "lack power to detect outperforming managers." The same
arithmetic that says you cannot prove your strategy works also says the profession is
systematically **missing real skill**. Absence of a t-stat is not evidence of absence of edge. This
is the single most important qualifier on everything above.

**Value added is real; capture is the problem.** Berk and van Binsbergen measure genuine managerial
skill that the fund's investors do not receive — exactly the Berk-Green mechanism. Skill is not the
scarce thing. *Keeping the proceeds of skill* is the scarce thing, and that is a bargaining
question about barriers and capacity, not a research question.

---

## 8. What actually decides outcomes, ranked

Honest ranking, with the counterintuitive punchline at the bottom:

1. **Arena and payer selection** — does a payer exist at your horizon and size at all?
2. **Breadth** — how many independent bets the arena affords, which caps your Sharpe *and* your
   rate of learning.
3. **Cost structure** — the wall that kills most retail edges before they start (this desk's own
   ~15bp KRX sell-side tax makes weekly-rebalance books dead on arrival).
4. **Survival and sizing** — converts an edge into compounding and prevents absorbing states;
   cannot manufacture return from a zero-edge signal. Over-betting past f\* provably *lowers* growth
   while raising risk, so risk management is a multiplier in [0,1], never a source.
5. **Signal cleverness** — last.

Which answers the original question directly: **your ideas are the least important input; your
arena is the most important.** And the questioner's alternative hypothesis — "simple risk appetite
and stock choice" — is half-right in an instructive way. Sizing genuinely dominates outcomes for
most participants, because most participants' signal is approximately zero and their sizing is
ruinous. But it dominates as a multiplier on an edge you must already possess.

---

## 9. Epistemic tiering

Because the question asked specifically for what is verifiable from first principles:

**Provable — identities and theorems, true by construction.** Sharpe's arithmetic (an accounting
identity, with Pedersen's qualifier). t = SR·√T and the multiple-testing hurdle T ≈ 2 ln(N)/SR².
IR = IC·√BR, given its independence assumptions. Kelly's growth-optimality and the result that
leverage beyond f\* reduces growth. Grossman-Stiglitz equilibrium (a theorem *within its model*).

**Robust empirics — measured, replicated, directionally reliable.** Post-publication factor decay
(measured here at 48–106% on the canonical five, ~58% in McLean-Pontiff's published sample).
Hou-Xue-Zhang's 65%/82% failure rates. The market outperforming the factor playbook over the last
two decades. Persistent skill in a minority of managers (KTWW).

**Contested — live disagreements, do not treat as settled.** The magnitude of the replication
crisis (Hou-Xue-Zhang's pessimism versus Chen-Zimmermann's much higher replication rates versus
Jensen-Kelly-Pedersen's hierarchical-Bayes rehabilitation — all three camps are serious). Whether
machine learning adds durable alpha net of costs. Whether factor decay reflects crowding, publication
bias, or regime change.

**Folklore — repeated, weakly grounded.** "Halve your backtest Sharpe" (a reasonable prior, no
rigorous basis). "Markets are efficient" as an unqualified statement. "You need a PhD." "Retail
cannot compete" — the honest version is that retail cannot compete *at institutional horizons and
sizes*, which is a statement about arenas, not people.

---

## 10. Honest limits of this page

The §2 computation is mine, from primary data, and is the strongest thing here — but publication
dates are judgment calls and the portfolios are gross of all costs. The §3 papers were read directly
from source PDFs. Everything about elite-firm practice (Medallion's record, pod-shop mechanics,
alpha-factory scale) was deliberately **not** included: the research agents tasked with verifying
those numbers died on a session rate limit before reporting, and this page does not carry unverified
firm-level figures. The [industrialization of edge](industrialization-of-edge.md) page already holds
the receipts-backed version of that material. Chen-Zimmermann and Jensen-Kelly-Pedersen are cited
from training knowledge as counterweights and were **not** verified in this session — treat their
specific numbers as pending. ⚠️ **Superseded 2026-07-20:** both were verified, and the elite-firm
material was recovered, by the independent pass in §11. Read §10 as the state of the page on 2026-07-19
and §11 as the correction.

---

## 11. Independent verification pass (added 2026-07-20)

A second deep-research run was launched on the *same question* with none of this page's conclusions in
its arguments — a deliberately uncontaminated second opinion, so that disagreement between the two
passes would be the deliverable. It read 24 primary sources and adversarially adjudicated 18 claims.
Provenance, method, and the run's own damage report:
[recovered run wf_1fe1d6d7-52a](../sources/deep-research-quant-discovery-validation-2026-07-20.md).

**The §10 pending items are now resolved, and they resolve in favour of the counterweights.**
Chen-Zimmermann verified: **98% of 161** clearly-significant published predictors reproduce at t > 1.96
when re-coded from scratch. Jensen-Kelly-Pedersen verified: **82.4%** replicate under hierarchical
Bayes with a 2.8% posterior standard error, and the identical 82.4% holds out-of-sample across 93
countries. Both figures are now confirmed against the source PDFs rather than carried from training
knowledge. Add Chen's separate result that Harvey-Liu-Zhu's t > 3.0 hurdle is **not empirically
identified** — the data support hurdles anywhere from 0 to 3.0 — and the §3 presentation of t > 3 as
*the* multiple-testing answer is too confident.

**Sharpened after re-verification (see §12): the entire dispute reduces to a choice of error rate.**
Harvey-Liu-Zhu's famous 3.0 comes from setting the false-discovery rate at **1%**. At the conventional
**5%**, their own model on their own preferred row returns **2.27** — barely above the 1.96 they set out
to discredit. Chen's bootstrap says that at either level the uncertainty swamps the point estimate
(0–3.0 at FDR 5%, 0–3.5 at FDR 1%). So **t > 3.0 is not a measured constant; it is what you get after
electing a stricter-than-conventional error rate**, and Harvey-Liu-Zhu then argue it is a *floor*
because the file drawer is uncounted — which is precisely the extrapolation Chen shows destroys
identification. They even hedge it themselves: *"Should a t-statistic of 3.0 be used for every factor
proposed in the future? Probably not."* The honest filing is that **the hurdle depends on the error rate
you choose and on an unobservable file drawer.**

**The open question at the bottom of this page is largely dissolved, by one sentence.** That question
asked which side of the Hou-Xue-Zhang versus Chen-Zimmermann methodological dispute is right, and
called it the highest-value unresolved question for a practitioner. Chen and Zimmermann answer it
themselves, immediately after showing predictability survives publication: *"these results do not
account for trading costs. Indeed, Chen and Velikov (2019) find that the remaining predictability is
eliminated by effective bid-ask spreads."* The optimists and pessimists are arguing about whether
published anomalies are **statistically real**. Neither claims they are **tradeable**. The dispute is
therefore mostly irrelevant to anyone who has to pay a spread — which reinforces this page's
conclusion by a cleaner route than §2 took, and means the §2 result and the 82–98% replication rates
are not in conflict: they measure different things, one post-publication net-of-nothing on five
factors, the other in-sample statistical existence across hundreds.

The decay direction corroborates: Jensen-Kelly-Pedersen measure 47% (0.49% → 0.26% monthly alpha),
McLean-Pontiff's published 58%, against the 73% measured in §2 here. §2 running higher is what
continued crowding through 2026 predicts, so the three are consistent in direction and ordering.

**One §9 row is a candidate to move — but not yet.** "Halve your backtest Sharpe" sits under *Folklore —
repeated, weakly grounded*. Harvey and Liu appear to give it a rigorous basis while showing it is **wrong
in a specific direction**: the correct multiple-testing haircut is strongly nonlinear — more than 50%
below annualized Sharpe 0.4, and at most 25% above Sharpe 1.0, so marginal strategies are
under-penalized by the rule of thumb and strong ones over-penalized. **Holding it in Folklore for now:
that claim comes from one of the seventeen sources this run never adversarially adjudicated** (see §12),
and given that every refutation in this run killed an over-generalizing final sentence, an unattacked
claim is not yet grounds for promoting a tier. Verify it, then move it.

**§1's power arithmetic gains sharper theorems.** Bailey and López de Prado's Minimum Backtest Length
inverts the T ≈ 2·ln(N)/SR² relation into the form that actually binds a researcher: **five years of
data supports at most 45 independent configurations; two years supports seven.** Re-verification
confirmed these are *exact integer boundaries*, not round numbers (N=45 → 4.998 years, N=46 → 5.036).
Lo's Sharpe standard error, sqrt((1 + SR²/2)/T), adds a genuinely counterintuitive fact this page
lacked: **at fixed T the standard error rises with the true Sharpe**, so high-Sharpe strategies are
*harder* to validate, not easier. And the §6 reliance on out-of-sample testing needs a caveat — holdout
applied ~20 times at 95% confidence makes a false positive *expected*.

⚠️ **Two corrections to how this result is usually quoted, both established in §12.** First, the famous
"ten trials manufactures a Sharpe of 1.57 from nothing" is **a one-year number**. E[max_N] is a
dimensionless order statistic that equals an annualized Sharpe only at y = 1; scaled properly, ten
trials gives **1.575 at one year, 1.113 at two, 0.704 at five, 0.498 at ten.** Applying 1.57 to a normal
five-year backtest overstates the null threshold by **2.24×** — a mistake that makes honest strategies
look like noise. Second, "overfitting is actively destructive under memory" is **half theorem, half
simulation**: what the propositions *prove* is that optimizing in-sample **reverses the ordering** out
of sample; the stronger claim of outright negative expected returns is a Monte Carlo finding. Both
statements are true; only one is a theorem.

**§4's breadth argument now has primary-source receipts, including the ones §10 said were missing.**
Renaissance, under oath to the Senate: Medallion's model "makes predictions that are profitable only
slightly more often than not," with returns coming from "the mathematical principle known as the law
of large numbers" — at more than 100,000 trades a day. WorldQuant's published study of 4,002 real
production alphas: median standalone annualized Sharpe **1.487**, combined into a single "mega-alpha."
That is IR = IC·√BR with the IC and the N both visible.

**§8's rank-4 claim survives but must be stated more carefully.** "Risk management is a multiplier in
[0,1], never a source" faces a serious peer-reviewed challenge: Moreira-Muir (JF 2017) find a pure
inverse-variance sizing rule with *no return forecast* earns 4.86% annualized alpha on the market.
The resolution is not to dismiss it. Cederburg et al. (JFE 2020) show only 53 of 103 strategies improve
(p = 0.84 — and *fewer* than the 66 expected under the null, bootstrap p = 0.01), with real-time
implementable versions losing to the unmanaged portfolio in 72 of 103 cases; Man Group's own
researchers, arguing against commercial interest, show the effect is confined to assets with a
leverage effect and that "momentumness" explains 45–60% of the variation in Sharpe improvement.
**Vol-targeting's apparent alpha is a time-series momentum bet in disguise — a smuggled edge, not a
free one — and it does not survive real-time implementation.** The multiplier claim holds; the honest
version now names the challenge and answers it.

**§7's counter-case gets much stronger evidence than the mutual-fund studies.** CFTC audit-trail data
on 85 HFT firms: median firm Sharpe **4.30**, four-factor alpha 22.02%, return persistence of 0.421
daily and 0.723 monthly — and the edge was *not* competed away, with new entrants less profitable,
exiting faster, and the profit Herfindahl rising from 0.287 to 0.545. Meanwhile the mutual-fund nulls
are substantially a power failure: the Fama-French bootstrap misses skilled managers **85% of the time
when they exist by construction**. §7's "absence of a t-stat is not evidence of absence of edge" was
the right call and is now quantified.

**One thing this page did not anticipate, and should have.** The SEC's 2025 Two Sigma order documents
a researcher altering fourteen live models over 21 months undetected, and vulnerabilities identified
in March 2019 sitting unremediated until October 2023 (August 2023 was when the tampering was
detected; date corrected against the order in the 2026-07-20 third pass). The useful part is the mechanism: he drove
*decorrelation parameters* toward zero so his models mimicked the existing book while appearing to add
unique alpha, and was paid accordingly. Institutional validation optimizes **marginal alpha net of
correlation to the existing book** — not standalone backtest quality. That is a sixth item for §8's
ranking at the institutional level, and it is invisible from the outside.

*Limits of this pass.* Seven of the 25 claims sent for verification lost all three voters to the same
usage limit that killed the run's synthesis. **That hole has since been closed — see §12.** The four
"refuted" claims were refuted on their glosses, not their numbers. Details in the
[run brief](../sources/deep-research-quant-discovery-validation-2026-07-20.md).

---

## 12. Closing the verification hole (added 2026-07-20)

The seven claims orphaned by the usage limit were re-adjudicated by nine fresh independent skeptics,
three per source, checked against the *original cached PDFs* rather than re-fetched copies. Because
these are theorems, the voters were told to **rederive** rather than quote-match. **Six survived, one
was killed.** Full detail in the run brief.

**What survived, and is now safe to lean on.** Minimum Backtest Length reproduces exactly — 45 and 7 are
the precise integer boundaries. The Harvey-Liu-Zhu material passed 3-0, including a version check
confirming the 2014 working paper and the published RFS 2016 agree word-for-word — **no vintage trap
here**, unlike the McLean-Pontiff case §3 flags. One voter also settled a question the paper leaves
implicit: MinBTL-in-years is **frequency-free under the null**, since the q term in the Sharpe variance
vanishes at SR = 0; frequency re-enters only through finite-sample tails, where the bound runs ~4%
**anti-conservative** on short monthly backtests — against the user precisely where overfitting is most
tempting.

**What was killed** was a claim's appended sentence asserting Chen's identification failure is "a general
constraint on **any** multiple-testing correction." It is not — Chen's actual contribution is that the
constraint is *selective*, which is why he directs the field toward the strongly-identified statistics.

**The lesson worth keeping, independent of this page's subject.** Across both verification passes,
**every refutation — eight for eight — killed the final sentence of a claim while its numbers and quotes
verified.** The pattern is a universal quantifier, an epistemic upgrade, or an exactness claim bolted
onto accurate content. On three claims the voters were *unanimous about which sentence was defective
while splitting on whether it was fatal*, which means the binary refuted/not-refuted tally carries less
information than the named sentence. **When reading any machine-extracted claim, including the ones on
this page: trust the quotes, audit the last clause.**

**A methodological trap worth recording.** The formula for the expected maximum Sharpe extracts from the
PDF text layer as `1 − 1/(Ne⁻¹)`, which evaluates to 0.89 at N=10 and looks like a clean refutation. The
correct reading is `1 − 1/(Ne)`, confirmed by glyph coordinates, by the authors' own published Python,
and by the fact that only that parse reproduces their stated 1.57. A verifier trusting the text layer
would have produced a confident false refutation — and the same class of error is available to anyone
extracting equations from PDFs at scale.

**The caveat this exercise exposed, which matters more than any single claim.** All 25 adjudicated
claims came from just **seven sources, all in the replication-statistics cluster**. **Seventeen sources
were never attacked at all** — and they carry most of what §11 added: the Renaissance testimony,
WorldQuant, the CFTC HFT figures, Two Sigma, Thorp, the whole vol-targeting dispute, Lo's standard
error, the day-trader censuses, the Fama-French power result, and the Sharpe-haircut rule. Those are
verbatim quotes from named primary documents, but unadjudicated. Given the eight-for-eight pattern
above, treat their **quotes as probably sound and their concluding glosses as unverified.**

---

## Relationships

- **The evidence half of this page:**
  [How Systematic Strategies Are Actually Discovered and Validated](how-strategies-are-discovered-and-validated.md)
  — the same question answered from 24 primary sources by an uncontaminated run, covering the documented
  firm-level practice this page deliberately excluded (Renaissance under oath, WorldQuant's 4,002 alphas,
  the Two Sigma decorrelation criterion), the sizing-versus-edge adjudication, and where skill is
  measurably persistent. Read together: this page derives what the arithmetic forbids, that one reports
  what the record shows.
- The validation machinery this page's argument demands:
  [backtesting rigor & overfitting](../ml-stats/concepts/backtesting-overfitting.md) (which this page
  corrects: 452 anomalies, not "300+") and
  [performance metrics](../ml-stats/concepts/performance-metrics.md) (the Deflated Sharpe gate).
- The payer taxonomy whose statistical function §6 explains:
  [who pays you](../shared/concepts/who-pays-you.md).
- The decay evidence this page re-measures:
  [factor premia & alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md).
- Why edges persist at all despite §1: [limits to arbitrage](../shared/concepts/limits-to-arbitrage.md).
- The three-factor product this page's §8 ranking refines:
  [trading-system fundamentals](trading-system-fundamentals.md).
- The mechanism-level catalogue of edges: [techniques of winning trades](techniques-of-winning-trades.md);
  the firm-scale version: [the industrialization of edge](industrialization-of-edge.md).
- Where this desk's barriers actually are: [the alpha map](alpha-map.md) and
  the alpha benchmark.

## Open questions

- Does the §2 decay result survive cost-adjustment, and does the ranking of factors change once
  realistic shorting and financing costs are imposed?
- ~~Chen-Zimmermann report far higher replication rates than Hou-Xue-Zhang on overlapping data. The
  disagreement is methodological (breakpoints, weighting, t-hurdles). Which set of choices is right
  is the single highest-value unresolved question in this literature for a practitioner.~~
  **Largely dissolved 2026-07-20 (§11):** the dispute is about statistical existence, and both camps
  concede the surviving predictability is eliminated by effective bid-ask spreads. The practitioner
  question is not which camp is right but that neither claims tradeability. What remains open, and is
  now the sharper question: *which* anomalies survive costs at what capacity — the Chen-Velikov
  net-of-cost frontier, which this desk has not read directly.
- Can the "years to t=2" arithmetic be turned into a standing pre-trade gate — a signal is only
  worth building if its expected breadth delivers a verdict inside a decision-relevant horizon?
