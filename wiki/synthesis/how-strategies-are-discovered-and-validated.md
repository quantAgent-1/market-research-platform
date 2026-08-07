---
type: overview
title: "How Systematic Strategies Are Actually Discovered and Validated — The Evidence"
description: The report from the uncontaminated deep-research run — 24 primary sources on whether the published playbook still pays, what the mathematics forbids, how quant firms really run research, whether sizing can substitute for edge, and where trading skill is demonstrably real. With the evidence graded by what actually survived adversarial verification.
tags: [systematic-trading, ml-stats, methodology, epistemics, replication, evidence]
timestamp: 2026-07-20T00:00:00Z
status: active
sources: [../sources/deep-research-quant-discovery-validation-2026-07-20.md]
---

# How Systematic Strategies Are Actually Discovered and Validated

**This is the evidence half.** Its sibling, [Is Quant Research a Science?](is-quant-research-a-science.md),
derives what the arithmetic *forbids* — from Sharpe's identity, Grossman-Stiglitz, IR = IC·√BR, and a
re-measurement of the canonical factors on Ken French's data. This page asks the empirical question
instead: **what does the documentary record actually show about how strategies get found and checked?**
It comes from a deliberately uncontaminated research run that carried none of that page's conclusions,
so where the two agree, they agree independently. Provenance and method:
[the run brief](../sources/deep-research-quant-discovery-validation-2026-07-20.md).

**Read the confidence tiers in §7 before quoting anything here.** They were unusually lopsided when
first written; the missing pass has since been run (2026-07-20) and the tiers updated in place.

---

## The question, and the short answer

The question was whether building a profitable systematic strategy is a scientific process of
hypothesis and experiment — where you must generate your own ideas and test them — or whether it is a
well-known playbook where what really matters is risk appetite and stock selection.

**Both descriptions are real, and neither is where the money is.** The published playbook exists and is
statistically genuine; it is also economically dead once you pay the spread. Original hypothesis-driven
research exists and is what good firms do all day; it is also industrialized to a degree that makes
"come up with an idea" a misleading description of it. And risk appetite genuinely dominates outcomes
for most participants — but as a multiplier on an edge you must already have, never as a substitute.

The thing sitting underneath all five sub-questions is that **you cannot afford the evidence that would
justify believing your own strategy.** Everything else — the breadth obsession, the alpha factories, the
decorrelation criteria, the fractional-Kelly conservatism — is downstream of that.

---

## 1. Does the published playbook still pay?

This is the loudest fight in empirical asset pricing, and the run captured all sides of it.

**The pessimists.** Hou, Xue and Zhang re-tested 452 published anomalies over 1967–2016. Once you stop
overweighting tiny stocks — using NYSE size breakpoints and value-weighted returns — **65% fail to clear
even a single-test t ≥ 1.96**, and at a multiple-testing hurdle of 2.78 the failure rate reaches 82%.
Their diagnosis is not decay but *original error*: microcaps are 60.7% of listed companies and 3.2% of
market value, and the original studies leaned on them. Survival varies sharply by family — investment
73.7%, momentum 63.2%, profitability 44.3%, value 42%, intangibles 25.2%, and trading frictions roughly
4%, where 102 of 106 anomalies fail. Crucially, re-running on each study's *own* original sample gives a
65.3% failure rate — "quantitatively similar," in the paper's own words (no formal test is reported). **These effects mostly didn't decay; they were
never there at the strength claimed.**

**The optimists.** Chen and Zimmermann re-coded 319 characteristics from scratch and found that **98% of
the 161 that were clearly significant in their original papers reproduce** at t > 1.96. They also
dismantle the counting: Hou-Xue-Zhang's 452 "anomalies" derive from 240 characteristics (212 are
rebalancing-frequency variants), of which only 118 ever showed clear significance to replicate — and 117
of those 118 reproduce. Jensen, Kelly and Pedersen come at it with a Bayesian hierarchical model and get
**82.4% replicating, with a tight 2.8% posterior standard error, and the identical 82.4% out-of-sample
across 93 countries.**

**The methodology is doing almost all the work.** Jensen-Kelly-Pedersen show their own sample yields
55.6% under raw-return OLS (directly comparable to HXZ's 35%), 61.3% excluding factors the original
papers themselves found insignificant, 82.4% testing CAPM alpha instead of raw returns, 75.6% under a
frequentist correction, and 82.4% under Bayesian multiple testing — while HXZ's own 35% drops to 18%
under a comparable correction. **A spread of 18% to 82.4% across defensible choices is the whole
dispute.**

**Decay is real and everyone measures it.** McLean and Pontiff's 97 predictors earn 0.582% monthly
in-sample, 0.402% out-of-sample but pre-publication, and 0.264% after publication (≈3.2%/yr gross on the
long-short). Their headline declines — 26% out-of-sample, 58% post-publication — are panel-regression
estimates (dummy coefficients −0.150 and −0.337 on the 0.582 base), not ratios of those raw means, which
would give 31% and 55%. They reject *both* the null
that predictability vanishes and the null that it doesn't decay. Jensen-Kelly-Pedersen independently
measure 47% (0.49% → 0.26% monthly alpha; their statistic is post-*original-sample*, not
post-publication). Two refinements worth holding onto: the 26% is an explicit
**upper bound** on data-mining bias, since some traders learn of a predictor pre-publication and their
trading is arbitrage rather than overfitting; and **decay is largest for the most impressive backtests**
— higher in-sample t-statistics decay more. The mean in-sample t was 3.55.

### The sentence that settles it for a practitioner

Chen and Zimmermann, immediately after demonstrating that predictability survives publication:

> *"It's important to note, however, that these results do not account for trading costs. Indeed, Chen
> and Velikov (2019) find that the remaining predictability is eliminated by effective bid-ask spreads."*

They also note that imposing value-weighting or screening out sub-20th-percentile stocks cuts in-sample
returns by about 30% — roughly 20 basis points a month — before you have paid a spread.

**So the two camps are arguing about statistical existence, and neither claims tradeability.** For
anyone who has to cross a spread, the replication war is close to moot: the published playbook is real
and it does not pay. That reconciliation is more useful than picking a side, and it is why the
sibling page's factor re-measurement and this literature's 82–98% replication rates are not in conflict
— they measure different things.

---

## 2. What the mathematics forbids

This is the part that is true by construction rather than by measurement, and it is harsher than the
folklore.

**A backtest's Sharpe ratio is not evidence until you know how many things were tried.** The expected
*maximum* Sharpe across N trials, when every strategy has exactly zero true skill, grows without bound
in N — a consequence of extreme-value theory, not a fact about markets. Bailey, Borwein, López de Prado
and Zhu give the closed form and its √(2 ln N) bound.

⚠️ **The famous number is routinely misquoted, including in the first draft of this page.** "Ten trials
manufactures a Sharpe of 1.57 from nothing" is a **one-year** figure. The quantity is a dimensionless
order statistic that equals an annualized Sharpe only when the sample is one year long. Scaled properly,
ten trials at zero skill gives:

| Backtest length | Expected best Sharpe from pure noise |
|---|---|
| 1 year | 1.575 |
| 2 years | 1.113 |
| 5 years | 0.704 |
| 10 years | 0.498 |

Applying 1.57 to a normal five-year backtest overstates the noise threshold by **2.24×** — an error that
makes genuinely good strategies look like luck. (The table prints the paper's own Gumbel approximation, which runs about
+2.3% high at N = 10 — the exact values are 1.539 / 1.088 / 0.688 / 0.487. The same overshoot is why the
paper's "above 2.6" at N = 128 is slightly wrong: the exact expectation is 2.5946.)

**Minimum Backtest Length is the same theorem stood on its head, and it is the practical form.** To keep
the expected noise-Sharpe at 1.0, **five years of data supports at most 45 independent configurations;
two years supports seven.** Those are exact integer boundaries, not round numbers. Two further points
that matter for how you'd use it: the count is *frequency-free* under the null — daily versus monthly
data doesn't change the years required — and finite-sample tails inflate the true noise maximum ~4–5% above
normal theory on short monthly samples — but that inflation nearly cancels the approximation's built-in
overshoot, so in net terms the two-year boundary (N=7, T=24) is calibrated exactly (realized E[max] =
1.000 across 400,000 simulated paths) while the five-year boundary (N=45, T=60) runs ~1.6% permissive.

**Out-of-sample testing is necessary and not sufficient.** Holdout applied roughly twenty times at 95%
confidence makes a false positive *expected*, and the survivor then gets reported as a single-trial
result. When the performance series is mean-reverting — the proposition's actual hypothesis is a
stationary first-order autoregression with equal volatilities across configurations; positive
autocorrelation alone does not do it — optimizing in-sample provably **reverses** the ordering out of
sample: better in-sample implies worse out-of-sample. (The stronger claim, that expected
out-of-sample returns go outright negative, is a simulation result rather than a theorem; both are in
the paper, only one is proved.)

**Even measuring a Sharpe ratio is harder than it looks.** Lo's standard error is √((1 + SR²/2)/T),
which has the counterintuitive consequence that **at a fixed sample size the standard error rises with
the true Sharpe** — high-Sharpe strategies are harder to validate, not easier. And annualizing a monthly
Sharpe by √12 is valid only under IID returns; ignoring serial correlation overstated annualized Sharpes
in a sample of hedge funds by as much as 65%.

**The multiple-testing hurdle is contested, and the disagreement is narrower than it sounds.**
Harvey, Liu and Zhu argue the conventional t > 2.0 is invalid given the scale of search, and recommend
t > 3.0 — arguing it is a *floor*, since their census of 316 tested factors omits the file drawer of
failed and unpublished tests. Chen answers that the hurdle is not empirically identified at all: bootstrapped
t-hurdles span 0 to 3.0.

The resolution is a choice of error rate, and it takes both of HLZ's tables to see it. Their headline
frequentist hurdles (Figure 3, BHY baseline) are **2.78 at 5% FDR — the very number Hou-Xue-Zhang
borrowed — and 3.39 at 1%**, with their stated minimum at 3.18. Their structural model with correlations
says it more sharply: at the correlation level their own objective function selects (ρ = 0.2, Table 5),
it returns **2.95 ≈ 3.0 at 1% FDR and 2.27 at the conventional 5%** — the latter barely above the 1.96
they set out to discredit. Either way t > 3.0 is not a measured constant; it is what you get after
electing an error rate, on top of an unobservable file drawer. They hedge it
themselves: *"Should a t-statistic of 3.0 be used for every factor proposed in the future? Probably
not."* **The honest statement is that the hurdle depends on the error rate you choose and on a file
drawer nobody can see.**

One more calibration from the same paper: even the factors it classifies as *true* average 6.6% a year
at 15% volatility — **a Sharpe of 0.44, with roughly 70% of them below 0.5.** That bounds what any single
published factor can contribute.

---

## 3. How quant firms actually run research

The best evidence here is adversarial or compelled — testimony, enforcement actions, disclosure — rather
than marketing.

**Renaissance, under oath to the Senate Permanent Subcommittee on Investigations, described Medallion in
terms that are almost an admission of no per-trade edge:**

> *"The model developed by Renaissance for Medallion makes predictions that are profitable only slightly
> more often than not. Moreover, the predicted price movements can be easily overwhelmed by external
> events. To compensate for these factors, the model generates a large number of recommendations, so
> that by virtue of the mathematical principle known as the law of large numbers, the variability of the
> returns produced by the model is greatly reduced."*

The record quantifies the breadth: **100,000–150,000 trades a day with each bank, a combined 26–39
million a year** (the round "100,000 a day / 30 million a year" is Senator Levin's summary of those
figures), with positions held under three months 87% of the time. This is IR = IC·√BR with both terms visible — a
near-zero information coefficient converted into a high information ratio purely by N. The same record
documents leverage of up to 20:1 through basket options versus the 2:1 Regulation T limit, and about
$34 billion of pre-tax profit across 60 options between 2000 and 2014. The research organization is
described as 200–250 people including roughly 90 science and mathematics PhDs whose standing job is
continuous revision of the model.

**WorldQuant published the only large-scale look at real production signals.** Of 4,002 production alphas drawn
from a larger proprietary population, the 3,289 with positive Sharpe and complete statistics show a
median standalone annualized Sharpe of **1.487** (first quartile 0.938, maximum 4.117) — gross of costs. The stated operating model is to mine very large
numbers of individually weak signals and combine them algorithmically into a single "mega-alpha,"
described not as ambition but as current practice. **366 of the 4,002 — 9.1% — realized negative Sharpe in live
trading** (a derived count: the paper weeds 4,002 down to 3,636, calling the excluded alphas ones that
"have not lived up to their expectations"; all its figures are real-life, "out-of-sample by definition").
These are deployed production alphas, so that is a post-validation failure rate, not a discovery hit
rate — the true funnel is far steeper — and note the median above is computed after this weeding.

**The SEC's 2025 Two Sigma order is the most useful document of the set, and not for the scandal.** A
single researcher altered fourteen live models over 21 months without detection (November 2021 until the
changes were spotted in August 2023); vulnerabilities identified internally in March 2019 went
unremediated until October 2023; the firm repaid $165 million and paid $90 million in penalties. The mechanism is the valuable part: he drove **decorrelation parameters**
toward zero so his models reproduced the forecasts of the existing model book while appearing to generate
unique alpha — collecting, in the order's words, "millions of dollars of additional compensation" from
the resulting net overperformance.

That tells you what institutional validation actually optimizes. **Not standalone backtest quality but
marginal alpha net of correlation to what the firm already runs** — measured explicitly as a model-approval gate, and flowing into
pay through the overperformance it manufactures. It
also punctures the folk image of elite quant shops as places where model governance is rigorous by
default.

Putting the three together: strategy discovery at scale is **mass search with a portfolio-level
acceptance criterion**, closer to high-throughput screening than to hypothesis-and-experiment. The
question "did you come up with your own idea" is the wrong unit of analysis; the unit is the pipeline.

---

## 4. Can sizing, leverage, or risk management substitute for edge?

**No — and the theory is unusually clean here.** Thorp's optimal fraction is a function of the edge
itself (f\* = m/ab, valid only when expectation m > 0), so a zero edge gives a zero bet. Past a critical
fraction the same favourable game becomes near-certain ruin: at a 53% win probability the optimum is 6%
of capital and ruin begins around 12%. Betting exactly at that critical fraction gives wealth that
oscillates between zero and infinity almost surely. Thorp also notes that estimated edges are
systematically biased above true edges — data mining, non-stationarity, rule changes, capital inflow —
which is the argument for fractional Kelly.

**The retail data is the empirical version of the same statement.** In a complete regulatory census of
Brazilian day traders, of 19,646 people who started, **97% of those who persisted beyond 300 days lost
money**; the single best earned $310 a day against a daily standard deviation of $2,560, an implied daily
Sharpe near 0.12. The share with positive profit *decreases* monotonically with days traded — the
signature of a negative-expectation process, not of learning. Panel regressions on 714,637 trader-days
find no learning effect at all. Taiwan's complete exchange data agrees: under 3% of day traders are
predictably profitable, gross losses of 7bp/day become 23.9bp net after costs, and — the elegant part —
day-trading returns are *negatively* skewed (−0.22) while individual Taiwanese stocks average +2.36, so
**even a pure risk-seeker would get better lottery exposure by buying one volatile stock and holding
it.** Risk appetite is a strictly dominated route to payoff skew.

**The one serious counter-argument deserves to be taken seriously, then resolved.** Moreira and Muir
showed in the *Journal of Finance* that scaling a factor by the inverse of its recent realized variance —
a pure sizing rule containing **no return forecast at all** — produces 4.86% annualized alpha on the
market portfolio and raises the buy-and-hold Sharpe by about 25%. Their mechanism is that variance is
highly forecastable at short horizons while returns are not (the strategy rebalances monthly), so you improve the trade-off without
predicting anything. If that holds, sizing really does create risk-adjusted return.

It mostly doesn't hold, for two independent reasons:

- **It is momentum in disguise.** Man Group's own researchers — arguing against their commercial
  interest, since they sell volatility-targeted products — show the benefit is confined to assets with a
  leverage effect (equities, credit) and is negligible for bonds, currencies and commodities. Because
  risk assets have a negative return-volatility relation, inverse-volatility scaling *mechanically
  implements a time-series momentum bet*, and the "momentumness" explains **45–60% of the cross-sectional
  variation in Sharpe improvement.** The edge was smuggled in, not created.
- **It does not survive real-time implementation.** Across 103 equity strategies, only 53 volatility-managed
  versions beat their unmanaged counterparts on Sharpe — indistinguishable from a coin flip (p = 0.84),
  and *fewer* than the 66 you would expect under a null of persistent volatility with no risk-return
  relation (bootstrap p = 0.01). Implementable versions using only past data **underperform simply holding
  the original portfolio in 72 of 103 cases** by certainty-equivalent return (58 of 103 by Sharpe ratio). The in-sample evidence requires ex-post optimal weights.

There is also a sharp methodological lesson buried in that last paper: the spanning-regression alpha used
to certify these strategies is algebraically a **weaker** test than actual performance improvement. Given
the correlations involved, a strategy can post a significantly positive alpha while delivering a 30%-or-worse
*drop* in Sharpe ratio. Passing the standard academic significance test is not the same as being a better
investment.

**Where risk management does earn its keep** is distributional. Volatility targeting reliably reduces the
probability of extreme returns and the volatility of volatility, and cuts maximum drawdowns — which is
genuinely valuable under concave utility. It cuts *both* tails, and it leaves expected risk-adjusted
return roughly unchanged for most assets. That is a real benefit, honestly stated. It is not alpha.

---

## 5. Where trading skill is demonstrably real

A page that stopped at §4 would be nihilism, and the evidence does not support nihilism.

**The strongest measurement comes from regulator-grade data — with a provenance warning this page first
lacked.** Using CFTC audit-trail records with trader identifiers, covering 85 high-frequency firms in
E-mini S&P 500 futures over 2010–2012, the **median firm earned an annualized Sharpe of 4.30** and a
four-factor alpha of 22.02% — over thirteen times the index's Sharpe (0.31). The top quartile exceeded
9.10 and the top decile 12.68. **Those figures exist only in the 2014 Baron-Brogaard-Kirilenko working
paper.** When the study reached peer review (JFQA 2019, with Hagströmer added), the confidential CFTC
data was gone: the published version covers 16 HFT firms in Swedish equities — median Sharpe 1.61, alpha
9%. The E-mini census never passed peer review in the quoted form. Performance is strongly *persistent*
where measured: autoregressive coefficients of 0.421 daily and 0.723 monthly for the Aggressive subgroup
(Mixed 0.109/0.407; Passive −0.73 daily), which is precisely the test that mutual-fund performance
famously fails.

And the edge was **not competed away** over the sample. New entrants were less profitable than incumbents
and more likely to exit; the Passive firms' profit Herfindahl rose from 0.287 to 0.545 (the Aggressive
subgroup's showed no trend, 0.362 → 0.381); aggregate profitability
did not decline after controlling for volatility and volume. Returns came overwhelmingly from aggressive,
liquidity-*taking* activity (90.67% annualized alpha) rather than passive market making (23.22%), and
about 45% of aggressive revenue was extracted from other HFT firms rather than from unsophisticated
traders. The measured edge is a differential against other professionals.

**Individual skill is documented too, over samples long enough to matter.** Thorp reports 28.5 years of
convertible-hedge returns compounding at roughly 20% with about 6% volatility and near-zero market
correlation — across approximately 1.25 million individual "bets" averaging $65,000 (his word; his
concurrent *positions* ran in the hundreds). The sample size is the argument.

**And the famous null results are substantially a power failure.** The Fama-French bootstrap — the
canonical evidence that essentially no mutual funds beat the market — **fails to detect skilled managers
about 85% of the time in simulations where skilled managers exist by construction.** Even under generous
assumptions (an information ratio of 1.0, 10% of funds genuinely skilled) the best available test reaches
only 66.3% power, because the best zero-alpha fund's t-statistic is nearly indistinguishable from the
best truly-skilled one. The opposing landmark study has the mirror defect: its bootstrap is badly
oversized, producing false-positive rates of 8.5% to 23.2% against a nominal 5%. **Two celebrated papers,
biased in opposite directions, which is why they reached opposite conclusions from similar data.**

**Skill can be real while being uninvestable.** Berk and van Binsbergen measure managerial skill in
dollars extracted rather than percentage alpha and find the average active fund adds $3.2 million a year,
with differences persisting up to ten years. Over the same sample, net alpha to investors is 3bp/month
equal-weighted and −1bp value-weighted — neither distinguishable from zero. The skill exists; the
manager captures it. Note also that the median fund *destroys* $20,000 a month and only 43% add value at
all: the industry adds value in aggregate only because the skilled minority controls most of the capital.

---

## 6. What it all means together

Assemble the five and a single mechanism runs through them.

**The published playbook is statistically real and economically dead.** That is not a paradox — it is
Grossman-Stiglitz. Prices stay inefficient by roughly the cost of the search that corrects them, so a
published anomaly's remaining return converges toward its implementation cost. The spread is the
equilibrating variable, which is exactly what Chen and Velikov measure.

**You cannot buy statistical certainty with time, because the data does not exist.** Minimum Backtest
Length says five years supports 45 configurations; honest power calculations say a genuine Sharpe-0.5
idea found after 100 variants needs decades. Nobody has that — not you, not Citadel.

**So the industry buys evidence in the only other currencies available.** Breadth, which makes the
t-statistic clock run faster and is why Renaissance's near-coin-flip predictions and WorldQuant's
Sharpe-1.5 signals are profitable in aggregate. Cross-sample replication, which turns one test into
twenty. Mechanism, which is a prior that kills most of the hypothesis space before you touch the data.
And portfolio-level acceptance criteria — Two Sigma's decorrelation parameter — which asks not "is this
good?" but "is this *different* from what we already own?"

**Risk management multiplies and does not create.** The one peer-reviewed counter-example turns out to be
a momentum bet wearing a risk-management costume, and it fails out of sample anyway.

**And skill is real, persistent, and measurable — where the instruments are good enough to see it.**
Regulator-grade transaction data finds it easily; return-based mutual-fund tests miss it 85% of the time.
Absence of a t-statistic is not evidence of absence of edge, which is the single most important qualifier
on everything above.

So: is it a science? **Yes, but it is industrial screening rather than physics** — enormous candidate
libraries, brutal attrition, publication bias, a replication crisis, and a decisive test that is always
out-of-sample. The honest answer to "do you have to come up with your own ideas" is that **you have to
come up with hundreds and expect nearly all of them to die** — and that the arena you choose to search
in matters more than the cleverness of any individual idea.

---

## 7. Confidence tiers — read this before quoting anything above

The run adversarially verified 25 of its 120 extracted claims with three independent skeptics each,
instructed to refute — all of them in the replication-statistics cluster. **Update 2026-07-20: the hole
that left has been closed.** A third pass (four adversarial verifier agents over the run's own cached
PDFs plus the live Senate/GPO/SEC records, with the §2 mathematics independently re-derived by quadrature
and 400,000-path Monte Carlo) adjudicated the seventeen sources the run never attacked, and this page has
been corrected in place where it failed. The full ledger is in
[the run brief](../sources/deep-research-quant-discovery-validation-2026-07-20.md).

**Tier 1 — adjudicated and survived.** Everything in §1 and §2. All 25 originally verified claims came
from seven sources, every one in the replication-and-statistics cluster: McLean-Pontiff, Hou-Xue-Zhang,
Jensen-Kelly-Pedersen, Chen-Zimmermann, Harvey-Liu-Zhu, Chen (2024), and Bailey et al. The mathematical
results were additionally *re-derived* — including by numerical quadrature and 400,000-path Monte Carlo —
rather than merely quote-matched, and re-derived once more in the third pass.

**Tier 2 — adjudicated and killed.** Five claims died across the two adjudication passes (four in the
original run, one in re-verification; an earlier draft of this section said three), and instructively:
every one lost its *interpretive final sentence* while its numbers verified. The refutation arguments
went **eight for eight** against final sentences — a universal quantifier, an epistemic upgrade, or an
exactness claim bolted onto accurate content.

**Tier 3 — attacked late, and it held.** The seventeen practice-side sources (Renaissance, WorldQuant,
Two Sigma, Thorp, the volatility-targeting trio, Lo, both day-trader censuses, the CFTC data, and the
mutual-fund power results) were adjudicated on 2026-07-20. Outcome: **quotes and numbers verified nearly
verbatim everywhere** — the Renaissance statement word-for-word, every Thorp and day-trader-census
figure, the Man Group 45–60%, the Cederburg statistics, the Harvey-Liu power numbers, all five
Berk-van Binsbergen figures. What failed was scope and framing, now fixed above: the CFTC-HFT
publication status, two subgroup mislabelings, the Two Sigma remediation date, the Cederburg metric
choice, and the WorldQuant denominator.

⚠️ **The uncomfortable shape this section originally warned about — evidence strongest where least
actionable — no longer holds; the verification budget now covers the whole page.** The original working
assumption ("quotes and numbers probably sound; concluding interpretations the part to distrust") was
borne out almost exactly: no primary number was found fabricated or misquoted, and every genuine defect
was a gloss, a scope elision, or a date slip.

---

## 8. Honest limits

This report was assembled by hand from recovered claims after the original run's synthesis stage was
killed by a usage limit; it is not the report that harness would have written, and nobody can now know
how that would have differed. Two sources were recovered through mirrors after 403 errors, and one of
those was later proven by hash to be a preprint whose internal numbering contradicts itself — so results
from it are cited here by name rather than by proposition number. The run's own decomposition chose the
sources, so its coverage inherits whatever that decomposition missed: most visibly, there is no evidence
here from inside a pod shop or a market maker beyond what regulators compelled into the open. And the
practice-side picture leans on three firms that agreed to be visible or were forced to be — which is a
selected sample by construction. A third verification pass (2026-07-20) has since adjudicated the
seventeen previously unattacked sources against the same cached primary PDFs plus the live Senate and
SEC records, and corrected this page in place; its ledger is in the run brief.

---

## Relationships

- The derivation this page is the evidence half of:
  [Is Quant Research a Science?](is-quant-research-a-science.md) — read them together.
- Provenance, method, and the full verification ledger:
  [the run brief](../sources/deep-research-quant-discovery-validation-2026-07-20.md).
- The validation machinery §2 demands:
  [backtesting rigor & overfitting](../ml-stats/concepts/backtesting-overfitting.md) and
  [performance metrics](../ml-stats/concepts/performance-metrics.md).
- The decay evidence in §1: [factor premia & alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md);
  why edges persist at all: [limits to arbitrage](../shared/concepts/limits-to-arbitrage.md).
- The firm-scale version of §3: [the industrialization of edge](industrialization-of-edge.md).
- Where this desk's own barriers are: [the alpha map](alpha-map.md).

## Open questions

- **Which anomalies survive costs, at what capacity?** §1 shows the replication debate is dissolved by
  the spread — so the live question is the Chen-Velikov net-of-cost frontier, which this desk has not
  read directly. This is now the highest-value unread paper in the area.
- **Does the volatility-targeting adjudication in §4 hold up under verification? — Answered 2026-07-20:
  yes.** Verified against all three primary PDFs; every number held, including the 45–60% momentumness
  R². The one added disclosure: "72 of 103" is the certainty-equivalent metric (58 of 103 by Sharpe).
- Can the Minimum Backtest Length bound be wired into a standing pre-trade gate — a signal is only worth
  building if its breadth returns a verdict inside a decision-relevant horizon?
