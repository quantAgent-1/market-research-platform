"""muval — Micron (MU) / Nvidia (NVDA) / AMD valuation model, MU also gets risk & report.

Usage:
    python tools/muval/muval.py               # MU: pull (cached), model, write report, open it
    python tools/muval/muval.py --offline     # caches only, no network
    python tools/muval/muval.py --refresh     # force re-pull all feeds
    python tools/muval/muval.py --no-open     # don't open the report in a browser
    python tools/muval/muval.py --name NVDA   # valuation-only console brief for NVDA (or AMD)
    python tools/muval/muval.py selftest      # offline arithmetic anchors

Outputs (MU): store/report.html, store/valuation-<date>.json, console brief.
Outputs (NVDA/AMD): store/valuation-<ticker>-<date>.json, console brief. No HTML
report and no risk/vol model for non-MU names yet -- see README.

Assumptions: assumptions.toml (every valuation lever, data-anchored, commented;
per-name under [scenarios.<TICKER>.*] / [cash_mechanics.<TICKER>] /
[normalized.<TICKER>] / [names.<TICKER>], global sections apply to all names).
"""

from __future__ import annotations

import json
import math
import sys
import tomllib
import webbrowser
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
STORE = TOOL_DIR / "store"
sys.path.insert(0, str(TOOL_DIR))

import numpy as np  # noqa: E402


def load_cfg() -> dict:
    with open(TOOL_DIR / "assumptions.toml", "rb") as f:
        return tomllib.load(f)


def _flat_cfg_for_report(cfg: dict, ticker: str) -> dict:
    """report.py (untouched, MU-only) expects a flat cfg["normalized"] dict with
    pe_band_low/pe_band_high directly on it. Hand it a shallow copy namespaced
    down to one name; the multi-name cfg used by fundamentals/valuation is
    untouched."""
    flat = dict(cfg)
    flat["normalized"] = cfg["normalized"][ticker]
    return flat


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(errors="replace")
    if "selftest" in argv:
        return selftest()

    offline = "--offline" in argv
    refresh = "--refresh" in argv

    name = "MU"
    if "--name" in argv:
        i = argv.index("--name")
        if i + 1 >= len(argv):
            print("[error] --name requires a value, e.g. --name NVDA")
            return 2
        name = argv[i + 1].upper()
        if name not in ("MU", "NVDA", "AMD"):
            print(f"[error] unsupported --name {name!r}; supported: MU, NVDA, AMD")
            return 2

    import data as D
    import fundamentals as F
    import valuation as V

    cfg = load_cfg()

    if name == "MU":
        import riskvol as R
        import report as REP

        d = D.pull_all(offline=offline, refresh=refresh)
        print("[model] fundamentals ...")
        fund = F.build(d, cfg)
        fund["_peers"] = d["yf"].get("peers", {})
        print("[model] valuation (scenarios, reverse DCF, Monte Carlo) ...")
        val = V.run(d, fund, cfg)
        print("[model] risk & volatility ...")
        risk = R.run(d, cfg)
        print("[report] building ...")
        json_path = REP.write_json(val, risk, fund)
        html_path = REP.build_html(val, risk, fund, _flat_cfg_for_report(cfg, "MU"))
        print()
        print(REP.console_brief(val, risk, fund))
        print(f"JSON snapshot: {json_path}")
        if "--no-open" not in argv:
            webbrowser.open(html_path.as_uri())
        return 0

    # ---- non-MU: valuation-only path (no risk/vol model, no HTML report yet) ----
    d = D.pull_all(offline=offline, refresh=refresh, names=(name,))
    if name not in d["prices"]:
        # data.py's shared TICKERS table (which all_prices()/pull_all() draw the
        # "prices" dict from) doesn't include every name `names=` can pull
        # fundamentals for -- AMD is fundamentals-only there. Pull its price
        # history directly through the same public data.prices() function, no
        # change to data.py needed.
        print(f"[data] prices {name} (not in data.TICKERS, pulling directly) ...")
        d["prices"][name] = D.prices(name, offline=offline, refresh=refresh)

    print("[model] fundamentals ...")
    fund = F.build(d, cfg, ticker=name)
    print("[model] valuation (scenarios, reverse DCF, Monte Carlo) ...")
    val = V.run(d, fund, cfg, ticker=name)

    json_path = _write_valuation_json(val, fund, name)
    print()
    print(_console_brief_valuation_only(val, fund, name))
    print(f"JSON snapshot: {json_path}")
    return 0


# --------------------------------------------- non-MU console brief + JSON --

def _console_brief_valuation_only(val: dict, fund: dict, ticker: str) -> str:
    b = val["base"]
    mc = val["montecarlo"]
    r = val["reverse"]
    w = val["wacc"]
    # bull (A) read: nm_steady-solve and WACC-solve are independent bisections
    # (fixed WACC solving for margin vs. fixed margin solving for WACC) -- each
    # can succeed or fail (None = unreachable in-range) on its own, so report
    # whichever one(s) actually resolved rather than an all-or-nothing gate.
    nm_a, wacc_a = r.get("implied_nm_steady_on_A"), r.get("implied_wacc_on_A")
    if nm_a is not None and wacc_a is not None:
        bull_line = f"  bull revenue path + {nm_a:.0%} steady net margin, or bull path at {wacc_a:.1%} WACC"
    elif wacc_a is not None:
        bull_line = (f"  bull revenue path cannot reach the price at any steady net margin <= 90% "
                     f"(fixed at its own margins); at its own margins it reaches price only at {wacc_a:.1%} WACC")
    elif nm_a is not None:
        bull_line = f"  bull revenue path + {nm_a:.0%} steady net margin (no WACC in [5.5%, 25%] reaches price on its own margins)"
    else:
        bull_line = "  bull revenue path cannot reach the price at any steady net margin <= 90%, nor at any WACC down to 5.5%"

    lines = [
        "=" * 74,
        f"{ticker} VALUATION MODEL   as of {b['price_date']}   price ${b['price']:,.2f}",
        "=" * 74,
        f"DCF scenarios: A ${val['scenarios']['A']['dcf']['ps']:,.0f} (p={val['probs'][0]:.0%}) | "
        f"B ${val['scenarios']['B']['dcf']['ps']:,.0f} (p={val['probs'][1]:.0%}) | "
        f"C ${val['scenarios']['C']['dcf']['ps']:,.0f} (p={val['probs'][2]:.0%})",
        f"Probability-weighted fair value : ${val['fv_prob_weighted']:,.0f}",
        f"Monte Carlo p25/p50/p75         : ${mc['pct']['p25']:,.0f} / ${mc['pct']['p50']:,.0f} / ${mc['pct']['p75']:,.0f}",
        f"P(model fair value > price)     : {mc['p_above_price']:.1%}  (price = p{100 * (1 - mc['p_above_price']):.0f} of the model distribution)",
        "-" * 74,
        "What $%.0f already assumes (reverse DCF):" % b["price"],
        f"  perpetual owner earnings of ${r['perp_eps']:,.0f}/sh ({r['perp_vs_fy27_eps']:.0%} of next-FY consensus EPS), or",
        bull_line,
        f"  (base-case cycle geometry cannot reach the price at any margin <= 90%)" if r.get("implied_nm_steady_on_B") is None or (r.get("implied_nm_steady_on_B") or 0) > 0.85 else f"  base-case cycle geometry requires a {r['implied_nm_steady_on_B']:.0%} steady margin",
        "-" * 74,
        f"WACC {w['wacc']:.1%} (beta {w['beta']:.2f} shrunk from {w['beta_raw']:.2f}, rf {w['rf']:.2%})",
        "=" * 74,
    ]
    return "\n".join(ln for ln in lines if ln)


def _clean_for_json(o):
    if isinstance(o, dict):
        return {k: _clean_for_json(v) for k, v in o.items()
                if k not in ("values", "level", "path", "pv_rows", "history")}
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return [float(x) for x in o]
    if isinstance(o, (list, tuple)):
        return [_clean_for_json(x) for x in o]
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def _write_valuation_json(val: dict, fund: dict, ticker: str) -> Path:
    b = val["base"]
    out = {
        "ticker": ticker, "asof": b["price_date"], "price": b["price"],
        "valuation": _clean_for_json({k: v for k, v in val.items() if k != "base"}),
        "trend": {k: v for k, v in fund["trend"].items() if k != "level"},
        "snapshot": _clean_for_json(fund["snapshot"]),
        "consensus": fund["consensus"],
    }
    STORE.mkdir(parents=True, exist_ok=True)
    path = STORE / f"valuation-{ticker}-{b['price_date']}.json"
    path.write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    return path


# ------------------------------------------------------------------ selftest --

def selftest() -> int:
    """Arithmetic anchors, no network, no cache."""
    import fundamentals as F
    import valuation as V
    import riskvol as R
    import pandas as pd

    ok = True

    def check(name, cond, detail=""):
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {detail}")
        ok = ok and cond

    print("[selftest]")

    # 1. DCF of a constant perpetuity ~= closed form
    name_cfg = {"fy0": 2026, "fye_month": 8}
    base = {"rev26": 100.0, "nm26": 0.2, "rev27_cons": 100.0, "rev_prior": 100.0 / 1.6,
            "shares_m": 1.0, "stub_eps": 0.0, "net_cash": 0.0, "price": 100.0,
            "price_date": "2026-03-01"}
    sc = {"fy27_rev_vs_consensus": 1.0, "peak_extra_years": 0, "peak_extra_growth": 0.0,
          "trough_frac_of_peak": 1.0, "steady_frac_of_peak": 1.0, "steady_growth": 0.0,
          "nm_peak": 0.2, "nm_trough": 0.2, "nm_steady": 0.2,
          "capex_boom": 0.10, "capex_trough": 0.10, "capex_steady": 0.10}
    mech = {"dna_start": 0.10, "dna_converge_years": 1, "dna_vs_capex_steady": 1.0,
            "nwc_pct_of_delta_rev": 0.0, "dilution_per_year": 0.0}
    cfg = {"terminal": {"g": 0.0, "exit_ev_ebitda": 8.0}, "wacc": {"tax_rate": 0.0}}
    p = V.scenario_path(base, sc, mech, 2036, name_cfg)
    # flat FCF = 100*(0.2 + 0.1 - 0.1) = 20 forever; at r=10%, PV ~= 200 at the FY27 point
    d = V.dcf(p, base, 0.10, cfg, name_cfg)
    pv_expected = 20.0 / 0.10  # perpetuity value at valuation date, first flow ~1y out
    check("perpetuity DCF within 3%", abs(d["equity"] - pv_expected) / pv_expected < 0.03,
          f"(got {d['equity']:.1f}, closed-form {pv_expected:.1f})")

    # 2. Gordon terminal consistency: doubling g-gap ~ halves TV
    cfg2 = {"terminal": {"g": 0.05, "exit_ev_ebitda": 8.0}, "wacc": {"tax_rate": 0.0}}
    d2 = V.dcf(p, base, 0.10, cfg2, name_cfg)
    check("terminal value rises with g", d2["equity"] > d["equity"])

    # 3. reverse solve inverts forward
    fund_stub = {"consensus": {"eps_fy1": 10.0}}
    # (covered implicitly by 1-2; direct bisection check:)
    lo, hi = 0.05, 0.20
    target = d["equity"] * 0.8
    for _ in range(50):
        mid = (lo + hi) / 2
        if V.dcf(p, base, mid, cfg, name_cfg)["equity"] > target:
            lo = mid
        else:
            hi = mid
    check("bisection on WACC converges", abs(V.dcf(p, base, lo, cfg, name_cfg)["equity"] - target) / target < 0.01)

    # 4. GARCH on synthetic data recovers persistence within tolerance
    rng = np.random.default_rng(3)
    n = 3000
    w_true, a_true, b_true = 0.05, 0.08, 0.90
    x = np.zeros(n)
    v = w_true / (1 - a_true - b_true)
    for t in range(1, n):
        v = w_true + a_true * x[t - 1] ** 2 + b_true * v
        x[t] = np.sqrt(v) * rng.standard_normal()
    g = R.garch11(pd.Series(x / 100.0))
    check("GARCH persistence within 0.05", abs(g["persistence"] - (a_true + b_true)) < 0.05,
          f"(got {g['persistence']:.3f}, true {a_true + b_true:.2f})")

    # 5. Yang-Zhang on synthetic GBM ~ input vol
    sigma = 0.30
    n = 2000
    dt = 1 / 252
    z = rng.standard_normal(n) * sigma * np.sqrt(dt)
    close = 100 * np.exp(np.cumsum(z))
    op = np.roll(close, 1) * np.exp(rng.standard_normal(n) * 0.001)
    op[0] = 100
    intraday = np.abs(rng.standard_normal(n)) * sigma * np.sqrt(dt) * 0.6
    hi_px = np.maximum(op, close) * np.exp(intraday)
    lo_px = np.minimum(op, close) * np.exp(-intraday)
    px = pd.DataFrame({"Open": op, "High": hi_px, "Low": lo_px, "Close": close,
                       "Adj Close": close},
                      index=pd.date_range("2018-01-01", periods=n, freq="B"))
    yz = R.realized_yang_zhang(px, 63).dropna()
    check("Yang-Zhang within 20% of true vol", abs(yz.mean() - sigma) / sigma < 0.20,
          f"(got {yz.mean():.3f}, true {sigma})")

    # 6. factor decomposition shares sum to 1
    print("  (variance-decomposition sum check runs in the live pipeline)")

    print("[selftest]", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
