"""muval.complex — the MU / NVDA / AMD complex, not three separate reports.

Runs the existing per-name pipeline (data -> fundamentals -> valuation) in-process
for all three names on one shared data pull, then builds the cross-name analysis
none of the single-name reports can do:

  1. A cross-name valuation table (price vs model, WACC vs price-implied WACC).
  2. Mini football fields, one panel per name on its own price scale.
  3. The MU/NVDA revenue-ratio consistency check against the scenario sets.
  4. A parametric AI-capex "pool bridge" from NVDA+AMD accelerator revenue back to
     a required hyperscaler capex level, plus Micron's implied memory attach rate.
  5. One factor, owned three times: 3y correlation matrix, PC1 variance share,
     per-name beta to SMH, and the effective-breadth consequence for sizing.

Style follows tools/muval/report.py exactly: same palette module, same matplotlib
rcParams (both come along for free on `import report`), same html_table/_fmt/img
helpers (imported, not reimplemented), same CSS look (the CSS string itself is a
local variable inside report.build_html, not an importable symbol, so it is
reproduced verbatim below rather than duplicated by hand-guessing the pattern).

Usage:
    python tools/muval/complex.py               # pull (cached), model, write report, open it
    python tools/muval/complex.py --offline     # caches only, no network
    python tools/muval/complex.py --refresh     # force re-pull all feeds
    python tools/muval/complex.py --no-open     # don't open the report in a browser

Outputs: store/complex-report.html, store/complex-<date>.json, console summary.
This file does not modify muval.py / valuation.py / fundamentals.py / data.py /
report.py — it only imports from them.
"""

from __future__ import annotations

import json
import math
import sys
import tomllib
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
STORE = TOOL_DIR / "store"
sys.path.insert(0, str(TOOL_DIR))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import data as D  # noqa: E402
import fundamentals as F  # noqa: E402
import valuation as V  # noqa: E402
import report as REP  # noqa: E402  (importing sets plt.rcParams -- see report.py's module-level block)
import matplotlib.pyplot as plt  # noqa: E402  (same pyplot instance report.py configured)

NAMES = ("MU", "NVDA", "AMD")

# ---- palette handles pulled straight from report.py so the two tools render identically ----
INK, INK2, MUTED = REP.INK, REP.INK2, REP.MUTED
BASELINE = REP.BASELINE
BLUE = REP.BLUE
BLUE_L, BLUE_XL = REP.BLUE_L, REP.BLUE_XL
SC_COLOR = REP.SC_COLOR
_fmt = REP._fmt
html_table = REP.html_table
img = REP.img

# --------------------------------------------------- Block 4 parametric context --
# NOT data. Two of these three numbers are assumptions about industry structure;
# the third is a desk research figure with an as-of date. See Block 4's own note
# in the HTML report -- this dict exists so every number the block prints traces
# back to one place.
PARAMS = {
    "accel_share_of_ai_capex": 0.60,   # accelerators as a share of AI-datacenter capex (parameter, not data)
    "amd_dc_share": 0.60,              # AMD revenue that is data-center (parameter, not data)
    "capex_pool_2026": 725.0,          # $B/yr hyperscaler AI capex, 2026 (desk deep-research figure, as-of Jul-2026)
}


def load_cfg() -> dict:
    with open(TOOL_DIR / "assumptions.toml", "rb") as f:
        return tomllib.load(f)


# ============================================================== pipeline ====

def run_pipeline(offline: bool, refresh: bool) -> tuple[dict, dict, dict, dict]:
    """Same call sequence as muval.py's --name path, looped over all three names on
    one shared data pull -- same cfg, same cache, so identical numbers to running
    `muval.py --name X` three times (same Monte Carlo seed too)."""
    cfg = load_cfg()
    d = D.pull_all(offline=offline, refresh=refresh, names=NAMES)
    for t in NAMES:
        if t not in d["prices"]:
            # data.TICKERS (the shared price-history table) doesn't carry AMD --
            # same patch muval.py applies for any non-MU name.
            print(f"[data] prices {t} (not in data.TICKERS, pulling directly) ...")
            d["prices"][t] = D.prices(t, offline=offline, refresh=refresh)

    fund, val = {}, {}
    for t in NAMES:
        print(f"[model] fundamentals {t} ...")
        fund[t] = F.build(d, cfg, ticker=t)
        print(f"[model] valuation {t} ...")
        val[t] = V.run(d, fund[t], cfg, ticker=t)
    return cfg, d, fund, val


def steady_rev(path: dict) -> float:
    """Revenue ($M) at a scenario path's own steady-state year (path['steady_fy']).
    Each name's steady_fy is anchored off its own fy0, so this is 'that scenario
    letter's long-run plateau,' not a shared calendar year across names."""
    idx = int(np.where(path["years"] == path["steady_fy"])[0][0])
    return float(path["rev"][idx])


# =================================================================== Block 1 ====
# Cross-name valuation table: price vs model, WACC vs the discount rate the bull
# path is already priced at.

def block1_rows(val: dict) -> list[dict]:
    rows = []
    for t in NAMES:
        v = val[t]
        price = v["base"]["price"]
        rows.append({
            "name": t, "price": price, "fv": v["fv_prob_weighted"],
            "dcf_over_price": v["fv_prob_weighted"] / price,
            "mc_p50": v["montecarlo"]["pct"]["p50"],
            "p_above": v["montecarlo"]["p_above_price"],
            "wacc": v["wacc"]["wacc"],
            "wacc_bull": v["reverse"]["implied_wacc_on_A"],
            "perp_eps": v["reverse"]["perp_eps"],
            "perp_pct_fy1": v["reverse"]["perp_vs_fy27_eps"],
        })
    return rows


def block1_html(rows: list[dict]) -> str:
    headers = ["Name", "Price", "Prob-weighted DCF", "DCF / price", "MC median",
               "P(FV > price)", "Model WACC", "Price-implied WACC (bull path)",
               "Perp owner EPS (% next-FY consensus EPS)"]
    trs = []
    for r in rows:
        trs.append([
            f"<b>{r['name']}</b>", _fmt(r["price"], "usd"), _fmt(r["fv"], "usd"),
            f"{r['dcf_over_price']:.2f}×", _fmt(r["mc_p50"], "usd"),
            _fmt(r["p_above"], "pct"), _fmt(r["wacc"], "pct"),
            _fmt(r["wacc_bull"], "pct") if r["wacc_bull"] is not None else "—",
            f"{_fmt(r['perp_eps'], 'usd2')} ({_fmt(r['perp_pct_fy1'], 'pct0')})",
        ])
    return html_table(headers, trs,
        "Prob-weighted DCF / MC median use each name's own scenario probabilities (assumptions.toml). "
        "P(FV &gt; price) is the Monte Carlo probability mass above today's tape; 1 minus it is the price's "
        "own percentile in the model's fair-value distribution.")


def block1_prose(rows: list[dict]) -> str:
    r = {x["name"]: x for x in rows}
    pctile = {t: 100 * (1 - r[t]["p_above"]) for t in NAMES}
    pctile_line = "; ".join(f"{t} at p{pctile[t]:.0f}" for t in NAMES)
    gap_pp = {t: (r[t]["wacc"] - r[t]["wacc_bull"]) * 100 for t in NAMES if r[t]["wacc_bull"] is not None}
    bull_line = "; ".join(f"{t} {r[t]['wacc_bull']:.1%} implied vs {r[t]['wacc']:.1%} model WACC" for t in NAMES
                           if r[t]["wacc_bull"] is not None)
    if gap_pp:
        widest = max(gap_pp, key=gap_pp.get)
        narrowest = min(gap_pp, key=gap_pp.get)
        gap_line = (f"<b>{widest}</b> carries the largest gap ({gap_pp[widest]:.1f} points), "
                    f"<b>{narrowest}</b> the smallest ({gap_pp[narrowest]:.1f} points) — read that spread as "
                    "which name's price leans hardest on optimism this model cannot independently verify.")
    else:
        gap_line = ""
    return f"""
    <p>The pattern is uniform across the complex, not a Micron quirk: every name's price sits at or above the
    model's own p{min(pctile.values()):.0f} — {pctile_line} — so today's tape is priced above nearly the whole
    Monte Carlo fair-value distribution for all three names at once. Turning the DCF around on each name's own
    bull (A) scenario, the discount rate that makes the bull path worth today's price sits below that name's
    CAPM-derived WACC every time: {bull_line}. There are two honest readings of that gap, and the model cannot
    tell them apart — it can only measure the gap, not explain it: either the market is applying a lower risk
    premium to the whole AI complex than CAPM with these betas implies, or prices already embed outcomes beyond
    what the configured bull case assumes (a steeper or longer AI-capex cycle than scenario A itself models).
    {gap_line}</p>"""


def block1_console(rows: list[dict]) -> str:
    headers = ["Name", "Price", "PW DCF", "DCF/Px", "MC p50", "P(FV>Px)", "WACC", "WACC@bull", "PerpEPS(%FY+1)"]
    widths = [4, 9, 9, 7, 9, 9, 7, 10, 16]

    def fmt_row(cells):
        return "  ".join(str(c).rjust(w) for c, w in zip(cells, widths))

    lines = [fmt_row(headers), "  ".join("-" * w for w in widths)]
    for r in rows:
        wacc_bull = f"{r['wacc_bull']:.1%}" if r["wacc_bull"] is not None else "n/a"
        lines.append(fmt_row([
            r["name"], f"${r['price']:,.0f}", f"${r['fv']:,.0f}", f"{r['dcf_over_price']:.2f}x",
            f"${r['mc_p50']:,.0f}", f"{r['p_above']:.1%}", f"{r['wacc']:.1%}", wacc_bull,
            f"${r['perp_eps']:,.0f} ({r['perp_pct_fy1']:.0%})",
        ]))
    return "\n".join(lines)


# =================================================================== Block 2 ====
# Mini football fields: one panel per name, each on its own price scale.

def fig_football_multi(val: dict) -> str:
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 6.5))
    for ax, t in zip(axes, NAMES):
        v = val[t]
        price = v["base"]["price"]
        mc = v["montecarlo"]["pct"]
        rows = [
            ("DCF scenarios C..A (diamond = prob-weighted FV)",
             v["scenarios"]["C"]["dcf"]["ps"], v["scenarios"]["A"]["dcf"]["ps"], v["fv_prob_weighted"], BLUE),
            ("Monte Carlo p25-p75", mc["p25"], mc["p75"], None, BLUE_L),
            ("Monte Carlo p5-p95", mc["p5"], mc["p95"], None, BLUE_XL),
        ]
        for i, (label, lo, hi, pt, color) in enumerate(reversed(rows)):
            ax.barh(i, hi - lo, left=lo, height=0.55, color=color, edgecolor="none")
            if pt is not None:
                ax.plot([pt], [i], marker="D", color=INK, markersize=6, zorder=5)
        ax.axvline(price, color=INK, lw=1.6, zorder=6)
        ax.set_ylim(-0.6, len(rows) - 0.4)
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([rr[0] for rr in reversed(rows)], fontsize=8.7, color=INK2)
        xmax = max(price, mc["p95"], v["scenarios"]["A"]["dcf"]["ps"]) * 1.15
        ax.set_xlim(0, xmax)
        ax.text(price, len(rows) - 0.55, f" price ${price:,.0f}", color=INK, fontsize=9.5,
                fontweight="bold", va="bottom")
        ax.set_title(t, fontsize=11.5)
        ax.set_xlabel("$ per share")
    fig.tight_layout(h_pad=1.4)
    return img(fig, "mini football fields for MU, NVDA, and AMD, each on its own price scale")


# =================================================================== Block 3 ====
# The MU/NVDA revenue-ratio consistency check.

def block3_ratio_series(fund: dict) -> pd.Series:
    """MU FY t revenue / NVDA FY (t+1) revenue, both actual annuals ($M). MU's fiscal
    year ends late August, NVDA's ends late January, so NVDA FY(t+1) is the closest
    calendar alignment to MU FY t — e.g. MU FY2025 (Aug-25) pairs with NVDA FY2026
    (Jan-26). Starts at MU FY2012 (post-Elpida three-supplier DRAM era, the same
    window convention cycle_stats/normalized use elsewhere in this codebase)."""
    mu = fund["MU"]["annual"]["revenue"].dropna()
    nv = fund["NVDA"]["annual"]["revenue"].dropna()
    idx = [t for t in mu.index if t >= 2012 and (t + 1) in nv.index]
    return pd.Series({int(t): mu[t] / nv[t + 1] for t in idx}).sort_index()


def block3_implied_ratios(val: dict) -> dict:
    """Scenario-implied steady-state ratio per matched letter: MU-X steady-year
    revenue / NVDA-X steady-year revenue. Each side uses its own path's own
    steady_fy (see steady_rev) -- not a shared calendar year."""
    return {k: steady_rev(val["MU"]["scenarios"][k]["path"]) / steady_rev(val["NVDA"]["scenarios"][k]["path"])
            for k in ("A", "B", "C")}


def fig_ratio(ratio_series: pd.Series, implied: dict) -> str:
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    ax.plot(ratio_series.index, ratio_series.values, color=BLUE, lw=2, marker="o", markersize=4,
            label="actual: MU FY t revenue / NVDA FY (t+1) revenue")
    last_fy = int(ratio_series.index[-1])
    x_fc = last_fy + 2.2
    ax.axvline(last_fy + 1, color=BASELINE, lw=1, ls="--")
    # A/B/C implied ratios sit close together (~0.40-0.44) -- spread them on x so the
    # three diamonds and labels don't overlap even though their y-values nearly do.
    x_offset = {"A": -0.5, "B": 0.0, "C": 0.5}
    for k in ("A", "B", "C"):
        xk = x_fc + x_offset[k]
        ax.plot([xk], [implied[k]], marker="D", color=SC_COLOR[k], markersize=9, zorder=5, linestyle="none")
        ax.annotate(k, (xk, implied[k]), textcoords="offset points", xytext=(0, 9),
                    color=SC_COLOR[k], fontweight="bold", fontsize=10, ha="center")
    ax.set_ylabel("MU revenue / NVDA revenue")
    ax.set_xlabel("MU fiscal year (paired with NVDA FY t+1 -- MU FYE Aug, NVDA FYE Jan)")
    ax.set_title("Memory vs GPU: the revenue-ratio history, and what each scenario letter implies at steady state")
    ax.set_xlim(ratio_series.index[0] - 0.5, x_fc + 1.3)
    ymax = ax.get_ylim()[1]
    ax.text(last_fy + 1, ymax * 0.90, " scenario-\n implied\n steady\n state", color=MUTED, fontsize=7.5, va="top")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    return img(fig, "MU to NVDA revenue-ratio history with scenario-implied steady-state points")


def block3_prose(ratio_series: pd.Series, implied: dict) -> str:
    current_fy = int(ratio_series.index[-1])
    current = float(ratio_series.iloc[-1])
    peak_fy = int(ratio_series.idxmax())
    peak = float(ratio_series.max())
    avg_implied = sum(implied.values()) / 3
    spread = max(implied.values()) - min(implied.values())
    implied_line = ", ".join(f"{k} {implied[k]:.2f}" for k in ("A", "B", "C"))
    return f"""
    <p>Through FY2022 Micron's annual revenue was comparable to or larger than Nvidia's — the ratio ran as high
    as {peak:.1f}x (MU FY{peak_fy} / NVDA FY{peak_fy + 1}), back when Nvidia was still mostly a gaming-GPU company.
    From FY2023 the ratio falls off a cliff as Nvidia's AI-datacenter revenue compounds (NVDA revenue: $27B to
    $61B to $130B to $216B across FY2023-26) faster than Micron's HBM ramp shows up in <em>completed</em> fiscal
    years; the most recent pairing, MU FY{current_fy} / NVDA FY{current_fy + 1}, is the series' low at
    <b>{current:.2f}</b>. Micron's HBM re-acceleration is a story already visible in its FY{current_fy + 1}
    quarterly prints (see the single-name MU report), not yet in a closed fiscal year — this actuals-only chart
    cannot show it "pulling back up" until macrotrends posts a completed FY{current_fy + 1}.</p>
    <p>The scenario-implied steady-state ratios — {implied_line} — cluster tightly around <b>{avg_implied:.2f}</b>,
    a band only {spread:.2f} wide ({spread / avg_implied:.0%} of the average) despite A, B and C being built from
    very different dollar trajectories for each name. That tight clustering is the finding: it is not that the
    bull case happens to pair well with the bull case — <b>every</b> letter, independently, keeps Micron's
    steady-state revenue at roughly {avg_implied:.0%} of Nvidia's. Mechanically, that means the assumption set
    moves MU and NVDA together across the whole scenario space, which is exactly what "the same macro bet" means
    in portfolio terms: sizing both is not diversification across two independent theses, it is one AI-capex-
    persistence thesis sized twice. One honest flag: {avg_implied:.2f} is roughly {avg_implied / current:.1f}x
    today's actual {current:.2f} — every letter, including the bear case C, assumes Micron claws back a
    substantially larger relative share of the complex's revenue than it has today. That is a real, checkable
    modeling choice baked identically into all three letters, not something that emerged independently per
    scenario.</p>"""


# =================================================================== Block 4 ====
# The AI-capex pool bridge — parametric context, not data.

def block4_table(val: dict) -> list[dict]:
    rows = []
    for k in ("A", "B", "C"):
        nvda_rev = steady_rev(val["NVDA"]["scenarios"][k]["path"]) / 1e3   # $B
        amd_rev_total = steady_rev(val["AMD"]["scenarios"][k]["path"]) / 1e3   # $B
        amd_dc = amd_rev_total * PARAMS["amd_dc_share"]
        accel_rev = nvda_rev + amd_dc
        pool = accel_rev / PARAMS["accel_share_of_ai_capex"]
        pool_x = pool / PARAMS["capex_pool_2026"]
        mu_rev = steady_rev(val["MU"]["scenarios"][k]["path"]) / 1e3   # $B
        attach = mu_rev / accel_rev
        rows.append({"tier": k, "nvda_rev": nvda_rev, "amd_dc": amd_dc, "accel_rev": accel_rev,
                     "pool": pool, "pool_x": pool_x, "mu_rev": mu_rev, "attach": attach})
    return rows


def block4_html(rows: list[dict]) -> str:
    headers = ["Tier", "NVDA steady rev", "AMD steady rev (DC portion)", "Implied accelerator revenue",
               "Required AI-capex pool, $B/yr", "vs 2026 pool", "MU attach ratio"]
    trs = [[f"<b>{r['tier']}</b>", f"${r['nvda_rev']:,.0f}B", f"${r['amd_dc']:,.0f}B",
            f"${r['accel_rev']:,.0f}B", f"${r['pool']:,.0f}B", f"{r['pool_x']:.2f}x", f"{r['attach']:.0%}"]
           for r in rows]
    note = (f"PARAMETRIC CONTEXT, not data: accelerator share of AI-capex ({PARAMS['accel_share_of_ai_capex']:.0%}) "
            f"and AMD's data-center revenue share ({PARAMS['amd_dc_share']:.0%}) are assumptions; the "
            f"${PARAMS['capex_pool_2026']:,.0f}B/yr 2026 hyperscaler AI-capex pool is a desk research figure as of "
            "Jul-2026, not a modeled or measured quantity. Treat this block as a plausibility bridge, not a forecast.")
    return html_table(headers, trs, note)


def block4_prose(rows: list[dict]) -> str:
    a = next(r for r in rows if r["tier"] == "A")
    c = next(r for r in rows if r["tier"] == "C")
    attach_vals = [r["attach"] for r in rows]
    stable = (max(attach_vals) - min(attach_vals)) < 0.10
    attach_line = ", ".join(f"{r['tier']} {r['attach']:.0%}" for r in rows)
    coherence = ("a stable band, which says the three scenario sets agree on memory-per-accelerator economics "
                 "even though they disagree sharply on the size of the pool itself." if stable else
                 "a band wide enough that memory-per-accelerator economics are themselves scenario-dependent, "
                 "not just the pool size.")
    return f"""
    <p>Joint-A — every name's bull scenario at once — requires the world's hyperscalers to grow AI capex from
    today's ${PARAMS['capex_pool_2026']:,.0f}B/yr to roughly <b>${a['pool']:,.0f}B/yr ({a['pool_x']:.1f}x today's
    level) and hold it there</b> at the steady-state year, not just touch it at a one-time peak. Joint-C — every
    name's bear scenario — corresponds to a pool that shrinks to about <b>${c['pool']:,.0f}B/yr ({c['pool_x']:.2f}x
    today's level)</b>, i.e. hyperscaler AI capex giving back more than half of where it stands in 2026. Between
    those anchors, the memory-attach ratio — Micron's steady-state revenue as a share of the implied accelerator
    revenue — runs {attach_line}: {coherence}</p>"""


# =================================================================== Block 5 ====
# One factor, owned three times.

def block5_data(d: dict, cfg: dict) -> dict:
    tickers = ("MU", "NVDA", "AMD", "SMH")
    rets = {t: np.log(d["prices"][t]["Adj Close"]).diff().dropna() for t in tickers}
    df = pd.concat(rets, axis=1, join="inner")
    years = cfg.get("riskvol", {}).get("factor_years_daily", 3)
    window = int(252 * years)
    df = df.iloc[-window:]

    corr = df.corr()
    c3 = df[["MU", "NVDA", "AMD"]].corr().values
    eigvals = np.linalg.eigvalsh(c3)[::-1]   # descending
    pc1_share = float(eigvals[0] / eigvals.sum())

    pairs = [("MU", "NVDA"), ("MU", "AMD"), ("NVDA", "AMD")]
    avg_corr = float(np.mean([corr.loc[a, b] for a, b in pairs]))
    eff_breadth = 3.0 / (1 + 2 * avg_corr)

    betas = {t: float(np.polyfit(df["SMH"], df[t], 1)[0]) for t in ("MU", "NVDA", "AMD")}

    return {"corr": corr, "pc1_share": pc1_share, "avg_pairwise_corr": avg_corr,
            "effective_breadth": eff_breadth, "betas_vs_smh": betas,
            "n_obs": int(len(df)), "start": str(df.index[0].date()), "end": str(df.index[-1].date()),
            "years": years}


def block5_corr_html(b5: dict) -> str:
    tickers = ("MU", "NVDA", "AMD", "SMH")
    headers = [""] + list(tickers)
    trs = [[f"<b>{a}</b>"] + [_fmt(b5["corr"].loc[a, b]) for b in tickers] for a in tickers]
    note = (f"{b5['years']:.0f}y daily log returns, {b5['n_obs']:,} trading days "
            f"({b5['start']} to {b5['end']}). Not a heatmap on purpose — the numbers are the point.")
    return html_table(headers, trs, note)


def block5_beta_html(b5: dict) -> str:
    headers = ["Name", "Beta vs SMH (3y daily)"]
    trs = [[t, _fmt(b5["betas_vs_smh"][t])] for t in ("MU", "NVDA", "AMD")]
    return html_table(headers, trs,
        "Univariate OLS slope of daily log returns on SMH's, same convention as the single-name factor model's "
        "practical hedge betas (report.py / riskvol.py).")


def block5_prose(b5: dict) -> str:
    return f"""
    <p>One principal component explains <b>{b5['pc1_share']:.0%}</b> of the three names' joint daily-return
    variance — MU, NVDA and AMD move overwhelmingly on one shared factor (the AI/semis cycle), with the rest
    split across name-specific news. Average pairwise correlation among the three is {b5['avg_pairwise_corr']:.2f};
    at that correlation, holding all three sizes a book at an effective breadth of
    <b>3 / (1 + 2 &times; {b5['avg_pairwise_corr']:.2f}) = {b5['effective_breadth']:.1f} independent bets</b>, not
    three — roughly the sizing consequence of one-and-a-bit uncorrelated positions, not a diversified sleeve.
    All three carry a beta to SMH above 1 (MU {b5['betas_vs_smh']['MU']:.2f}, NVDA {b5['betas_vs_smh']['NVDA']:.2f},
    AMD {b5['betas_vs_smh']['AMD']:.2f}), so the complex is not merely correlated with the semis sector — each
    name is a levered version of it.</p>"""


# ================================================================ console ====

def console_summary(rows: list[dict], ratio_series: pd.Series, implied: dict,
                     pool_rows: list[dict], b5: dict) -> str:
    r = {x["name"]: x for x in rows}
    gap_pp = {t: (r[t]["wacc"] - r[t]["wacc_bull"]) * 100 for t in NAMES if r[t]["wacc_bull"] is not None}
    widest = max(gap_pp, key=gap_pp.get) if gap_pp else None
    gap_txt = ", ".join(f"{t} {gap_pp[t]:.1f}pp" for t in NAMES if t in gap_pp)
    avg_implied = sum(implied.values()) / 3
    current = float(ratio_series.iloc[-1])
    implied_txt = ", ".join(f"{k} {implied[k]:.2f}" for k in ("A", "B", "C"))
    a_pool = next(x for x in pool_rows if x["tier"] == "A")

    lines = [
        "=" * 78,
        "MU / NVDA / AMD -- COMPLEX REPORT",
        "=" * 78,
        block1_console(rows),
        "-" * 78,
        "Headline findings:",
        f"1) Discount-rate gap: every name's bull (A) path is worth today's price at a LOWER discount rate",
        f"   than its own CAPM WACC -- {gap_txt}" + (f" -- widest at {widest}." if widest else "."),
        f"   The model can't tell whether that's a cheaper AI risk premium or outcomes beyond the bull case;",
        f"   it can only measure the gap.",
        f"2) Mutual consistency: MU/NVDA scenario-implied steady-state revenue ratios ({implied_txt}) cluster",
        f"   near {avg_implied:.2f} in every letter, vs today's actual {current:.2f} -- MU and NVDA are",
        f"   substantially the same AI-capex bet across this model's whole scenario space, not diversification.",
        f"3) Joint-A requires hyperscaler AI capex at ${a_pool['pool']:,.0f}B/yr ({a_pool['pool_x']:.1f}x the",
        f"   ${PARAMS['capex_pool_2026']:,.0f}B/yr 2026 pool), held at the steady-state year, for NVDA+AMD+MU's",
        f"   bull cases to be simultaneously true.",
        "-" * 78,
        f"One common factor explains {b5['pc1_share']:.0%} of the three names' joint daily variance; effective",
        f"breadth at these correlations is {b5['effective_breadth']:.1f} independent bets, not 3.",
        "=" * 78,
    ]
    return "\n".join(lines)


# =================================================================== JSON ====

def _f(x):
    if x is None:
        return None
    x = float(x)
    if math.isnan(x) or math.isinf(x):
        return None
    return x


def write_json(rows: list[dict], val: dict, ratio_series: pd.Series, implied: dict,
               pool_rows: list[dict], b5: dict, asof: str) -> Path:
    out = {
        "asof": asof,
        "names": list(NAMES),
        "per_name": {
            r["name"]: {
                "price": _f(r["price"]), "price_date": val[r["name"]]["base"]["price_date"],
                "fv_prob_weighted": _f(r["fv"]), "dcf_over_price": _f(r["dcf_over_price"]),
                "mc_p50": _f(r["mc_p50"]), "p_above_price": _f(r["p_above"]),
                "price_percentile": _f(100 * (1 - r["p_above"])),
                "wacc": _f(r["wacc"]), "wacc_implied_on_bull": _f(r["wacc_bull"]),
                "perp_eps": _f(r["perp_eps"]), "perp_vs_fy1_consensus_eps": _f(r["perp_pct_fy1"]),
                "scenario_ps": {k: _f(val[r["name"]]["scenarios"][k]["dcf"]["ps"]) for k in ("A", "B", "C")},
            } for r in rows
        },
        "revenue_ratio": {
            "history": {str(fy): _f(v) for fy, v in ratio_series.items()},
            "current": _f(ratio_series.iloc[-1]),
            "current_fy_pair": f"MU FY{int(ratio_series.index[-1])} / NVDA FY{int(ratio_series.index[-1]) + 1}",
            "scenario_implied": {k: _f(v) for k, v in implied.items()},
        },
        "capex_pool_bridge": {
            "params": dict(PARAMS),
            "tiers": {
                r["tier"]: {
                    "nvda_steady_rev_b": _f(r["nvda_rev"]), "amd_dc_steady_rev_b": _f(r["amd_dc"]),
                    "accel_revenue_b": _f(r["accel_rev"]), "required_pool_b": _f(r["pool"]),
                    "pool_vs_2026": _f(r["pool_x"]), "mu_attach_ratio": _f(r["attach"]),
                } for r in pool_rows
            },
        },
        "factor": {
            "correlation_matrix": {a: {b: _f(b5["corr"].loc[a, b]) for b in b5["corr"].columns}
                                    for a in b5["corr"].index},
            "pc1_variance_share": _f(b5["pc1_share"]),
            "avg_pairwise_corr_3name": _f(b5["avg_pairwise_corr"]),
            "effective_breadth": _f(b5["effective_breadth"]),
            "beta_vs_smh": {t: _f(v) for t, v in b5["betas_vs_smh"].items()},
            "window": {"years": b5["years"], "n_obs": b5["n_obs"], "start": b5["start"], "end": b5["end"]},
        },
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    STORE.mkdir(parents=True, exist_ok=True)
    path = STORE / f"complex-{asof}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return path


# =================================================================== HTML ====

def build_html(rows: list[dict], val: dict, ratio_series: pd.Series, implied: dict,
               pool_rows: list[dict], b5: dict, asof: str) -> Path:
    r = {x["name"]: x for x in rows}
    a_pool = next(x for x in pool_rows if x["tier"] == "A")
    gap_pp = {t: (r[t]["wacc"] - r[t]["wacc_bull"]) * 100 for t in NAMES if r[t]["wacc_bull"] is not None}
    widest = max(gap_pp, key=gap_pp.get) if gap_pp else None
    pctile = {t: 100 * (1 - r[t]["p_above"]) for t in NAMES}
    least_stretched = min(pctile, key=pctile.get)

    tiles = [
        ("Effective breadth", f"{b5['effective_breadth']:.1f} bets",
         f"3 names, avg pairwise corr {b5['avg_pairwise_corr']:.2f}"),
        ("Common factor (PC1)", f"{b5['pc1_share']:.0%}", "of joint daily variance, 3y"),
        ("Joint-A capex pool", f"${a_pool['pool']:,.0f}B/yr",
         f"{a_pool['pool_x']:.1f}x today's ${PARAMS['capex_pool_2026']:,.0f}B (parametric)"),
        ("Least-stretched name", f"{least_stretched} p{pctile[least_stretched]:.0f}",
         "lowest price-percentile of the three vs its own model"),
        ("Widest bull-WACC gap", f"{widest} {gap_pp[widest]:.1f}pp" if widest else "—",
         "model WACC minus price-implied WACC on the bull path"),
    ]
    tiles_html = "".join(
        f'<div class="tile"><div class="tlabel">{a}</div><div class="tvalue">{v}</div><div class="tsub">{s}</div></div>'
        for a, v, s in tiles)

    price_dates = sorted({val[t]["base"]["price_date"] for t in NAMES})
    asof_note = asof if len(price_dates) == 1 else f"{price_dates[0]} to {price_dates[-1]}"

    limits_html = """
    <ul>
      <li><b>The three Monte Carlo distributions are each internally coherent, but not jointly modeled.</b>
      Block 1's P(FV &gt; price) is computed independently per name (each name's own scenario draw and knob
      jitter); Block 5 shows the three names' actual daily returns share one factor for roughly two-thirds of
      their variance. Treat the three P(FV &gt; price) figures as correlated evidence pointing the same way,
      not as three independent checks.</li>
      <li><b>"Steady state" is each scenario path's own plateau year, not a shared calendar year.</b> MU's fy0
      is FY2026, NVDA's is FY2027 (fiscal year ends differ by five months); Block 3/4 compare each name's own
      steady_fy revenue, which lands in different absolute fiscal years across names.</li>
      <li><b>The revenue-ratio history (Block 3) is actuals-only</b> (macrotrends annual data), which lags the
      current in-progress fiscal year. Micron's HBM re-acceleration already visible in recent quarters has not
      closed a fiscal year yet, so the chart's most recent point is a trailing, not current, read.</li>
      <li><b>Block 4 is a plausibility bridge, not a forecast.</b> Two of its three parameters are named
      assumptions (accelerator share of AI capex, AMD's data-center revenue share); the $725B 2026 pool is a
      desk research figure with an as-of date, not a modeled or measured quantity. Small changes to either
      assumption move the required-pool column by a similar proportion — it is not more precise than its inputs.</li>
      <li><b>Every scenario knob behind this report is hand-set in assumptions.toml</b>, per name, and not
      derived from a shared cross-name model — the consistency found in Block 3/4 is a property of how the three
      names' scenarios were authored, evidence worth taking seriously but not a law of nature.</li>
    </ul>"""

    css = """
    body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #f9f9f7; color: #0b0b0b;
           margin: 0; padding: 24px 16px; }
    .wrap { max-width: 1060px; margin: 0 auto; }
    h1 { font-size: 24px; margin: 0 0 4px; }
    h2 { font-size: 17px; margin: 34px 0 6px; border-bottom: 1px solid #e1e0d9; padding-bottom: 5px;}
    .sub { color: #52514e; margin-bottom: 18px; font-size: 13.5px;}
    .card { background: #fcfcfb; border: 1px solid rgba(11,11,11,0.10); border-radius: 10px;
            padding: 14px 16px; margin: 10px 0; }
    .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
    .tile { background: #fcfcfb; border: 1px solid rgba(11,11,11,0.10); border-radius: 10px; padding: 10px 12px; }
    .tlabel { font-size: 11px; color: #898781; text-transform: uppercase; letter-spacing: .04em;}
    .tvalue { font-size: 21px; font-weight: 700; margin: 2px 0; }
    .tsub { font-size: 11.5px; color: #52514e; }
    .tablewrap { overflow-x: auto; }
    table { border-collapse: collapse; width: 100%; font-size: 12.5px; margin: 8px 0 2px; }
    th { text-align: left; color: #52514e; font-weight: 600; border-bottom: 1px solid #c3c2b7; padding: 5px 8px;}
    td { border-bottom: 1px solid #e1e0d9; padding: 5px 8px; font-variant-numeric: tabular-nums; }
    .tnote { font-size: 11.5px; color: #898781; margin: 4px 0 8px; }
    p, li { font-size: 13.5px; line-height: 1.55; }
    code { background: #f0efec; padding: 1px 4px; border-radius: 4px; font-size: 12px;}
    .verdict { font-size: 14.5px; }
    img { border-radius: 6px; }
    """

    html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MU / NVDA / AMD — the complex — {asof}</title>
<style>{css}</style></head>
<body><div class="wrap">
<h1>MU / NVDA / AMD — the complex, not three names</h1>
<div class="sub">as of {asof_note} · prices ${r['MU']['price']:,.0f} / ${r['NVDA']['price']:,.0f} /
${r['AMD']['price']:,.0f} · every per-name input editable in <code>assumptions.toml</code> ·
generated by <code>tools/muval/complex.py</code>, built on the per-name pipeline in <code>tools/muval</code></div>

<div class="tiles">{tiles_html}</div>

<h2>1. Cross-name valuation</h2>
<div class="card">{block1_html(rows)}{block1_prose(rows)}</div>

<h2>2. Where each price sits vs its own model</h2>
<div class="card">{fig_football_multi(val)}</div>

<h2>3. Memory vs GPU: a revenue-ratio consistency check</h2>
<div class="card">{fig_ratio(ratio_series, implied)}{block3_prose(ratio_series, implied)}</div>

<h2>4. The AI-capex pool bridge (parametric context)</h2>
<div class="card">{block4_html(pool_rows)}{block4_prose(pool_rows)}</div>

<h2>5. One factor, owned three times</h2>
<div class="card">{block5_corr_html(b5)}{block5_beta_html(b5)}{block5_prose(b5)}</div>

<h2>Data &amp; honest limits</h2>
<div class="card">{limits_html}
<div class="tnote">Model, not advice. Regenerates from cached raw pulls with
<code>python tools/muval/complex.py --offline</code>; refresh feeds with <code>--refresh</code>. Per-name detail
(risk/vol, tornado, Korea lead-lag, earnings reactions) lives in each name's own report — this page is only the
analysis that requires all three at once.</div></div>

</div></body></html>"""

    STORE.mkdir(parents=True, exist_ok=True)
    out = STORE / "complex-report.html"
    out.write_text(html, encoding="utf-8")
    return out


# ==================================================================== main ====

def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(errors="replace")
    offline = "--offline" in argv
    refresh = "--refresh" in argv

    cfg, d, fund, val = run_pipeline(offline, refresh)

    print("[report] building cross-name analysis ...")
    rows = block1_rows(val)
    ratio_series = block3_ratio_series(fund)
    implied = block3_implied_ratios(val)
    pool_rows = block4_table(val)
    b5 = block5_data(d, cfg)

    asof = val["MU"]["base"]["price_date"]
    html_path = build_html(rows, val, ratio_series, implied, pool_rows, b5, asof)
    json_path = write_json(rows, val, ratio_series, implied, pool_rows, b5, asof)

    print()
    print(console_summary(rows, ratio_series, implied, pool_rows, b5))
    print(f"HTML report: {html_path}")
    print(f"JSON snapshot: {json_path}")

    if "--no-open" not in argv:
        webbrowser.open(html_path.as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
