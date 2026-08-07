"""muval.events -- pre-earnings cards for MU / NVDA / AMD.

For each name: when is the next print, what move do options imply for it, how does
that compare to what the name has actually done on its last ~50 earnings days, and
is the event priced rich or cheap against its own history.

Reuses the existing fetch/cache layer (data.py) and risk engine (riskvol.py) as-is;
this file adds no new data sources and does not touch assumptions.toml. Table/CSS
styling borrows report.py's html_table / _fmt / palette constants (imported, not
reimplemented) -- see build_html() below for the small, deliberately copied CSS block
(report.build_html itself is never called: no charts here, tables only).

Usage:
    python tools/muval/events.py               # cached-first (network only if a
                                                 # per-feed cache file has gone stale)
    python tools/muval/events.py --offline      # caches only, no network, ever
    python tools/muval/events.py --refresh      # force re-pull all three feeds/name

Outputs: store/events-<date>.html, store/events-<date>.json, ASCII console cards.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOL_DIR))

import pandas as pd  # noqa: E402

import data as D       # noqa: E402
import riskvol as R    # noqa: E402
import report as REP   # noqa: E402  (reused for html_table / _fmt / palette only)

NAMES = ["MU", "NVDA", "AMD"]
FULL_NAME = {"MU": "Micron", "NVDA": "Nvidia", "AMD": "AMD"}
STORE = REP.STORE


# ---------------------------------------------------------------- small utils ----

def _c(v, kind: str = "num") -> str:
    """Console-safe formatter (ASCII only -- the console is cp949)."""
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return "n/a"
    if kind == "usd2":
        return f"${v:,.2f}"
    if kind == "usdb":
        return f"${v / 1e9:,.2f}B"
    if kind == "pct":
        return f"{v:.1%}"
    if kind == "pct0":
        return f"{v:.0%}"
    if kind == "pctnum":     # already a percentage number, e.g. cboe iv30 == 38.4 means 38.4%
        return f"{v:.1f}%"
    if kind == "x":
        return f"{v:.2f}x"
    return f"{v:,.2f}"


def _fmt_usdb(v) -> str:
    """HTML billions formatter matching report._fmt's missing-value style (em-dash)."""
    if v is None:
        return REP._fmt(None)
    return REP._fmt(v / 1e9, "usd2") + "B"


def _fmt_pctnum(v) -> str:
    """HTML formatter for already-a-percentage numbers (iv30), em-dash-style missing."""
    if v is None:
        return REP._fmt(None)
    return f"{v:.1f}%"


def _ordinal(n: int) -> str:
    """1 -> '1st', 2 -> '2nd', 3 -> '3rd', 11-13 -> 'th', else 'th'."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _f(x):
    """None/NaN-safe float cast (pandas row values arrive as numpy scalars, possibly NaN)."""
    try:
        if x is None or pd.isna(x):
            return None
    except (TypeError, ValueError):
        pass
    return float(x)


def _safe(o):
    """Recursively make an object JSON-serializable: NaN/Inf -> None, numpy scalars ->
    python natives, DataFrame/Series (shouldn't appear here, but be defensive) -> None."""
    if isinstance(o, dict):
        return {k: _safe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_safe(x) for x in o]
    if isinstance(o, (pd.Series, pd.DataFrame)):
        return None
    if hasattr(o, "item") and not isinstance(o, (str, bytes)):
        try:
            o = o.item()
        except Exception:
            pass
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def _next_earnings_ts(yf: dict):
    """Soonest unreported earnings_dates entry (eps_act is None). Mirrors the exact
    selection rule riskvol.implied_view() uses internally, kept independent here so the
    header (date/EPS/revenue) still resolves even if the options feed (cboe) is empty."""
    next_earn = None
    for e in yf.get("earnings_dates", []):
        if e.get("eps_act") is None:
            d = pd.Timestamp(e["date"])
            if d >= pd.Timestamp.now() - pd.Timedelta(days=2):
                next_earn = d if next_earn is None or d < next_earn else next_earn
    return next_earn


def _extract_move(move: dict):
    """Returns (move_1sd_or_equivalent, human label, is_fallback) from an
    implied_view()["earnings_move"] dict. Key presence (not truthiness) gates the
    branch, since a legitimately-computed 0.0 event move is a valid value."""
    if not move:
        return None, "no implied move available (insufficient option data around the print)", False
    if "event_move_1sd" in move:
        label = f"bracketing {move['pre_expiry']} / {move['post_expiry']} -- {move['method']}"
        return move["event_move_1sd"], label, False
    if "implied_move_total" in move:
        label = (f"FALLBACK -- no expiry brackets the print; single-expiry straddle to "
                 f"{move['post_expiry']} ({move['dte']}d out) -- {move['method']}")
        return move["implied_move_total"], label, True
    return None, "no implied move available (unrecognized earnings_move shape)", False


# -------------------------------------------------------------------- the card ----

def build_card(name: str, offline: bool, refresh: bool) -> dict:
    px = D.prices(name, offline=offline, refresh=refresh)
    yf = D.yf_fundamentals(name, offline=offline, refresh=refresh)
    cboe = D.cboe_options(name, offline=offline, refresh=refresh)

    spot = cboe.get("spot") if cboe else None
    if spot is None:
        spot = float(px["Close"].iloc[-1])

    next_earn = _next_earnings_ts(yf)
    eps_est = ((yf.get("earnings_estimate") or {}).get("0q") or {}).get("avg")
    rev_est = ((yf.get("revenue_estimate") or {}).get("0q") or {}).get("avg")
    days_until = ((next_earn.normalize() - pd.Timestamp.now().normalize()).days
                  if next_earn is not None else None)

    iv = R.implied_view(cboe, yf)
    move = iv.get("earnings_move") or {}
    move_1sd, move_label, is_fallback = _extract_move(move)
    iv30 = _f(cboe.get("iv30"))

    r = R.log_returns(px)
    rv20_series = R.realized_cc(r, 20)
    rv20 = float(rv20_series.iloc[-1])
    rv20_hist10y = rv20_series.iloc[-int(R.ANN * 10):].dropna()
    rv20_p90 = float(rv20_hist10y.quantile(0.90)) if len(rv20_hist10y) else None
    rv20_pctile = float((rv20_hist10y < rv20).mean()) if len(rv20_hist10y) else None
    extreme_vol = bool(rv20_p90 is not None and rv20 > rv20_p90)

    earn = R.earnings_study(yf, px)
    stats = earn["stats"]
    events_df = earn["events"]

    richness = None
    hist_pctile = None
    verdict = "N/A -- missing implied move or history stats"
    median_abs = stats.get("median_abs")
    if move_1sd is not None and median_abs:
        richness = move_1sd / median_abs
        if not events_df.empty:
            hist_pctile = float((events_df["reaction"].abs() < move_1sd).mean())
        if richness < 0.8:
            verdict = "priced CHEAP vs history"
        elif richness <= 1.25:
            verdict = "in line"
        else:
            verdict = "priced RICH vs history"

    last8 = []
    if not events_df.empty:
        for _, e in events_df.tail(8).iloc[::-1].iterrows():
            last8.append({
                "date": e["date"],
                "eps_est": _f(e["eps_est"]), "eps_act": _f(e["eps_act"]),
                "surprise": _f(e["surprise"]), "gap": _f(e["gap"]),
                "reaction": _f(e["reaction"]),
            })

    span = [events_df["date"].iloc[0], events_df["date"].iloc[-1]] if not events_df.empty else [None, None]

    return {
        "name": name, "full_name": FULL_NAME.get(name, name),
        "spot": _f(spot),
        "next_earnings": str(next_earn.date()) if next_earn is not None else None,
        "days_until": int(days_until) if days_until is not None else None,
        "consensus_eps": _f(eps_est), "consensus_rev": _f(rev_est),
        "iv30": iv30, "rv20": rv20, "rv20_p90_10y": rv20_p90,
        "rv20_pctile_10y": rv20_pctile, "extreme_vol": extreme_vol,
        "implied_move_1sd": _f(move_1sd), "implied_move_label": move_label,
        "implied_move_is_fallback": is_fallback,
        "history_n": stats.get("n", 0), "history_span": span,
        "history_stats": stats, "history_last8": last8,
        "richness": richness, "pctile_of_history": hist_pctile, "verdict": verdict,
    }


# ---------------------------------------------------------------- console render ----

def render_summary(cards: list) -> str:
    headers = ["Name", "Next print", "Days", "Implied +/-1sd", "Median hist |move|", "Richness", "Verdict"]
    rows = []
    for c in cards:
        rows.append([
            c["name"],
            c["next_earnings"] or "n/a",
            str(c["days_until"]) if c["days_until"] is not None else "n/a",
            _c(c["implied_move_1sd"], "pct"),
            _c(c["history_stats"].get("median_abs"), "pct"),
            _c(c["richness"], "x") if c["richness"] is not None else "n/a",
            c["verdict"],
        ])
    widths = [max(len(h), max((len(r[i]) for r in rows), default=0)) for i, h in enumerate(headers)]
    lines = ["  ".join(h.ljust(w) for h, w in zip(headers, widths)),
             "  ".join("-" * w for w in widths)]
    for row in rows:
        lines.append("  ".join(cell.ljust(w) for cell, w in zip(row, widths)))
    return "\n".join(lines)


def render_card(c: dict) -> str:
    full = f" ({c['full_name']})" if c["full_name"] != c["name"] else ""
    L = []
    L.append("=" * 78)
    L.append(f"{c['name']}{full}".ljust(46) + f"spot {_c(c['spot'], 'usd2')}")
    L.append("-" * 78)
    days_str = f"  ({c['days_until']} days)" if c["days_until"] is not None else ""
    L.append(f"Next earnings   : {c['next_earnings'] or 'n/a'}{days_str}")
    L.append(f"Consensus EPS   : {_c(c['consensus_eps'], 'usd2')}    "
             f"Consensus revenue: {_c(c['consensus_rev'], 'usdb')}")
    L.append("-" * 78)
    fb = ("  [FALLBACK METHOD -- includes non-event baseline vol, treat as upper bound]"
          if c["implied_move_is_fallback"] else "")
    mv = _c(c["implied_move_1sd"], "pct")
    mv_str = f"+/-{mv}" if c["implied_move_1sd"] is not None else mv
    L.append(f"IMPLIED MOVE (options): {mv_str} (1sd){fb}")
    L.append(f"  via {c['implied_move_label']}")
    L.append(f"IV30                  : {_c(c['iv30'], 'pctnum')}")
    rv_flag = "  [ABOVE 10y 90th pctile -- extreme regime]" if c["extreme_vol"] else ""
    L.append(f"RV20 (20d, annualized): {_c(c['rv20'], 'pct')}{rv_flag}")
    L.append("-" * 78)
    span = c["history_span"]
    span_str = f" ({span[0]} to {span[1]})" if span[0] else ""
    L.append(f"HISTORY: {c['history_n']} earnings-day events{span_str}")
    st = c["history_stats"]
    L.append(f"  mean |reaction|   : {_c(st.get('mean_abs'), 'pct')}")
    L.append(f"  median |reaction| : {_c(st.get('median_abs'), 'pct')}")
    L.append(f"  max |reaction|    : {_c(st.get('max_abs'), 'pct')}")
    L.append(f"  % up              : {_c(st.get('pct_up'), 'pct0')}")
    L.append(f"  mean up-move      : {_c(st.get('mean_up'), 'pct')}")
    L.append(f"  mean down-move    : {_c(st.get('mean_dn'), 'pct')}")
    L.append("")
    L.append("  last 8 prints:")
    hdr = ["date", "eps est", "eps act", "surprise", "gap", "next-day"]
    widths = [10, 8, 8, 9, 8, 9]
    L.append("  " + "  ".join(h.ljust(w) for h, w in zip(hdr, widths)))
    for e in c["history_last8"]:
        cells = [
            e["date"] or "n/a",
            _c(e["eps_est"], "usd2"), _c(e["eps_act"], "usd2"),
            _c(e["surprise"], "pct0"), _c(e["gap"], "pct"), _c(e["reaction"], "pct"),
        ]
        L.append("  " + "  ".join(cell.ljust(w) for cell, w in zip(cells, widths)))
    L.append("-" * 78)
    r_str = _c(c["richness"], "x") if c["richness"] is not None else "n/a"
    L.append(f"VERDICT: richness {r_str} (implied move / median historical |reaction|) -> {c['verdict']}")
    if c["pctile_of_history"] is not None:
        L.append(f"  implied move sits at the {_ordinal(round(c['pctile_of_history'] * 100))} percentile "
                 f"of the historical |reaction| distribution")
    if c["implied_move_is_fallback"] and c["richness"] is not None:
        L.append("  NOTE: richness uses the fallback straddle read -- likely biased HIGH "
                 "(baseline vol is not stripped out)")
    if c["extreme_vol"]:
        L.append("  CAVEAT: RV20 is above the 10-year 90th percentile for this name -- "
                 "history may understate current-cycle move sizes")
    L.append("=" * 78)
    return "\n".join(L)


# ------------------------------------------------------------------- html render ----

CSS = """
body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #f9f9f7; color: #0b0b0b;
       margin: 0; padding: 24px 16px; }
.wrap { max-width: 1060px; margin: 0 auto; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 17px; margin: 34px 0 6px; border-bottom: 1px solid #e1e0d9; padding-bottom: 5px;}
h3 { font-size: 13px; margin: 14px 0 4px; color: #52514e; }
.sub { color: #52514e; margin-bottom: 18px; font-size: 13.5px;}
.card { background: #fcfcfb; border: 1px solid rgba(11,11,11,0.10); border-radius: 10px;
        padding: 14px 16px; margin: 10px 0; }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 12.5px; margin: 8px 0 2px; }
th { text-align: left; color: #52514e; font-weight: 600; border-bottom: 1px solid #c3c2b7; padding: 5px 8px;}
td { border-bottom: 1px solid #e1e0d9; padding: 5px 8px; font-variant-numeric: tabular-nums; }
.tnote { font-size: 11.5px; color: #898781; margin: 4px 0 8px; }
p, li { font-size: 13.5px; line-height: 1.55; }
code { background: #f0efec; padding: 1px 4px; border-radius: 4px; font-size: 12px;}
.verdict { font-size: 14.5px; }
"""


def render_summary_html(cards: list) -> str:
    rows = []
    for c in cards:
        rows.append([
            f"<b>{c['name']}</b>",
            c["next_earnings"] or "-",
            str(c["days_until"]) if c["days_until"] is not None else "-",
            REP._fmt(c["implied_move_1sd"], "pct"),
            REP._fmt(c["history_stats"].get("median_abs"), "pct"),
            REP._fmt(c["richness"], "x") if c["richness"] is not None else "-",
            c["verdict"],
        ])
    return REP.html_table(
        ["Name", "Next print", "Days", "Implied +/-1sd", "Median hist |move|", "Richness", "Verdict"],
        rows,
        "Richness = implied 1sd move / median historical |next-day reaction|. Buckets: "
        "&lt;0.8 cheap, 0.8-1.25 in line, &gt;1.25 rich.")


def render_html_card(c: dict) -> str:
    verdict_color = {
        "priced RICH vs history": REP.RED,
        "priced CHEAP vs history": REP.AQUA,
        "in line": REP.MUTED,
    }.get(c["verdict"], REP.MUTED)

    full = f" -- {c['full_name']}" if c["full_name"] != c["name"] else ""

    header_table = REP.html_table(
        ["Spot", "Next earnings", "Days until", "Consensus EPS (this Q)", "Consensus revenue (this Q)"],
        [[REP._fmt(c["spot"], "usd2"), c["next_earnings"] or "-",
          str(c["days_until"]) if c["days_until"] is not None else "-",
          REP._fmt(c["consensus_eps"], "usd2"), _fmt_usdb(c["consensus_rev"])]])

    fb_note = " (FALLBACK method)" if c["implied_move_is_fallback"] else ""
    move_table = REP.html_table(
        ["Implied move (1sd)", "IV30", "RV20 (20d, ann.)", "Method"],
        [[REP._fmt(c["implied_move_1sd"], "pct") + fb_note,
          _fmt_pctnum(c["iv30"]), REP._fmt(c["rv20"], "pct"), c["implied_move_label"]]])

    st = c["history_stats"]
    hist_table = REP.html_table(
        ["n events", "mean |reaction|", "median |reaction|", "max |reaction|", "% up", "mean up", "mean down"],
        [[st.get("n", "-"), REP._fmt(st.get("mean_abs"), "pct"), REP._fmt(st.get("median_abs"), "pct"),
          REP._fmt(st.get("max_abs"), "pct"), REP._fmt(st.get("pct_up"), "pct0"),
          REP._fmt(st.get("mean_up"), "pct"), REP._fmt(st.get("mean_dn"), "pct")]])

    last8_rows = [[e["date"], REP._fmt(e["eps_est"], "usd2"), REP._fmt(e["eps_act"], "usd2"),
                   REP._fmt(e["surprise"], "pct0"), REP._fmt(e["gap"], "pct"), REP._fmt(e["reaction"], "pct")]
                  for e in c["history_last8"]]
    last8_table = REP.html_table(
        ["Announce date", "EPS est", "EPS actual", "Surprise", "Overnight gap", "Next-day close"],
        last8_rows)

    richness_str = REP._fmt(c["richness"], "x") if c["richness"] is not None else "n/a"
    pctile_str = (_ordinal(round(c["pctile_of_history"] * 100)) + " percentile"
                  if c["pctile_of_history"] is not None else "n/a")
    fb_warn = ("<br>Richness uses the fallback straddle read -- likely biased high (baseline vol is "
               "not stripped out)." if c["implied_move_is_fallback"] and c["richness"] is not None else "")
    caveat = ""
    if c["extreme_vol"]:
        caveat = (f'<p class="tnote">CAVEAT: RV20 ({REP._fmt(c["rv20"], "pct")}) is above the 10-year '
                  f'90th percentile ({REP._fmt(c["rv20_p90_10y"], "pct")}) for this name -- history may '
                  f'understate current-cycle move sizes.</p>')

    return f"""
<h2>{c['name']}{full}</h2>
<div class="card">
  <div class="verdict" style="border-left:4px solid {verdict_color}; padding-left:10px;">
    <b>Richness {richness_str}</b> (implied move / median historical |reaction|) -&gt;
    <b style="color:{verdict_color}">{c['verdict']}</b>. Implied move sits at the {pctile_str}
    of the historical |reaction| distribution.{fb_warn}
  </div>
  {caveat}
  <h3>Event</h3>
  {header_table}
  <h3>Implied vs realized</h3>
  {move_table}
  <h3>Earnings-day history ({st.get('n', '?')} events, {c['history_span'][0] or '?'} to {c['history_span'][1] or '?'})</h3>
  {hist_table}
  {last8_table}
</div>"""


def build_html(cards: list) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    body = "".join(render_html_card(c) for c in cards)
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pre-earnings cards -- MU / NVDA / AMD -- {today}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<h1>Pre-earnings cards -- MU, NVDA, AMD</h1>
<div class="sub">as of {today} &middot; implied move from the CBOE delayed option chain (forward-variance
bracketing where available) &middot; history from yfinance earnings-date actuals &middot; generated by
<code>tools/muval/events.py</code></div>

<h2>Cross-name summary</h2>
<div class="card">{render_summary_html(cards)}</div>
{body}
</div></body></html>"""


# ------------------------------------------------------------------------- main ----

def main(argv: list) -> int:
    sys.stdout.reconfigure(errors="replace")
    offline = "--offline" in argv
    refresh = "--refresh" in argv

    cards = []
    for name in NAMES:
        print(f"[events] {name} ...")
        try:
            cards.append(build_card(name, offline=offline, refresh=refresh))
        except Exception as e:
            print(f"  [warn] {name} failed: {e}")
    if not cards:
        print("[events] no cards built -- aborting")
        return 1

    print()
    print("=" * 78)
    print("CROSS-NAME SUMMARY -- pre-earnings implied-move richness")
    print("=" * 78)
    print(render_summary(cards))
    print()
    for c in cards:
        print(render_card(c))
        print()

    STORE.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    html_path = STORE / f"events-{today}.html"
    json_path = STORE / f"events-{today}.json"

    html_path.write_text(build_html(cards), encoding="utf-8")
    payload = {
        "asof": today,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "names": [c["name"] for c in cards],
        "cards": {c["name"]: c for c in cards},
    }
    json_path.write_text(json.dumps(_safe(payload), indent=1, default=str), encoding="utf-8")

    print(f"HTML report  : {html_path}")
    print(f"JSON snapshot: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
