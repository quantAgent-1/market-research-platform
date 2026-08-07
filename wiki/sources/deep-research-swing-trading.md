---
type: research-brief
title: "Swing Trading & Momentum — Does It Have an Edge? (Deep-Research Brief, 2026)"
description: The honest, mostly-skeptical evidence on whether swing-trading and momentum strategies have a real edge net of costs — and where the data-snooping, decay, and cost critiques bite.
tags: [systematic-trading, momentum, swing-trading, evidence, factor]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: []
---

# Swing Trading & Momentum — Does It Have an Edge? Deep-Research Brief

**Source:** Claude Code `deep-research` run `wf_ffc3eb7e-b4a` (2026-06-14; hit a session-quota wall
mid-verification, **resumed** after the 5am reset).
**Method:** 5 angles → 24 sources → 103 claims → 25 adversarially verified → **20 confirmed, 5
refuted → 11 findings.** Sources are strong (*J. Finance*, JFE, *J. Financial Econometrics*),
verbatim-verified.
**Scope honesty:** the verification budget went to the *edge / cost / data-snooping* question
(Angles 1, 2, 6). It did **not** surface verified evidence on the **semiconductor regime**,
**risk-sizing specifics**, **momentum crashes**, **PEAD**, **short-term reversal**, or the **retail
base rate** — those remain open (see gaps).

## The one-paragraph answer
The honest verdict is **mostly skeptical**. The only swing approaches with a serious academic
backbone are **momentum** (cross-sectional MOM2-12 and 52-week-high) — and even there, **net-of-cost
survival is genuinely contested**: the equal-weighted/small-cap version is gutted by costs, while
liquidity-weighted versions may survive to multi-billion-dollar scale. **Technical price-action
rules** (moving-average/breakout) had a real *in-sample* edge on a century of DJIA data that
**completely disappears out-of-sample and on tradable S&P futures once you correct for the thousands
of rules searched** — and no rule survives in mature US large-cap indices (exactly where megacap
semis trade). On top of that, published edges **decay ~26% out-of-sample and ~58% post-publication.**
None of this says swing trading is impossible — it says the edge is small, fragile, cost-sensitive,
decaying, and concentrated in places (small/young markets) that megacap-semi traders don't operate.

## Confirmed findings (synthesized)

### Momentum — the real but contested backbone
- **Net-of-cost survival is a live debate.** Equal-weighted momentum is *best gross, worst after
  costs* (it tilts to illiquid small caps).
  [Korajczyk-Sadka (2004, JF)](https://www.kellogg.northwestern.edu/faculty/korajczy/htm/Korajczyk%20Sadka.jf2004.pdf):
  liquidity-weighted momentum survives to **~$5B capacity** (Dec-1999 terms) before alpha →0;
  [Lesmond-Schill-Zhou (2004, JFE)](https://www.researchgate.net/publication/222429602_The_Illusory_Nature_of_Momentum_Profits)
  argue costs make the standard strategy an "illusion of profit." Live-trade data (Frazzini-Israel-
  Moskowitz 2015) finds real costs ~10× smaller than Lesmond's estimates. *The strong "momentum never
  beats costs" claim was refuted 0-3.*
- **Definition:** the standard signal is **MOM2-12** — past 12-month return skipping the most recent
  month (to dodge 1-month reversal) —
  [Asness-Moskowitz-Pedersen (2013, JF)](https://w4.stern.nyu.edu/facdir/lpederse/papers/ValMomEverywhere.pdf).
  *(Their "momentum in all 8 markets" claim was refuted 0-3 here — use this for the definition, not
  as proof of universal robustness.)*
- **52-week-high (the breakout archetype):**
  [George-Hwang (2004, JF)](https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf): nearness to the
  52-week high gives W-L ~**1.23%/mo** (ex-Jan) and statistically *subsumes* Jegadeesh-Titman
  momentum — but **in-sample 1963-2001, US, gross**; later work finds it small/insignificant US
  1980-2014 (decay).
- **Time-series / single-name trend momentum is weaker than believed (contested):**
  [Huang et al. (2020, JFE)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3165284) — asset-by-
  asset evidence is weak (47/55 assets t<1.65) and the pooled t fails bootstrap; and where TSM *is*
  profitable, it performs like a **net-long exposure** strategy, not genuine prediction
  (Goyal-Jegadeesh). *Contested by AQR/D'Souza who defend trend over 100+ years.* Implication:
  single-name trend-following profit may be long-bias/risk-premium, not a forecasting edge.

### Technical rules — the headline reversal
- **In-sample:** the best technical rule on ~100yr DJIA beat the benchmark even after data-snooping
  correction ([Sullivan-Timmermann-White 1999, JF](https://www.kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Sullivan_Timmermann_White.pdf)).
- **Out-of-sample / tradable: it vanishes.** OOS 1987-96 the best rule's Reality-Check p-value is
  **0.341** (not significant); on **S&P 500 futures** the snooping-adjusted p-value is **0.90-0.99**.
  "There is no evidence that any trading rule outperforms."
- **No edge in mature US large-caps:**
  [Hsu-Kuan (2005)](https://www.researchgate.net/publication/5213483_Reexamining_the_Profitability_of_Technical_Analysis_with_Data_Snooping_Checks)
  — profitable rules exist in *young* markets (NASDAQ, Russell 2000) **but not DJIA / S&P 500**.
  Megacap semis are S&P 500 large caps → the unfavorable side. *(The "young-market edge survives
  costs OOS" claim was refuted 0-3.)*

### Alpha decay — the strongest skeptic's pillar
- [McLean-Pontiff (2016, JF)](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365): published
  predictors decay **~26% out-of-sample, ~58% post-publication** (US-specific). Decay is *not* pure
  data-snooping (~10% statistical bias, insignificant) — the rest is crowding — but what survives is
  **economically marginal net of costs** (Chen-Velikov: ~8 bps/mo).

## What got refuted (did NOT survive)
- "Momentum profits don't exceed costs / are illusory" (0-3 — overstated; contested by Korajczyk-
  Sadka, Frazzini et al.).
- "Momentum earns a premium in all 8 markets/asset classes" (0-3 — overstated from that single source).
- "BLL technical edge is robust to data-snooping in all DJIA subperiods" (0-3).
- "Technical-rule disappearance is due *solely* to rising market efficiency" (0-3 — three explanations
  exist).
- "Young-market technical edge is robust to costs out-of-sample" (0-3).

## Caveats
- **Scope gaps (open, not covered):** semiconductor/AI-rally regime; risk-sizing (ATR/Kelly/risk-of-
  ruin); momentum crashes (Daniel-Moskowitz); PEAD; short-term reversal; the retail-loss base rate.
  These were in the question but produced no verified claims.
- **Live debates:** momentum cost-survival, TSM predictability, and durability of surviving alpha are
  genuinely two-sided (several 2-1 votes — read as "one rigorous side").
- **Vintage:** core results are in-sample and dated (Korajczyk-Sadka Dec-1999; George-Hwang
  1963-2001; STW ends 1996; Hsu-Kuan ends 2002). OOS decay means today's exploitable edge is likely
  smaller; none addresses 2023-2026.
- **Index-level, not single-name:** the technical-rule evidence is on *indices*, a real scope limit
  for applying it directly to NVDA/AMD/etc.

## Open questions (a focused follow-up could target)
1. The **2024-2026 AI-semiconductor regime** with recent data (SOX/SMH breadth, leadership, forward
   P/E vs history, earnings IV, the megacaps through 2018/2022 drawdowns).
2. **Momentum crashes** (Daniel-Moskowitz 2016) in high-beta single names — magnitude/frequency, and
   the sizing/trend-filter response.
3. The **retail/active-trader loss base rate** (Barber-Odean and successors) and which risk rules
   (ATR, R-multiples, fractional-Kelly) distinguish the durable minority.
4. **PEAD** and **short-term reversal** net of costs in liquid large-caps today; earnings-gap tail
   risk for single-name semi catalyst swings.

## Feeds into the wiki
- New: [Momentum](../systematic-trading/factors-signals/momentum.md) ·
  [Swing trading](../systematic-trading/strategies/swing-trading.md) ·
  [Regime detection](../ml-stats/concepts/regime-detection.md) ·
  [Semiconductors](../shared/instruments/semiconductors.md)
- Strengthens: [Factor premia & alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md) ·
  [Backtesting & overfitting](../ml-stats/concepts/backtesting-overfitting.md) ·
  [Who actually wins](../shared/concepts/who-wins-empirical-record.md)

## Primary sources (verified)
- Korajczyk & Sadka (2004, JF) — https://www.kellogg.northwestern.edu/faculty/korajczy/htm/Korajczyk%20Sadka.jf2004.pdf
- Lesmond, Schill & Zhou (2004, JFE) — https://www.researchgate.net/publication/222429602_The_Illusory_Nature_of_Momentum_Profits
- Asness, Moskowitz & Pedersen (2013, JF) — https://w4.stern.nyu.edu/facdir/lpederse/papers/ValMomEverywhere.pdf
- George & Hwang (2004, JF) — https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf
- Huang, Li, Wang & Zhou (2020, JFE) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3165284
- Sullivan, Timmermann & White (1999, JF) — https://www.kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Sullivan_Timmermann_White.pdf
- Hsu & Kuan (2005, J. Financial Econometrics) — https://www.researchgate.net/publication/5213483_Reexamining_the_Profitability_of_Technical_Analysis_with_Data_Snooping_Checks
- McLean & Pontiff (2016, JF) — https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365
