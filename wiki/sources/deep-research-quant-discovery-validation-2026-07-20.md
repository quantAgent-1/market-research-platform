---
type: research-brief
title: "Deep-research — How Systematic Strategies Are Actually Discovered and Validated (recovered run, 2026-07-20)"
description: Provenance + verified ledger for the uncontaminated second-opinion run on whether quant research is a scientific process — 24 primary sources, 120 extracted claims, 18 adversarially adjudicated in-run, 7 re-verified after the crash, and the 17 practice-side sources adjudicated in a third pass (2026-07-20). Recovered from workflow state after the session died on a usage limit before synthesis.
resource: workflow wf_1fe1d6d7-52a
tags: [systematic-trading, ml-stats, methodology, epistemics, replication, evidence]
timestamp: 2026-07-20T00:00:00Z
status: active
sources: []
---

# Deep-research — How Systematic Strategies Are Actually Discovered and Validated

**Run:** workflow `wf_1fe1d6d7-52a` (task `wkuuhl9qf`) · 106 agents · 5.47M tokens · 1,356 tool calls
· 29m27s · **24 primary sources → 120 claims → 18 adversarially adjudicated.**
**Synthesized into:**
[How Systematic Strategies Are Actually Discovered and Validated](../synthesis/how-strategies-are-discovered-and-validated.md)
— the readable report, and the deliverable this run was launched to produce.
**Also reconciles into:** [Is Quant Research a Science?](../synthesis/is-quant-research-a-science.md) (§11–§12).

## Why this page exists (read this first)

This run completed normally at 2026-07-19T20:59:00Z and then **the session hit its usage limit in the
same second the completion notification arrived.** No answer was ever written. The chat that launched
it ends with the limit message and nothing else.

The damage was not confined to the write-up. The limit began biting during the verification phase and
killed agents on the way out, in this order:

- **21 of 75 verifier agents died** — which is exactly the three voters on each of seven claims. Those
  seven were reported as "unverified" by the harness, which reads like a design choice and is not one.
  They are claims whose adjudication was destroyed.
- **The synthesis agent died** having produced nothing. Its transcript holds its prompt and one reply:
  the limit message. The harness's own result object says so plainly — *"Synthesis step was skipped or
  failed — returning 14 verified claims unmerged."*

Everything upstream survived intact in the workflow state and the 106 agent transcripts: all 120 claims
with verbatim quotes and sources, and the full reasoning behind all 54 surviving votes. This page is
the recovery. **The research was never lost; only the report was, and this replaces it.**

## Question

Is building a quant model and a profitable strategy a scientific process of experiments — must you
generate your own hypotheses and backtest them — or is it a well-known playbook where what matters is
risk appetite and stock selection? Five sub-questions: post-publication decay and the replication
crisis *including its serious rebuttals*; the first-principles statistical limits; the documented
research process inside firms; whether sizing can substitute for edge; and the counter-evidence where
skill demonstrably persists.

The run was launched **deliberately uncontaminated** — the arguments carried none of the conclusions
from [Is Quant Research a Science?](../synthesis/is-quant-research-a-science.md), written earlier the
same session. The point was an independent second opinion, so that **disagreement between the two
passes would itself be the deliverable.**

## Method and its honest state

Five search angles → 24 primary sources fetched → 5 falsifiable claims extracted per source with
verbatim supporting quotes → top 25 claims sent to 3-vote adversarial verification, each voter
instructed to *refute*.

| Stage | Designed | Actually delivered |
|---|---|---|
| Sources fetched | 15 target | **24** |
| Claims extracted | — | **120** (all recovered, all quoted) |
| Claims verified | top 25 | **18 adjudicated**, 7 destroyed by the limit |
| Verdicts | 14 confirmed / 4 refuted | same, but see the refutation caveat below |
| Synthesis | 1 report | **none** — recovered by hand here |

**The four "refutations" are not what the label suggests.** In every one of the four, the verifiers
confirmed the underlying statistics verbatim against the primary PDF and refuted only the claim's
*interpretive gloss*. The correct reading is *keep the numbers, drop the framing*. Two examples:

- The Jensen-Kelly-Pedersen out-of-sample statistics (82.6% / 83.3% / 87.4% positive; GLS slopes 0.57,
  0.26, 0.35 at t = 3.5–5.3) verified exactly. What died was the gloss "a slope of 0.26 means roughly a
  quarter of in-sample edge survives," which confuses a regression slope with a level ratio and
  contradicts the paper's own 47% decay figure one page earlier.
- The Chen-Zimmermann counting critique of Hou-Xue-Zhang (452 anomalies → 240 characteristics → 118
  ever significant → 117 reproduce) verified verbatim. What died was calling HXZ's headline "roughly
  50%" — HXZ say 65% — and presenting one side of a live dispute as settled.

So the pass killed sloppy summarising, not evidence. That is the verification working.

## The 24 sources

All rated primary. Peer-reviewed finance journals (JF, RFS, JFE, JPM, FAJ), Fed and CFTC working
papers, an AMS *Notices* paper, a Senate PSI hearing record, an SEC enforcement release, and Thorp's
handbook chapter. Notable that three independent regulator-grade datasets appear — CFTC audit-trail
HFT data, the Brazilian CVM day-trader census, and Taiwan Stock Exchange complete transaction data —
none of which can be selection-biased by voluntary reporting.

Two provenance flags the extractors raised on themselves, which is the behaviour you want: the
Renaissance prepared statement (senate.gov returned 403) was recovered via corroborated search rather
than from the PDF, and the AMS paper (also 403) was verified against the lead author's own preprint
mirror with identity confirmed by title, all four authors, and the referee acknowledgement.

## What it establishes

**The replication fight is about statistical existence, and it is genuinely unresolved.** The same
question yields 18% to 82.4% depending on defensible methodology choices — Hou-Xue-Zhang get 35% (18%
after multiple-testing correction); Jensen-Kelly-Pedersen get 82.4% under hierarchical Bayes with a
2.8% posterior standard error, and the identical 82.4% out-of-sample in 93 countries; Chen-Zimmermann
reproduce 98% of 161 clearly-significant predictors when re-coded from scratch. Chen separately bounds
the false-discovery rate among published predictors at 22% and shows Harvey-Liu-Zhu's famous t > 3.0
hurdle is *not empirically identified* — the data support anything from 0 to 3.0.

**And it does not matter as much as it looks, because of one sentence.** Chen and Zimmermann, having
shown that predictability survives publication, write immediately afterward: *"these results do not
account for trading costs. Indeed, Chen and Velikov (2019) find that the remaining predictability is
eliminated by effective bid-ask spreads."* The optimists and the pessimists are arguing about whether
published anomalies are statistically real. **Both camps agree they are not tradeable.** For a
practitioner the replication debate is largely moot, and this is the single most useful thing the run
recovered.

**The first-principles limits are theorems, and they are worse than the folklore.** Expected maximum
in-sample Sharpe under N trials at *zero true skill* is E[max] ≈ (1−γ)Z⁻¹(1−1/N) + γZ⁻¹(1−1/(Ne)),
bounded by √(2 ln N). **Minimum Backtest Length inverts it: five years of data supports at most 45
independent configurations; two years supports seven** — re-verified below, and these are exact integer
boundaries, not round figures. Lo's Sharpe standard error is sqrt((1 + SR²/2)/T), which carries a
genuinely counterintuitive consequence — at fixed sample size the standard error *rises* with the true
Sharpe, so high-Sharpe strategies are harder to validate, not easier.

Bailey and López de Prado add the sting: with memory in the series, overfitting stops being
performance-neutral out of sample. Their propositions **prove** that optimizing in-sample *reverses* the
ordering out of sample — better in-sample implies worse out-of-sample. The stronger statement, that
expected out-of-sample returns go outright **negative**, is a Monte Carlo result rather than a theorem,
so it should be cited as simulation evidence. Their own summary: "when investment advisers do not
control for backtest overfitting, good backtest performance is an indicator of negative future
results." Holdout and k-fold do not save you; ~20 applications at 95% confidence make a false positive
expected, and the survivor is then reported as a single-trial result.

**Breadth is confirmed from primary sources, under oath.** Renaissance told the Senate that Medallion's
model "makes predictions that are profitable only slightly more often than not" and that the returns
come from "the mathematical principle known as the law of large numbers" — with the record quantifying
the breadth at more than 100,000 trades a day, ~30 million a year. WorldQuant's published study of
4,002 real production alphas gives a median standalone annualized Sharpe of **1.487** (computed over its
3,289 positive-Sharpe alphas — see third pass), combined algorithmically into a "mega-alpha." This is IR = IC·√BR with receipts: near-zero per-bet accuracy,
enormous N.

**Sizing multiplies edge and cannot create it — with one serious challenge that has to be handled.**
Thorp is unambiguous: f* is a function of the edge (f* = m/ab, valid only if m > 0), and leverage past
a critical fraction converts a favourable game into near-certain ruin (at p = .53, f* = .06 but ruin
begins at f_c = .11973). The Brazilian census is the empirical version: of 19,646 traders, 97% of those
persisting past 300 days lost money, and the single best earned $310/day against a $2,560 daily
standard deviation — a daily Sharpe near 0.12, which is risk-taking, not edge.

The challenge is volatility targeting, and it is a real three-paper dispute. Moreira-Muir (JF 2017)
find a pure inverse-variance sizing rule containing *no return forecast* earns 4.86% annualized alpha
on the market — explicitly sizing substituting for prediction. Cederburg and coauthors (JFE 2020)
answer that only 53 of 103 strategies improve on Sharpe (p = 0.84, and *fewer* than the 66 expected
under the null, bootstrap p = 0.01), and that implementable real-time versions lose to simply holding
the unmanaged portfolio in 72 of 103 cases (by certainty-equivalent return; 58 of 103 by Sharpe). Man Group's own researchers — arguing against their
commercial interest — show the benefit is confined to assets with a leverage effect and that
"momentumness" explains 45–60% of the cross-sectional variation in Sharpe improvement. **The
resolution: vol-targeting's alpha is a time-series momentum bet in disguise, i.e. a smuggled edge, and
it does not survive real-time implementation.** The multiplier claim survives, but it has to be stated
this way rather than asserted.

**Skill exists, persists, and is measurable — where the instruments are good enough.** CFTC
audit-trail data on 85 HFT firms in E-mini futures: median firm Sharpe **4.30**, four-factor alpha
22.02%, top decile above 12.68 (third-pass caveat: those figures live only in the 2014 working paper —
the peer-reviewed JFQA 2019 version is 16 firms in Swedish equities, median Sharpe 1.61, alpha 9%).
Return persistence coefficients of 0.421 daily and 0.723 monthly (Aggressive subgroup) — and the edge
was *not* competed away over the sample: new entrants were less profitable, exited more, and the
Passive firms' profit Herfindahl rose from 0.287 to 0.545. Thorp's own 28.5-year record compounds ~20% at ~6%
volatility across ~1.25 million individual bets. Against that, the mutual-fund null results are
substantially a power failure: the Fama-French bootstrap fails to detect skilled managers **85% of the
time when they exist by construction**, and even at IR = 1.0 with 10% of funds skilled the best
available test reaches only 66.3% power.

**Elite firms are not the rigorous ideal the folklore imagines.** The SEC's January 2025 Two Sigma
order: one employee altered fourteen live models over 21 months without detection; internally
identified vulnerabilities sat from March 2019 to October 2023 unremediated (August 2023 was when the
tampering was detected); $165M repaid and $90M in penalties. The mechanism matters more than the scandal — the researcher drove *decorrelation
parameters* toward zero so his models mimicked the existing book while appearing to add unique alpha.
That tells you what institutional validation actually optimizes: **marginal alpha net of correlation to
what the firm already runs**, measured and paid on explicitly.

## The seven claims the limit destroyed — RE-VERIFIED 2026-07-20

The hole is closed. Nine fresh independent skeptics (three voters per source group) re-ran the
adjudication against the **original cached PDFs** from the dead session's `tool-results/` — the same
bytes the extractors read, which removes the 403-and-mirror risk that dogged the first pass. Because
these are theorems rather than estimates, the voters were told to **rederive** rather than quote-match.

**Six survive, one is killed.**

| Claim | Refutes | Verdict |
|---|---|---|
| Chen — t > 3.0 not empirically identified | 1/3 | survives, pairing corrected |
| Chen — structural cause of the failure | **2/3** | **killed on its final sentence** |
| Expected maximum Sharpe under N trials | 1/3 | survives as reportage, math corrected |
| Minimum Backtest Length | 0/3 | survives — reproduces exactly |
| Overfitting destructive under memory | 0/3 | survives — proof scope narrowed |
| N almost never disclosed | 1/3 | survives, "in principle" corrected |
| Harvey-Liu-Zhu hurdle + tail clause | 0/3 | survives 3-0 |

**MinBTL came through strongest.** 45 and 7 are not rounded — they are the precise integer boundaries
(N=45 → 4.998 yr, N=46 → 5.036 yr; N=7 → 1.923 yr, N=8 → 2.129 yr), reproduced independently of the
paper's own figure. One voter also settled a question the paper leaves implicit: **MinBTL-in-years is
frequency-free under the null**, because the q term in Var[ŜR] = (1 + SR²/2q)/y vanishes at SR = 0.
Frequency re-enters only through finite-sample tails, where MinBTL runs ~4% **anti-conservative** at
T=24 — short monthly backtests, exactly where the temptation to overfit is worst. (Third-pass
refinement: that ~4% is tail inflation versus normal theory; net of the Gumbel approximation's built-in
overshoot, the two-year boundary is calibrated exactly — realized E[max] = 1.000 over 400k paths — and
the five-year boundary runs ~1.6% hot.)

**The one correction that matters for practice: E[max_N] is not a Sharpe ratio.** It is a dimensionless
order statistic that equals an annualized Sharpe *only on a one-year sample*. Scaled properly, ten
trials at zero skill gives **1.575 at one year, 1.113 at two, 0.704 at five, 0.498 at ten.** Quoting
"ten trials manufactures a Sharpe of 1.57" against a normal five-year backtest overstates the null
threshold by **2.24×**. Two voters independently computed the exact expectation by quadrature and by
400,000-path Monte Carlo, agreeing to three decimals: the true value at N=10 is **1.5388** (the paper's
Gumbel approximation runs +2.3% high) and at N=128 it is **2.5946** — i.e. *below* the paper's stated
"above 2.6". The approximation is applied by its own authors at N=7 and N=10, well outside the "N ≫ 1"
regime they state for it.

**Citation warning.** The cached PDF was proven by SHA-256 to be byte-identical to the author's preprint
mirror, **not** the published Notices article (34pp single-column versus 14pp two-column,
61(5):458–471). It is the post-referee text, but its numbering is unstable: the formal environments read
"Proposition 2.1" and "Theorem 3.1" while **the same document's body cites them as "Proposition 1" and
"Theorem 1"**. Cite these results *by name and page range*, never by proposition number.

**A trap worth recording.** Raw PyMuPDF extraction renders the formula's second term as `1 − 1/(Ne⁻¹)`,
which evaluates to 0.89 at N=10 and looks like a clean refutation. The correct reading is `1 − 1/(Ne)`,
confirmed three ways — glyph baseline coordinates, the authors' own published Python
(`ss.norm.ppf(1-1./(numTrials*np.e))`), and the fact that only that parse reproduces 1.57. A verifier
trusting the text layer would have produced a confident false refutation.

**What was killed, and why it is the same failure every time.** The refuted claim's first two-thirds is
near-verbatim from Chen's abstract; what died is its appended sentence, *"This is a general constraint
on any multiple-testing correction estimated from a published-literature sample."* That inverts the
paper's actual contribution — Chen's point is that the constraint is **selective**, which is why he
tells the field to focus on the strongly-identified statistics. The sentence is also self-contradicting:
empirical Bayes shrinkage and the local FDR *are* multiple-testing corrections estimated from published
literature, and the claim's own preceding clause calls them strongly identified.

**⭐ The method finding.** Across both passes, **every single refutation — eight for eight — killed the
final sentence of a claim while its numbers and quotes verified.** A universal quantifier ("any"), an
epistemic upgrade ("in principle"), or an exactness claim ("true by construction") gets appended to
accurate content. And on three of the claims here the voters were **unanimous about the defective
sentence while splitting on whether it was fatal** — so the binary refuted/not-refuted tally is close to
noise, while the named failing sentence is reliable. **The vote count is the least informative output of
this harness; the identified sentence is the valuable one.**

## Honest limits

**The verification is far more lopsided than a "25 of 120 claims" summary suggests, and this is the most
important caveat on the page.** All 25 claims sent to adjudication came from just **seven sources, every
one of them in the replication-statistics cluster**: McLean-Pontiff, Hou-Xue-Zhang,
Jensen-Kelly-Pedersen, Chen-Zimmermann, Harvey-Liu-Zhu, Chen (2024), and Bailey et al. That is where
this page's evidence is strong.

**Seventeen sources were never adjudicated by the run itself** (hole closed by the third pass below,
2026-07-20) — and they carry most of the practice-side material:
the Renaissance testimony, WorldQuant's 4,002 alphas, the CFTC HFT figures, the Two Sigma order, Thorp,
the entire Moreira-Muir / Cederburg / Man Group vol-targeting dispute, Lo's Sharpe standard error, the
Brazilian and Taiwanese day-trader censuses, the Fama-French bootstrap power result, and Harvey-Liu's
nonlinear Sharpe haircut. Those claims are verbatim quotes from named primary documents, extracted by an
agent that flagged its own provenance problems honestly — but **no skeptic ever attacked them.** Given
that eight of eight adjudicated refutations killed an over-generalizing final sentence, the working
assumption for every unadjudicated claim should be that its **quotes and numbers are probably sound and
its concluding gloss is the part to distrust.** Two figures have since been confirmed incidentally
(Jensen-Kelly-Pedersen's 0.93 out-of-sample information ratio, and Harvey-Liu-Zhu's 2.27 traced to their
own Table 5), which is encouraging but is not a substitute for the pass. The pass itself has now been
run — see the third-pass section below.

The synthesis above is mine, assembled from the recovered claims — it is not the report the harness
would have written, and no one can now know how that would have differed. Two sources were recovered
through mirrors after 403s, flagged in place; one of those mirrors was later proven by hash to be a
preprint whose internal numbering contradicts itself. The run's own decomposition chose the sources, so
its coverage inherits whatever that decomposition missed — most visibly, there is no evidence here from
a pod shop's or market maker's internal research protocol beyond what regulators compelled into the
open.

## Third pass — the seventeen unattacked sources, adjudicated (2026-07-20)

Run from the enginev5.1 session at the user's request ("verify the report from first principles").
Method: **four adversarial verifier agents** — each instructed to refute, quote verbatim, and report
page/table locations — over this run's own cached PDFs in the dead session's `tool-results/` (the same
bytes the extractors read), plus the live records where nothing was cached (Senate PSI Joint Statement
and Report via hsgac/govinfo, the hearing transcript S.Hrg. 113-422, SEC Order 34-102207 via sec.gov).
In parallel, every §2/§4 mathematical claim was **re-derived independently**: exact E[max] by
quadrature, the MinBTL integer boundaries, 400,000-path Monte Carlo at the T=24 and T=60 boundaries,
OU/AR(1) ordering-reversal simulations, Kelly numerics, and Lo's AR(1) annualization arithmetic.
41 claim clusters were checked.

**Result: the numbers held almost universally.** The Renaissance statement is word-for-word in the
Joint Statement; the PSI record confirms $34.2B across exactly 60 options (31 Barclays + 29 Deutsche
Bank, 2000–2014), leverage up to 20:1 (Deutsche Bank's ceiling was 18:1), and 100,000–150,000
trades/day *per bank* (26–39M/yr combined — the round 100k/30M is Levin's rounding); every Thorp figure
including f\* = .06, f_c = .11973, and the lim-sup/lim-inf oscillation theorem; every Brazilian and
Taiwanese census figure including the −0.22/+2.36 skew pair; Moreira-Muir's 4.86%/25%; the Man Group
45–60% momentumness R² (Exhibit 20); Cederburg's 53/103, p = 0.84, the 66-expected null, p = 0.01, and
the 30%-drop-with-positive-alpha sentence verbatim; Harvey-Liu's 8.5–23.2% size distortion, 15.0% power
(= the 85% miss rate) and 66.3% ceiling; and all five Berk-van Binsbergen figures.

**What failed — every failure a scope, framing, or provenance defect, corrected in place on the report
page:**

1. **CFTC-HFT provenance (the material one).** Median Sharpe 4.30 / alpha 22.02% / 85 firms exist only
   in the April 2014 Baron-Brogaard-Kirilenko working paper (SSRN 2433118). The peer-reviewed successor
   (Baron-Brogaard-Hagströmer-Kirilenko, JFQA 54(3) 2019) lost the confidential CFTC data and covers 16
   HFT firms in Swedish equities: median Sharpe 1.61, alpha 9%. The E-mini census never survived peer
   review in the quoted form.
2. **Two subgroup mislabelings:** persistence 0.421/0.723 is the Aggressive-HFT subgroup (Mixed
   0.109/0.407, Passive −0.73 daily); Herfindahl 0.287→0.545 is Passive-only (Aggressive 0.362→0.381,
   no trend).
3. **Two Sigma dates:** the Order (¶33; "Relevant Period," ¶2) says remediation came in **October
   2023**; August 2023 was detection. Fourteen models exactly (Nov 2021–Aug 2023). Pay ran off "net
   overperformance" (¶30); the decorrelation metric itself gated model approval (¶18).
4. **Cederburg's "72 of 103" is the certainty-equivalent metric;** the Sharpe-ratio analogue is 58 of
   103 (45 outperform). The report had silently used the stronger statistic.
5. **WorldQuant's median 1.487 is computed on n = 3,289** (Table 1) — after excluding the 366
   negative-Sharpe alphas (itself a derived count, 4,002 − 3,636, never printed as a numeral) and
   others.
6. **McLean-Pontiff's 26%/58% are panel-regression estimates** (coefficients −0.150/−0.337 on the 0.582
   base), not ratios of the raw means (which give 31%/55%).
7. **HLZ takes both tables:** the headline BHY hurdles are 2.78 at 5% FDR (= HXZ's hurdle) and 3.39 at
   1%, stated minimum 3.18; the structural model at HLZ's own best-fit ρ = 0.2 gives 2.95 ≈ 3.0 at 1%
   and 2.27 at 5%. The elected-error-rate conclusion survives; the single-number framing did not.
8. **MinBTL calibration:** the ~4% anti-conservativeness is tail inflation versus normal theory; net of
   the Gumbel overshoot, the two-year boundary is calibrated exactly (realized E[max] = 1.000, 400k
   paths) and the five-year boundary runs ~1.6% hot.
9. **"Under serially correlated returns" → mean reversion.** Proposition 6.3's hypothesis is a
   stationary AR(1) performance series with equal volatilities; simulation confirms positive
   autocorrelation alone produces no reversal (OU cumulative PnL: corr(IS, OOS) = −0.70; AR(1)+0.3 on
   returns: +0.01).
10. **Wording:** Thorp's 1.25M are "bets" (his concurrent positions ran in the hundreds); HXZ say
    "quantitatively similar," not "statistically indistinguishable"; JKP's 47% decay is
    post-original-sample, not post-publication; and the report's Tier-2 count was three where the two
    passes' records show five (4 + 1).

**One flag for downstream pages:** the $23.5M Modeler-A compensation figure circulating in the
signal-combination working note is **not in the SEC order** — the Order says only "millions of dollars
of additional compensation." Any specific figure needs a press citation and a SECONDARY label. Also:
it is an SEC administrative order (settled), not a court document.

The report's second open question — does the §4 vol-targeting adjudication survive verification — is
**answered: yes**, with the metric disclosure in item 4.

## Links into the wiki

- Reconciles into and corrects [Is Quant Research a Science?](../synthesis/is-quant-research-a-science.md)
  — resolves its §10 pending items on Chen-Zimmermann and Jensen-Kelly-Pedersen, and answers its
  highest-value open question via the trading-cost reconciliation.
- Sharpens [backtesting rigor & overfitting](../ml-stats/concepts/backtesting-overfitting.md) with
  MinBTL, the expected-maximum-Sharpe theorem, and the nonlinear Sharpe haircut.
- Supplies primary-source receipts to [the industrialization of edge](../synthesis/industrialization-of-edge.md)
  (Renaissance under oath, WorldQuant's 4,002 alphas, Two Sigma's decorrelation criterion).
- Bears on [factor premia & alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md).
