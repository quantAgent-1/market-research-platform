#!/usr/bin/env python3
"""flowmap.py — The Flow Read v0.1 (semis institutional-flow map, P1-live slice).

One integrated module answering the five-question flow read before any conviction
entry, on the semiconductor complex:

  Q1  Who owned the recent move?        (cohort attribution — KR/TW measured, US inferred)
  Q2  Whose shares am I buying?         (forced seller vs informed distributor)
  Q3  Who is forced to trade next?      (ffcal clock + leveraged-ETF MOC arithmetic)
  Q4  Where is the crowd?               (margin, positioning, crowding state)
  Q5  What's already priced?            (the expectations bar, not the fundamental level)

Design spec: wiki/designs/semis-institutional-flow-map.md (P1-live, section 11).
Identification contract: detects POSITIONING and PRESSURE, never intent. Every
attribution is emitted as hypothesis + confidence + falsifier (MU 2026-06-23 lesson).

Data (all free):
  KR cohort prints   Naver mobile trend API (D+0; engine-v3 S3's approved fallback basis)
  KR margin          KOFIA freesis JSON POST (engine-v3 S10's endpoint, pulled live)
  TW cohort prints   TWSE T86 daily JSON (三大法人 per name; cached per day)
  US prices/options  yfinance (daily + intraday, chains, earnings, estimates)
  US short volume    FINRA CNMS daily short-sale files (cached per day)
  Calendar           tools/calendar/ffcal.py (imported)
  Context            engine-v3 lake if present (NAAIM history, COT, SI fallback)

Commands:
  python flowmap.py                 # full read: pull, compute, brief to stdout,
                                    # write store/dashboard.html (+snapshot), open browser
  python flowmap.py read --quick    # shallower backfills (first run fast path)
  python flowmap.py read --offline  # no network; caches + engine lake only
  python flowmap.py selftest        # arithmetic anchors, no network

Outputs (files are the database):
  store/dashboard.html              # the interactive panel (self-contained)
  store/snapshots/read-<ts>.json    # full computed state — the grading substrate
  store/aum/aum-<date>.json         # own forward AUM archive (S5-style)
  store/cache/...                   # per-day immutable pulls (t86, finra) + soft caches
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import statistics
import sys
import time
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # console is cp949
except Exception:
    pass

import logging

import pandas as pd  # noqa: E402

logging.getLogger("yfinance").setLevel(logging.CRITICAL)  # dead candidate tickers 404 loudly

HERE = Path(__file__).resolve().parent
STORE = HERE / "store"
CACHE = STORE / "cache"
SNAPS = STORE / "snapshots"
AUMDIR = STORE / "aum"
FFCAL_DIR = HERE.parent / "calendar"
# Optional external research lake (KOFIA/COT/surveys). Set ENGINE_LAKE env to a local
# path if you maintain a sibling data lake; default is unset / non-existent (no local
# absolute paths shipped in the public repo).
_engine_env = os.environ.get("ENGINE_LAKE", "").strip()
ENGINE_LAKE = Path(_engine_env) if _engine_env else HERE / "optional_engine_lake"

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# ---------------------------------------------------------------- universe & registry

US_FOCUS = ["NVDA", "AMD", "MU"]
US_CONTEXT = ["SMH", "SOXX"]                      # complex references (SMH = residualizer)
KR_NAMES = {"005930": "Samsung Electronics", "000660": "SK hynix", "042700": "Hanmi Semiconductor"}
TW_NAMES = {"2330": "TSMC", "2454": "MediaTek"}
BRIEF_NAMES = ["NVDA", "AMD", "MU", "005930", "000660", "2330"]

# Leveraged-ETF suite for the L4 MOC arithmetic: (ticker, assumed L, reference).
# L is re-verified against the fund's longName at pull time; unresolvable tickers drop.
LETF_CANDIDATES = [
    ("SOXL", 3.0, "COMPLEX"), ("SOXS", -3.0, "COMPLEX"),
    ("USD", 2.0, "COMPLEX"), ("SSG", -2.0, "COMPLEX"),
    ("NVDL", 2.0, "NVDA"), ("NVDU", 2.0, "NVDA"), ("NVDX", 2.0, "NVDA"),
    ("NVDD", -1.0, "NVDA"), ("NVDQ", -2.0, "NVDA"),
    ("AMDL", 2.0, "AMD"), ("AMDU", 2.0, "AMD"),
    ("MUU", 2.0, "MU"), ("MUD", -1.0, "MU"),
]

# Pre-registered flag rules (design section 4, post-critic): |z|>=3 single feed, or
# |z|>=2 on >=2 feeds from DIFFERENT evidence groups, or the divergence tells.
Z_WIN = 60
FLAG_SINGLE = 3.0
FLAG_DUAL = 2.0
# The six evidence groups. Day one only some are armed; the dashboard says which.
GROUPS = ["asia-prints", "etf-flows", "options", "short-borrow", "off-exchange", "filings"]

# Pre-registered verdict thresholds (equal-weight scores; no fitting until >=60 graded days)
BREADTH_IDIO_PCT = 3.0        # |ret5 - ret5(SMH)| >= 3% -> idiosyncratic
CROWD_HI, CROWD_LO = 0.75, -0.75
Q2_DROP = -4.0                # 5d % move that counts as "forced-seller candidate tape"

RISK_FREE = 0.04

# ---------------------------------------------------------------------------- utils


def _tz(name: str, hours: int):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:
        return dt.timezone(dt.timedelta(hours=hours))


KST = _tz("Asia/Seoul", 9)
ET = _tz("America/New_York", -4)  # fallback offset is July-correct (EDT)


def now_kst() -> dt.datetime:
    return dt.datetime.now(KST)


def parse_num(v) -> float:
    """Signed, comma-grouped number strings ('-2,018,562', '+625,985') -> float."""
    try:
        s = str(v).replace(",", "").replace("+", "").strip()
        return float(s) if s not in ("", "-", "--") else float("nan")
    except (ValueError, TypeError):
        return float("nan")


def zscore(series: list[float] | pd.Series, win: int = Z_WIN) -> float | None:
    """z of the LAST value vs the trailing `win` values before it. None if thin."""
    s = [float(x) for x in list(series) if x == x]  # drop NaN
    if len(s) < max(12, win // 4) + 1:
        return None
    tail = s[-(win + 1):-1] if len(s) > win else s[:-1]
    if len(tail) < 10:
        return None
    mu = statistics.fmean(tail)
    sd = statistics.pstdev(tail)
    if sd <= 0:
        return None
    return (s[-1] - mu) / sd


def jsonify(o):
    """Recursively convert numpy/pandas scalars, dates, NaN -> JSON-safe python."""
    if o is None or isinstance(o, (bool, str)):
        return o
    if isinstance(o, (int,)):
        return o
    if isinstance(o, float):
        return None if (math.isnan(o) or math.isinf(o)) else o
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()
    if isinstance(o, dict):
        return {str(k): jsonify(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonify(v) for v in o]
    if hasattr(o, "item"):  # numpy scalar
        return jsonify(o.item())
    if isinstance(o, pd.Timestamp):
        return o.date().isoformat()
    return str(o)


def fmt_usd(x: float | None, signed: bool = False) -> str:
    if x is None or x != x:
        return "n/a"
    sign = "-" if x < 0 else ("+" if signed else "")
    a = abs(x)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if a >= div:
            return f"{sign}${a / div:.2f}{suf}"
    return f"{sign}${a:.0f}"


def fmt_krw(x: float | None, signed: bool = True) -> str:
    if x is None or x != x:
        return "n/a"
    sign = "-" if x < 0 else ("+" if signed else "")
    a = abs(x)
    if a >= 1e12:
        return f"{sign}{a / 1e12:.2f}T KRW"
    return f"{sign}{a / 1e9:.1f}B KRW"


def fmt_pct(x: float | None, signed: bool = True, dp: int = 1) -> str:
    if x is None or x != x:
        return "n/a"
    return f"{x * 100:+.{dp}f}%" if signed else f"{x * 100:.{dp}f}%"


@dataclass
class Feed:
    name: str
    group: str
    asof: str | None = None
    ok: bool = True
    note: str = ""


FEEDS: list[Feed] = []


def feed(name: str, group: str, asof=None, ok=True, note="") -> None:
    if isinstance(asof, (dt.date, dt.datetime)):
        asof = asof.strftime("%Y-%m-%d")
    FEEDS.append(Feed(name, group, asof, ok, note))


def soft_cache(path: Path, max_age_h: float, offline: bool):
    """Return cached JSON if fresh (or offline); None means caller must fetch."""
    if path.exists():
        age_h = (time.time() - path.stat().st_mtime) / 3600
        if offline or age_h <= max_age_h:
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return None
    return None


def save_cache(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonify(obj), ensure_ascii=False), encoding="utf-8")


# ------------------------------------------------------------------------- pullers


def pull_us_prices(tickers: list[str], offline: bool) -> dict[str, pd.DataFrame]:
    """Daily OHLCV per ticker via yfinance batch; parquet cache for --offline."""
    out: dict[str, pd.DataFrame] = {}
    cache_dir = CACHE / "px"
    if not offline:
        try:
            import yfinance as yf
            raw = yf.download(tickers, period="2y", interval="1d", group_by="ticker",
                              auto_adjust=True, progress=False, threads=True)
            for t in tickers:
                try:
                    df = raw[t].dropna(subset=["Close"]) if len(tickers) > 1 else raw.dropna(subset=["Close"])
                    if not df.empty:
                        out[t] = df
                        cache_dir.mkdir(parents=True, exist_ok=True)
                        df.to_parquet(cache_dir / f"{t.replace('^', '_')}.parquet")
                except Exception:
                    continue
        except Exception as e:
            feed("us-prices", "prices", ok=False, note=f"yfinance batch failed: {e}")
    for t in tickers:  # fill gaps from cache
        if t not in out:
            p = cache_dir / f"{t.replace('^', '_')}.parquet"
            if p.exists():
                try:
                    out[t] = pd.read_parquet(p)
                except Exception:
                    pass
    got = [t for t in tickers if t in out]
    asof = max((out[t].index[-1].date() for t in got), default=None)
    feed("us-prices", "prices", asof=asof, ok=bool(got),
         note=f"{len(got)}/{len(tickers)} tickers" + (" (cache)" if offline else ""))
    return out


def pull_us_intraday(tickers: list[str], offline: bool) -> dict[str, dict]:
    """Latest 5m bar per ticker -> live/last session return vs previous close."""
    out: dict[str, dict] = {}
    if offline:
        return out
    try:
        import yfinance as yf
        raw = yf.download(tickers, period="2d", interval="5m", group_by="ticker",
                          auto_adjust=True, progress=False, threads=True)
        for t in tickers:
            try:
                df = raw[t].dropna(subset=["Close"]) if len(tickers) > 1 else raw.dropna(subset=["Close"])
                if df.empty:
                    continue
                last = df.index[-1]
                out[t] = {"ts": last.isoformat(), "px": float(df["Close"].iloc[-1]),
                          "session_date": last.date().isoformat()}
            except Exception:
                continue
    except Exception:
        pass
    return out


def pull_kr_cohort(code: str, offline: bool, pages: int = 3) -> pd.DataFrame:
    """Naver mobile investor trend -> date, close, volume, foreign/inst/retail net (KRW).

    Net-buy values approximated as quantity x close — the engine-v3 S3 fallback's
    documented basis (consistent across the window, so z-scores are unaffected).
    """
    cpath = CACHE / "naver" / f"{code}.json"
    rows = soft_cache(cpath, max_age_h=3, offline=offline)
    if rows is None:
        import requests
        rows, cursor = [], None
        try:
            for _ in range(pages):
                params: dict = {"pageSize": 60}
                if cursor:
                    params["bizdate"] = cursor
                r = requests.get(f"https://m.stock.naver.com/api/stock/{code}/trend",
                                 params=params, headers=UA, timeout=20)
                r.raise_for_status()
                batch = r.json()
                if not isinstance(batch, list) or not batch:
                    break
                rows.extend(b for b in batch if isinstance(b, dict) and "bizdate" in b)
                oldest = min(str(b.get("bizdate", "")) for b in batch if isinstance(b, dict))
                cursor = (pd.Timestamp(oldest) - pd.Timedelta(days=1)).strftime("%Y%m%d")
                time.sleep(0.3)
            save_cache(cpath, rows)
        except Exception as e:
            feed(f"kr-cohort:{code}", "asia-prints", ok=False, note=str(e)[:120])
            rows = soft_cache(cpath, max_age_h=1e9, offline=True) or []
    recs = []
    for b in rows:
        close = parse_num(b.get("closePrice"))
        if close != close:
            continue
        recs.append({
            "date": pd.Timestamp(str(b["bizdate"])).date(),
            "close": close,
            "volume": parse_num(b.get("accumulatedTradingVolume")),
            "foreign_hold": parse_num(b.get("foreignerHoldRatio")),
            "foreign_net": parse_num(b.get("foreignerPureBuyQuant")) * close,
            "inst_net": parse_num(b.get("organPureBuyQuant")) * close,
            "retail_net": parse_num(b.get("individualPureBuyQuant")) * close,
        })
    df = pd.DataFrame(recs).drop_duplicates("date").sort_values("date").reset_index(drop=True)
    if not df.empty:
        feed(f"kr-cohort:{code}", "asia-prints", asof=df["date"].iloc[-1], note=f"{len(df)} sessions (Naver, qty x close)")
    return df


def pull_kofia_margin(offline: bool) -> pd.DataFrame:
    """KOFIA margin-credit balance (TOTAL/KOSPI/KOSDAQ, KRW) — engine-v3 S10's endpoint, live."""
    cpath = CACHE / "kofia.json"
    data = soft_cache(cpath, max_age_h=6, offline=offline)
    if data is None:
        import requests
        end = dt.date.today()
        body = {"dmSearch": {"tmpV40": "1000000", "tmpV45": (end - dt.timedelta(days=400)).strftime("%Y%m%d"),
                             "tmpV46": end.strftime("%Y%m%d"), "tmpV1": "D", "OBJ_NM": "STATSCU0100000070BO"}}
        try:
            r = requests.post("https://freesis.kofia.or.kr/meta/getMetaDataList.do", json=body,
                              headers={**UA, "Referer": "https://freesis.kofia.or.kr/stat/FreeSIS.do"}, timeout=30)
            r.raise_for_status()
            data = r.json().get("ds1", [])
            save_cache(cpath, data)
        except Exception as e:
            feed("kr-margin", "asia-prints", ok=False, note=f"KOFIA live failed: {str(e)[:90]}")
            data = soft_cache(cpath, max_age_h=1e9, offline=True)
    rows = []
    for row in data or []:
        if isinstance(row, dict) and row.get("TMPV1") and row.get("TMPV2") is not None:
            rows.append({"date": pd.Timestamp(str(row["TMPV1"])).date(),
                         "total": float(row["TMPV2"]) * 1e6,
                         "kospi": float(row.get("TMPV3") or 0) * 1e6,
                         "kosdaq": float(row.get("TMPV4") or 0) * 1e6})
    df = pd.DataFrame(rows).drop_duplicates("date").sort_values("date").reset_index(drop=True)
    if df.empty and ENGINE_LAKE.exists():  # lake fallback
        try:
            lk = pd.read_parquet(ENGINE_LAKE / "kofia_credit" / "TOTAL.parquet")
            df = pd.DataFrame({"date": pd.to_datetime(lk["effective_date"]).dt.date,
                               "total": lk["credit_balance"].astype(float)}).sort_values("date")
            feed("kr-margin", "asia-prints", asof=df["date"].iloc[-1], note="engine lake (stale fallback)")
            return df
        except Exception:
            pass
    if not df.empty:
        feed("kr-margin", "asia-prints", asof=df["date"].iloc[-1], note=f"{len(df)} days (KOFIA live)")
    return df


def pull_tw_cohort(code: str, offline: bool, sessions: int = 60) -> pd.DataFrame:
    """TWSE T86 per-name daily institutional prints (shares). Per-day files cached forever.

    Parsing is defensive: foreign = ex-dealer net (+ foreign-dealer net if present),
    trust = investment-trust net, dealer = total(idx 17) - foreign - trust (residual).
    """
    tdir = CACHE / "t86"
    tdir.mkdir(parents=True, exist_ok=True)
    import requests
    rows, d, scanned = [], dt.date.today(), 0
    fetched = 0
    while len(rows) < sessions and scanned < int(sessions * 1.9) + 10:
        scanned += 1
        if d.weekday() >= 5:
            d -= dt.timedelta(days=1)
            continue
        p = tdir / f"{d.strftime('%Y%m%d')}.json"
        day = None
        if p.exists():
            try:
                day = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                day = None
        if day is None and not offline:
            try:
                r = requests.get("https://www.twse.com.tw/rwd/en/fund/T86",
                                 params={"date": d.strftime("%Y%m%d"), "selectType": "ALLBUT0999", "response": "json"},
                                 headers=UA, timeout=20)
                day = r.json() if r.status_code == 200 else {"stat": f"http {r.status_code}"}
                # today's file may simply not be posted yet -> don't poison the cache
                if day.get("stat") == "OK" or d < dt.date.today():
                    p.write_text(json.dumps(day), encoding="utf-8")
                fetched += 1
                time.sleep(2.2 if fetched else 0)
            except Exception:
                day = None
        if day and day.get("stat") == "OK":
            for row in day.get("data", []):
                if row and str(row[0]).strip() == code and len(row) >= 18:
                    f_net = parse_num(row[3])
                    fd_net = parse_num(row[6])
                    f_all = f_net + (fd_net if fd_net == fd_net else 0.0)
                    trust = parse_num(row[9])
                    total = parse_num(row[17])
                    dealer = total - f_all - trust if total == total else float("nan")
                    rows.append({"date": d, "foreign_net": f_all, "trust_net": trust,
                                 "dealer_net": dealer, "total_net": total})
                    break
        d -= dt.timedelta(days=1)
    df = pd.DataFrame(rows).drop_duplicates("date").sort_values("date").reset_index(drop=True)
    if not df.empty:
        feed(f"tw-cohort:{code}", "asia-prints", asof=df["date"].iloc[-1], note=f"{len(df)} sessions (T86, shares)")
    else:
        feed(f"tw-cohort:{code}", "asia-prints", ok=False, note="no T86 rows")
    return df


def pull_finra_shortvol(tickers: list[str], offline: bool, days: int = 30) -> dict[str, pd.DataFrame]:
    """FINRA CNMS daily short-sale volume files -> per-name short-volume ratio series."""
    fdir = CACHE / "finra"
    fdir.mkdir(parents=True, exist_ok=True)
    import requests
    per: dict[str, list] = {t: [] for t in tickers}
    d, have, scanned = dt.date.today(), 0, 0
    while have < days and scanned < int(days * 1.9) + 10:
        scanned += 1
        if d.weekday() >= 5:
            d -= dt.timedelta(days=1)
            continue
        p = fdir / f"{d.strftime('%Y%m%d')}.txt"
        text = None
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="replace")
        elif not offline:
            try:
                r = requests.get(f"https://cdn.finra.org/equity/regsho/daily/CNMSshvol{d.strftime('%Y%m%d')}.txt",
                                 headers=UA, timeout=20)
                if r.status_code == 200 and "|" in r.text[:200]:
                    text = r.text
                    p.write_text(text, encoding="utf-8")
                elif d < dt.date.today():
                    p.with_suffix(".miss").write_text(str(r.status_code))
                time.sleep(0.35)
            except Exception:
                text = None
        elif p.with_suffix(".miss").exists():
            pass
        if p.with_suffix(".miss").exists() and text is None:
            d -= dt.timedelta(days=1)
            continue
        if text:
            have += 1
            want = set(tickers)
            for line in text.splitlines()[1:]:
                parts = line.split("|")
                if len(parts) >= 5 and parts[1] in want:
                    sv, tv = parse_num(parts[2]), parse_num(parts[4])
                    if tv and tv > 0:
                        per[parts[1]].append({"date": d, "short_ratio": sv / tv, "total_vol": tv})
        d -= dt.timedelta(days=1)
    out = {}
    for t, rows in per.items():
        if rows:
            out[t] = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    asof = max((df["date"].iloc[-1] for df in out.values()), default=None)
    feed("finra-shortvol", "short-borrow", asof=asof, ok=bool(out), note=f"{have} daily files")
    return out


def _yf_info(ticker: str, offline: bool) -> dict:
    cpath = CACHE / "yfinfo" / f"{ticker}.json"
    info = soft_cache(cpath, max_age_h=12, offline=offline)
    if info is None:
        try:
            import yfinance as yf
            raw = yf.Ticker(ticker).info or {}
            keys = ["longName", "totalAssets", "navPrice", "sharesOutstanding", "sharesShort",
                    "shortPercentOfFloat", "shortRatio", "dateShortInterest", "forwardPE", "trailingPE"]
            info = {k: raw.get(k) for k in keys}
            save_cache(cpath, info)
        except Exception:
            info = soft_cache(cpath, max_age_h=1e9, offline=True) or {}
    return info or {}


def _leverage_from_name(long_name: str | None, default: float) -> float:
    """Verify assumed leverage against the fund's name ('2X Long', 'Bear 3X', 'Inverse')."""
    if not long_name:
        return default
    s = long_name.upper()
    mult = None
    for pat, val in (("3X", 3.0), ("2X", 2.0), ("1.5X", 1.5), ("1X", 1.0)):
        if pat in s.replace(" ", ""):
            mult = val
            break
    if mult is None:
        return default
    neg = any(w in s for w in ("BEAR", "INVERSE", "SHORT", "DOWN"))
    return -mult if neg else mult


def pull_letf_suite(offline: bool) -> list[dict]:
    """Resolve the LETF candidates: AUM + verified leverage. Appends today's AUM archive."""
    suite = []
    for tkr, L, ref in LETF_CANDIDATES:
        info = _yf_info(tkr, offline)
        aum = info.get("totalAssets")
        if not aum or aum <= 0:
            continue
        Lv = _leverage_from_name(info.get("longName"), L)
        suite.append({"etf": tkr, "L": Lv, "k": Lv * Lv - Lv, "ref": ref,
                      "aum": float(aum), "name": info.get("longName") or tkr})
    if suite:
        AUMDIR.mkdir(parents=True, exist_ok=True)
        apath = AUMDIR / f"aum-{dt.date.today():%Y%m%d}.json"
        if not apath.exists():
            save_cache(apath, {r["etf"]: r["aum"] for r in suite})
        feed("letf-aum", "etf-flows", asof=dt.date.today(), note=f"{len(suite)}/{len(LETF_CANDIDATES)} funds resolved")
    else:
        feed("letf-aum", "etf-flows", ok=False, note="no AUM resolved")
    return suite


def aum_history() -> dict[str, list]:
    """Own forward AUM archive (grows one point per run-day)."""
    hist: dict[str, list] = {}
    for p in sorted(AUMDIR.glob("aum-*.json")):
        try:
            day = json.loads(p.read_text(encoding="utf-8"))
            d = p.stem.split("-")[1]
            for k, v in day.items():
                hist.setdefault(k, []).append({"date": f"{d[:4]}-{d[4:6]}-{d[6:]}", "aum": v})
        except Exception:
            continue
    return hist


def pull_options(ticker: str, spot: float, earnings_date: dt.date | None, offline: bool) -> dict:
    """Chain snapshot: ATM IV, P/C ratios, straddle-implied move at the event expiry,
    naive dealer-GEX profile (dealers long calls / short puts convention — LOW confidence)."""
    out = {"ok": False}
    if offline or not spot:
        return out
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        expiries = [dt.date.fromisoformat(e) for e in (t.options or [])]
        today = dt.date.today()
        near = [e for e in expiries if (e - today).days >= 5]
        if not near:
            return out
        chains, picked = {}, []
        base = near[0]
        picked.append(base)
        if earnings_date:
            ev = next((e for e in expiries if e >= earnings_date), None)
            if ev and ev not in picked:
                picked.append(ev)
        elif len(near) > 1:
            picked.append(near[1])
        for e in picked:
            ch = t.option_chain(e.isoformat())
            chains[e] = ch
        pc_oi = pc_vol = None
        c0 = chains[base]
        coi, poi = float(c0.calls["openInterest"].sum()), float(c0.puts["openInterest"].sum())
        cv, pv = float(c0.calls["volume"].fillna(0).sum()), float(c0.puts["volume"].fillna(0).sum())
        pc_oi = poi / coi if coi > 0 else None
        pc_vol = pv / cv if cv > 0 else None

        def atm_straddle(ch, exp):
            days = max((exp - today).days, 1)
            calls = ch.calls[(ch.calls["strike"] > spot * 0.85) & (ch.calls["strike"] < spot * 1.15)]
            if calls.empty:
                return None
            k = calls.iloc[(calls["strike"] - spot).abs().argsort()].iloc[0]["strike"]
            c = ch.calls[ch.calls["strike"] == k]
            p = ch.puts[ch.puts["strike"] == k]
            if c.empty or p.empty:
                return None
            def mid(row):
                b, a, last = float(row["bid"].iloc[0] or 0), float(row["ask"].iloc[0] or 0), float(row["lastPrice"].iloc[0] or 0)
                return (b + a) / 2 if (b > 0 and a > 0) else last
            st = mid(c) + mid(p)
            iv = float(pd.concat([c["impliedVolatility"], p["impliedVolatility"]]).mean())
            return {"strike": float(k), "straddle": st, "move": st / spot, "days": days, "iv": iv,
                    "expiry": exp.isoformat()}
        amb = atm_straddle(chains[base], base)
        event = None
        if earnings_date:
            ev_exp = next((e for e in picked if e >= earnings_date), None)
            if ev_exp:
                event = atm_straddle(chains[ev_exp], ev_exp)
        # naive GEX: sum gamma dollars per 1% across picked expiries, sign +call/-put
        def phi(x):
            return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
        strikes_all = []
        legs = []
        for e, ch in chains.items():
            T = max((e - today).days, 1) / 365.0
            for df_side, sgn in ((ch.calls, 1.0), (ch.puts, -1.0)):
                sub = df_side[(df_side["strike"] > spot * 0.8) & (df_side["strike"] < spot * 1.2)]
                for _, r in sub.iterrows():
                    iv = float(r["impliedVolatility"] or 0)
                    oi = float(r["openInterest"] or 0)
                    if iv <= 0.01 or oi <= 0:
                        continue
                    legs.append((float(r["strike"]), iv, T, oi, sgn))
                    strikes_all.append(float(r["strike"]))

        def gex_at(s):
            tot = 0.0
            for k, iv, T, oi, sgn in legs:
                d1 = (math.log(s / k) + (RISK_FREE + iv * iv / 2) * T) / (iv * math.sqrt(T))
                gamma = phi(d1) / (s * iv * math.sqrt(T))
                tot += sgn * gamma * oi * 100 * s * s * 0.01
            return tot
        gex_spot = gex_at(spot) if legs else None
        flip = None
        if legs:
            grid = [spot * (0.90 + i * 0.01) for i in range(21)]
            vals = [(s, gex_at(s)) for s in grid]
            for (s1, g1), (s2, g2) in zip(vals, vals[1:]):
                if g1 == 0 or (g1 < 0) != (g2 < 0):
                    flip = s1 + (s2 - s1) * (abs(g1) / (abs(g1) + abs(g2) + 1e-9))
                    break
        out = {"ok": True, "pc_oi": pc_oi, "pc_vol": pc_vol, "ambient": amb, "event": event,
               "gex_per_pct": gex_spot, "gex_flip": flip, "atm_iv": (amb or {}).get("iv")}
        feed(f"options:{ticker}", "options", asof=today, note=f"{len(legs)} legs, naive-GEX convention")
    except Exception as e:
        feed(f"options:{ticker}", "options", ok=False, note=str(e)[:100])
    return out


def pull_us_meta(ticker: str, offline: bool) -> dict:
    """Earnings date(s), past reaction moves inputs, EPS revision trend, SI fields."""
    cpath = CACHE / "yfmeta" / f"{ticker}.json"
    meta = soft_cache(cpath, max_age_h=12, offline=offline)
    if meta is None:
        meta = {}
        try:
            import yfinance as yf
            t = yf.Ticker(ticker)
            try:
                cal = t.calendar or {}
                eds = cal.get("Earnings Date") or []
                meta["next_earnings"] = min(eds).isoformat() if eds else None
            except Exception:
                meta["next_earnings"] = None
            try:
                ed = t.get_earnings_dates(limit=24)
                past = [i.date().isoformat() for i, r in ed.iterrows()
                        if r.get("Reported EPS") == r.get("Reported EPS") and i.date() < dt.date.today()]
                fut = [i.date().isoformat() for i, r in ed.iterrows() if i.date() >= dt.date.today()]
                meta["past_earnings"] = sorted(past, reverse=True)[:10]
                meta["next_earnings_alt"] = min(fut) if fut else None
            except Exception:
                meta["past_earnings"] = []
                meta["next_earnings_alt"] = None
            try:
                tr = t.get_eps_trend()
                rev = {}
                for period in ("0q", "0y", "+1y"):
                    if period in tr.index:
                        cur, ago = tr.loc[period, "current"], tr.loc[period, "30daysAgo"]
                        if cur == cur and ago and ago == ago and ago != 0:
                            rev[period] = float(cur) / float(ago) - 1.0
                meta["rev30"] = rev
            except Exception:
                meta["rev30"] = {}
            save_cache(cpath, meta)
        except Exception:
            meta = soft_cache(cpath, max_age_h=1e9, offline=True) or {}
    info = _yf_info(ticker, offline)
    meta["si"] = {"shares_short": info.get("sharesShort"), "pct_float": info.get("shortPercentOfFloat"),
                  "days_to_cover": info.get("shortRatio"),
                  "asof": (dt.datetime.fromtimestamp(info["dateShortInterest"], dt.timezone.utc).date().isoformat()
                           if info.get("dateShortInterest") else None)}
    return meta


def pull_engine_context() -> dict:
    """Optional context from the engine-v3 lake: NAAIM (full history -> z), COT."""
    ctx = {"present": ENGINE_LAKE.exists()}
    if not ctx["present"]:
        feed("engine-lake", "context", ok=False, note="lake not found")
        return ctx
    try:
        na = pd.read_parquet(ENGINE_LAKE / "surveys" / "naaim_exposure.parquet")
        na = na.sort_values("effective_date")
        vals = na["value"].astype(float).tolist()
        ctx["naaim"] = {"value": vals[-1], "z": zscore(vals, 260),
                        "asof": str(pd.to_datetime(na["effective_date"]).iloc[-1].date())}
    except Exception:
        ctx["naaim"] = None
    try:
        cot = pd.read_parquet(ENGINE_LAKE / "cot" / "NQ.parquet").sort_values("effective_date")
        ctx["cot_nq"] = {"value": float(cot["noncommercial_net"].iloc[-1]),
                         "z": zscore(cot["noncommercial_net"].astype(float).tolist(), 156),
                         "asof": str(pd.to_datetime(cot["effective_date"]).iloc[-1].date())}
    except Exception:
        ctx["cot_nq"] = None
    feed("engine-lake", "context", asof=None, ok=True,
         note="NAAIM" + (" ok" if ctx.get("naaim") else " missing") + ", COT" + (" ok" if ctx.get("cot_nq") else " missing"))
    return ctx


def pull_ffcal(asof: dt.date, horizon: int = 10) -> list[dict]:
    """Import the forced-flow calendar and serialize the next-N-days events."""
    try:
        sys.path.insert(0, str(FFCAL_DIR))
        import ffcal  # noqa: PLC0415
        ov = ffcal.load_overrides()
        ctx = ffcal.Ctx(asof, asof - dt.timedelta(days=7), asof + dt.timedelta(days=horizon + 45), ov)
        evs = ffcal.build(ctx)
        days = []
        for i in range(horizon):
            d = asof + dt.timedelta(days=i)
            todays = [e for e in evs if e.covers(d)]
            days.append({
                "date": d.isoformat(), "dow": d.strftime("%a"),
                "density": ffcal.day_score(todays, d) if hasattr(ffcal, "day_score") else len(todays),
                "events": [{"time": e.time, "label": e.label, "market": e.market, "size": e.size,
                            "conf": e.confidence, "mech": e.mechanics, "feed": e.feed,
                            "span": bool(e.end and e.end != e.date)} for e in todays],
            })
        feed("ffcal", "calendar", asof=asof, note=f"{sum(len(d['events']) for d in days)} events / {horizon}d")
        return days
    except Exception as e:
        feed("ffcal", "calendar", ok=False, note=str(e)[:120])
        return []


# ---------------------------------------------------------------- series helpers


def px_series(df: pd.DataFrame | None) -> dict:
    """Daily closes -> returns pack: ret1/5/20, z's, 20d arrays, ON/ID split."""
    out = {"ok": False}
    if df is None or df.empty or len(df) < 25:
        return out
    c = df["Close"].astype(float)
    o = df["Open"].astype(float)
    rets = c.pct_change()
    ret5_series = c.pct_change(5)
    out.update({
        "ok": True,
        "last": float(c.iloc[-1]), "date": df.index[-1].date().isoformat(),
        "ret1": float(rets.iloc[-1]), "ret5": float(ret5_series.iloc[-1]),
        "ret20": float(c.pct_change(20).iloc[-1]) if len(c) > 21 else None,
        "ret60": float(c.pct_change(60).iloc[-1]) if len(c) > 61 else None,
        "ret5_z": zscore(ret5_series.dropna().tolist()),
        "ret20_z": zscore(c.pct_change(20).dropna().tolist(), 250),
        "vol5_z": zscore(df["Volume"].astype(float).rolling(5).mean().dropna().tolist()),
        "dates20": [d.date().isoformat() for d in df.index[-20:]],
        "closes20": [float(x) for x in c.iloc[-20:]],
        "rets20": [float(x) if x == x else 0.0 for x in rets.iloc[-20:]],
    })
    on = (o / c.shift(1) - 1).iloc[-20:]
    idr = (c / o - 1).iloc[-20:]
    out["on20"] = [float(x) if x == x else 0.0 for x in on]
    out["id20"] = [float(x) if x == x else 0.0 for x in idr]
    out["on5"] = float((o / c.shift(1) - 1).iloc[-5:].sum())
    out["id5"] = float((c / o - 1).iloc[-5:].sum())
    rv = rets.iloc[-21:].std() * math.sqrt(252) if len(rets) > 21 else None
    out["rv20"] = float(rv) if rv is not None and rv == rv else None
    return out


def kr_px_pack(df: pd.DataFrame) -> dict:
    """Same pack from the Naver frame (close/volume columns)."""
    if df.empty or len(df) < 25:
        return {"ok": False}
    c = df["close"].astype(float)
    rets = c.pct_change()
    return {
        "ok": True, "last": float(c.iloc[-1]), "date": df["date"].iloc[-1].isoformat(),
        "ret1": float(rets.iloc[-1]), "ret5": float(c.pct_change(5).iloc[-1]),
        "ret20": float(c.pct_change(20).iloc[-1]) if len(c) > 21 else None,
        "ret60": float(c.pct_change(60).iloc[-1]) if len(c) > 61 else None,
        "ret5_z": zscore(c.pct_change(5).dropna().tolist()),
        "ret20_z": zscore(c.pct_change(20).dropna().tolist(), 120),
        "vol5_z": zscore(df["volume"].astype(float).rolling(5).mean().dropna().tolist()),
        "dates20": [d.isoformat() for d in df["date"].iloc[-20:]],
        "closes20": [float(x) for x in c.iloc[-20:]],
        "rets20": [float(x) if x == x else 0.0 for x in rets.iloc[-20:]],
        "rv20": float(rets.iloc[-21:].std() * math.sqrt(252)) if len(rets) > 21 else None,
    }


def cohort_pack(df: pd.DataFrame, cols: list[tuple[str, str]], unit: str) -> dict:
    """Cohort daily nets -> 20d chart arrays + 5d/20d cums + z of 5d sums per cohort."""
    if df.empty:
        return {"ok": False}
    out = {"ok": True, "unit": unit, "dates": [d.isoformat() for d in df["date"].iloc[-20:]], "cohorts": []}
    for key, label in cols:
        s = df[key].astype(float)
        roll5 = s.rolling(5).sum()
        out["cohorts"].append({
            "key": key, "label": label,
            "daily20": [float(x) if x == x else 0.0 for x in s.iloc[-20:]],
            "cum5": float(s.iloc[-5:].sum()), "cum20": float(s.iloc[-20:].sum()),
            "z5": zscore(roll5.dropna().tolist()),
            "streak": _streak(s),
        })
    return out


def _streak(s: pd.Series) -> int:
    """Signed run length of the latest cohort direction (+3 = 3 consecutive net-buy days)."""
    vals = [float(x) for x in s.tolist() if x == x]
    if not vals:
        return 0
    sign = 1 if vals[-1] > 0 else -1
    n = 0
    for v in reversed(vals):
        if (v > 0) == (sign > 0) and v != 0:
            n += 1
        else:
            break
    return sign * n


# ------------------------------------------------------------- the five questions


def verdict(v: str, chip: str, conf: str, headline: str, hypothesis: str = "",
            falsifier: str = "", evidence: list[str] | None = None) -> dict:
    return {"verdict": v, "chip": chip, "confidence": conf, "headline": headline,
            "hypothesis": hypothesis, "falsifier": falsifier, "evidence": evidence or []}


def q1_attribution(name: str, kind: str, px: dict, coh: dict, svr: pd.DataFrame | None,
                   smh_px: dict) -> tuple[dict, dict]:
    """Q1: who owned the recent move. Measured for KR/TW, inferred for US."""
    data: dict = {"cohort": coh if coh.get("ok") else None}
    ret5 = px.get("ret5")
    resid = None
    if ret5 is not None and smh_px.get("ret5") is not None:
        resid = ret5 - smh_px["ret5"]
    breadth = None
    if resid is not None:
        breadth = "idiosyncratic" if abs(resid) * 100 >= BREADTH_IDIO_PCT else "shared"
    data["breadth"] = {"resid5": resid, "verdict": breadth, "rule": f"|ret5 - ret5(SMH)| >= {BREADTH_IDIO_PCT}%"}

    if kind in ("kr", "tw") and coh.get("ok"):
        ranked = sorted(coh["cohorts"], key=lambda c: abs(c["cum5"]), reverse=True)
        dom = ranked[0]
        side = "bought" if dom["cum5"] > 0 else "sold"
        unit = coh["unit"]
        amt = fmt_krw(dom["cum5"]) if unit == "KRW" else f"{dom['cum5'] / 1e6:+.1f}M sh"
        ev = []
        for c in coh["cohorts"]:
            a = fmt_krw(c["cum5"]) if unit == "KRW" else f"{c['cum5'] / 1e6:+.2f}M sh"
            z = f", z={c['z5']:+.1f}" if c.get("z5") is not None else ""
            ev.append(f"{c['label']}: 5d {a}{z}, streak {c['streak']:+d}d")
        move = fmt_pct(ret5)
        hyp = f"The {move} 5d move was led by {dom['label'].lower()} ({side} {amt})."
        if breadth == "shared":
            hyp += " Breadth test says complex-wide -> read as flow, not name-specific information."
        fal = (f"If {dom['label'].lower()} flow flips sign for 2+ consecutive sessions while price "
               f"holds, this attribution dies.")
        v = verdict(f"{dom['label'].upper()} {side.upper()}", "info", "MEASURED-HIGH",
                    f"{dom['label']} {side} {amt} over 5d (direct prints)", hyp, fal, ev)
        return v, data

    # US: inference only — overnight/intraday split + short-volume ratio
    ev = []
    on5, id5 = px.get("on5"), px.get("id5")
    if on5 is not None:
        ev.append(f"5d split: overnight {fmt_pct(on5)} vs intraday {fmt_pct(id5)} "
                  f"(clientele diagnostic, not identity)")
    svr_z = None
    if svr is not None and not svr.empty:
        svr_z = zscore(svr["short_ratio"].tolist(), 25)
        data["svr"] = {"dates": [d.isoformat() for d in svr["date"].iloc[-30:]],
                       "ratio": [float(x) for x in svr["short_ratio"].iloc[-30:]], "z": svr_z}
        ev.append(f"FINRA short-volume ratio {svr['short_ratio'].iloc[-1] * 100:.0f}%"
                  + (f" (z={svr_z:+.1f})" if svr_z is not None else "")
                  + " — liquidity-provision mix, weak cohort signal")
    lead = "overnight/gap" if on5 is not None and abs(on5) > abs(id5 or 0) else "intraday-session"
    hyp = (f"No US cohort prints exist; the {fmt_pct(px.get('ret5'))} move is {breadth or 'unclassified'} "
           f"and was {lead}-led. Institutions cannot be identified from public data (identity traded for behavior).")
    fal = "Asia cohort prints (the measured anchors) contradicting the direction within 2 sessions."
    v = verdict("INFERRED", "neutral", "INFERRED-LOW",
                f"{lead}-led move; no direct cohort data for US names", hyp, fal, ev)
    return v, data


def q2_whose_shares(name: str, kind: str, px: dict, coh: dict, margin: dict | None,
                    moc_rows: list[dict]) -> dict:
    """Q2: forced seller (good) vs informed distributor (bad)."""
    ev, score_f, score_d = [], 0, 0
    ret5 = (px.get("ret5") or 0) * 100

    def amt(x):
        return fmt_krw(x) if coh.get("unit") == "KRW" else f"{(x or 0) / 1e6:+.2f}M sh"

    if kind in ("kr", "tw") and coh.get("ok"):
        by = {c["key"]: c for c in coh["cohorts"]}
        fkey = "foreign_net"
        rkey = "retail_net" if "retail_net" in by else "dealer_net"
        ikey = "inst_net" if "inst_net" in by else "trust_net"
        f, r = by.get(fkey), by.get(rkey)
        # forced-seller tape: hard 5d drop + retail/margin supply + foreign absorption
        if ret5 <= Q2_DROP:
            score_f += 1
            ev.append(f"5d {ret5:+.1f}% qualifies as stress tape (<= {Q2_DROP}%)")
            if r and (r.get("z5") or 0) <= -0.5:
                score_f += 1
                ev.append(f"{r['label']} net-selling z={r['z5']:+.1f} -> deleveraging-style supply")
            if margin and (margin.get("d5") or 0) < 0:
                score_f += 1
                ev.append(f"KR margin balance 5d change {fmt_krw(margin['d5'])} -> margin clock unwinding")
            if f and f["cum5"] > 0:
                score_f += 1
                ev.append(f"Foreign absorbed {amt(f['cum5'])} into the drop (buyer of forced supply)")
        # distribution tape: price flat/up while foreign steadily sells and retail absorbs
        if ret5 >= -1.0 and f and r:
            fs = f.get("streak") or 0
            if (f.get("z5") or 0) <= -1.0 or fs <= -3:
                score_d += 1
                ev.append(f"Foreign selling into strength: 5d {amt(f['cum5'])}, streak {fs:+d}d")
                if (r.get("z5") or 0) >= 1.0 or r["cum5"] > 0:
                    score_d += 1
                    ev.append(f"{r['label']} absorbing ({amt(r['cum5'])} 5d) — the classic distribution pair")
        if by.get(ikey):
            i = by[ikey]
            ev.append(f"{i['label']}: 5d {amt(i['cum5'])}, streak {i['streak']:+d}d")
        if score_d >= 2:
            return verdict("DISTRIBUTION TAPE", "serious", "MEASURED-MED",
                           "Informed-style distribution: foreigners selling strength, retail absorbing",
                           "Buying here means buying an informed distributor's shares (bad).",
                           "Foreign net-buy flipping positive 2+ consecutive sessions kills this read.", ev)
        if score_f >= 2:
            return verdict("FORCED-SELLER TAPE", "good", "MEASURED-MED",
                           "Cascade/deleveraging supply — sellers are forced, not informed",
                           "Buying here means buying a forced seller's shares (favorable), "
                           "the MU Jun-23 lesson in reverse.",
                           "If the complex keeps falling with foreign selling joining in, this was "
                           "information, not a cascade.", ev)
        return verdict("MIXED", "neutral", "MEASURED-LOW",
                       "No dominant forced-vs-informed pattern in the prints", "", "", ev)

    # US: mechanics-only inference
    if px.get("ok"):
        mech = sum(abs(r["dollars"] or 0) for r in moc_rows)
        big = max((abs(x) for x in px.get("rets20", [0])[-5:]), default=0)
        if big >= 0.025 and mech:
            ev.append(f"LETF suite rebalance on the biggest recent day ~ {fmt_usd(mech)} same-direction "
                      f"MOC flow -> mechanical amplification present")
            score_f += 1
        on5, id5 = px.get("on5") or 0, px.get("id5") or 0
        ev.append(f"Overnight {fmt_pct(on5)} vs intraday {fmt_pct(id5)} over 5d")
        # capitulation fingerprint: volume-climax day closing well off the low
        if (px.get("vol5_z") or 0) >= 2 and ret5 <= Q2_DROP:
            score_f += 1
            ev.append("Volume climax + stress tape -> flush fingerprint (weak, price-derived)")
    if score_f >= 2:
        return verdict("FORCED-FLAVORED", "good", "INFERRED-LOW",
                       "Mechanical/forced supply likely present (inference only)",
                       "US cohort identity is unobservable; this is a mechanics read.",
                       "Asia anchors showing informed-style distribution would override.", ev)
    return verdict("MIXED", "neutral", "INFERRED-LOW",
                   "No strong forced-vs-informed signature from US proxies", "", "", ev)


def q3_forced_next(name: str, suite: list[dict], ref_rets: dict, cal_days: list[dict],
                   margin: dict | None, gamma: dict | None, live: dict | None) -> tuple[dict, dict]:
    """Q3: ffcal window + LETF MOC arithmetic + margin clock + dealer-gamma state."""
    rows = []
    for r in suite:
        # COMPLEX view sums the whole suite; a name view takes its own single-stock
        # funds plus the index-level funds (shown as a separate COMPLEX line).
        if name != "COMPLEX" and r["ref"] != name and r["ref"] != "COMPLEX":
            continue
        ref = r["ref"] if r["ref"] != "COMPLEX" else "SOXX"
        rr = ref_rets.get(ref)
        dollars = r["k"] * r["aum"] * rr if rr is not None else None
        rows.append({**r, "ref_ret": rr, "dollars": dollars})
    total = sum(r["dollars"] for r in rows if r["dollars"] is not None) if rows else None
    ev = []
    rlab = "live" if (live or {}).get("is_live") else "last session"
    if rows:
        rr0 = rows[0]["ref_ret"]
        ev.append(f"LETF MOC estimate at {rlab} return {fmt_pct(rr0)}: {fmt_usd(total, signed=True)} "
                  f"(sum of (L^2-L) x AUM x r across {len(rows)} funds; trades ~15:50-16:00 ET, "
                  f"computable by ~15:00)")
    if margin and margin.get("z") is not None:
        state = "elevated" if margin["z"] >= 1 else ("low" if margin["z"] <= -1 else "normal")
        ev.append(f"KR margin balance {fmt_krw(margin['level'], signed=False)} (z={margin['z']:+.1f}, {state})"
                  + (f"; 5d {fmt_krw(margin['d5'])}" if margin.get("d5") is not None else ""))
        if margin["z"] >= 1 and (margin.get("kospi_ret1") or 0) <= -0.025:
            ev.append("MARGIN CLOCK ARMED: high balance + hard down day -> 09:00-10:00 KST "
                      "forced-supply window next Seoul open (ffcal F13 semantics)")
    if gamma and gamma.get("gex_per_pct") is not None:
        sign = "LONG gamma (hedging dampens moves)" if gamma["gex_per_pct"] > 0 else \
               "SHORT gamma (hedging amplifies moves)"
        flip = f", flip ~{gamma['gex_flip']:.0f}" if gamma.get("gex_flip") else ""
        ev.append(f"Dealer gamma (naive convention, LOW conf): {sign}{flip}")
    upcoming = []
    for d in cal_days[:7]:
        for e in d["events"]:
            if e["size"] in ("L", "XL") and not e.get("span"):
                upcoming.append(f"{d['date'][5:]} {e['label']}")
    if upcoming:
        ev.append("Calendar (L/XL next 7d): " + " | ".join(upcoming[:5]))
    headline = (f"{fmt_usd(total, signed=True)} mechanical MOC at {rlab} return"
                if total is not None else "Calendar-only view (no LETF rows resolved)")
    v = verdict("SCHEDULED FLOW", "info", "MEASURED-HIGH" if rows else "MEASURED-MED", headline,
                "The only flow knowable BEFORE it trades: leveraged-ETF close rebalancing plus "
                "the dated calendar.",
                "AUM figures go stale if not refreshed; scenario shifts with the day's return.", ev)
    return v, {"moc_rows": rows, "moc_total": total, "ref_label": rlab}


def q4_crowd(name: str, kind: str, px: dict, coh: dict, meta: dict | None, opt: dict | None,
             margin: dict | None, engine: dict, suite: list[dict]) -> tuple[dict, dict]:
    """Q4: crowd density. Equal-weight score over the armed z inputs (pre-registered)."""
    rows, score_in = [], []

    def row(label, value, z=None, orient=0, group="", asof=None, note=""):
        rows.append({"label": label, "value": value, "z": z, "orient": orient,
                     "group": group, "asof": asof, "note": note})
        if z is not None and orient:
            score_in.append(z * orient)

    if px.get("ret20") is not None:
        row("20d return (run-up)", fmt_pct(px["ret20"]), px.get("ret20_z"), +1, "prices")
    if px.get("vol5_z") is not None:
        row("Volume (5d avg)", f"z {px['vol5_z']:+.1f}", px["vol5_z"], 0, "prices")
    if kind == "kr" and coh.get("ok"):
        by = {c["key"]: c for c in coh["cohorts"]}
        if "retail_net" in by:
            c = by["retail_net"]
            row("Retail net-buy (20d cum)", fmt_krw(c["cum20"]), c.get("z5"), +1, "asia-prints",
                note="z is of the 5d flow")
        if "foreign_net" in by:
            c = by["foreign_net"]
            row("Foreign net-buy (20d cum)", fmt_krw(c["cum20"]), c.get("z5"), 0, "asia-prints",
                note="z is of the 5d flow")
    if kind == "tw" and coh.get("ok"):
        by = {c["key"]: c for c in coh["cohorts"]}
        if "foreign_net" in by:
            c = by["foreign_net"]
            row("Foreign net-buy (20d cum, shares)", f"{c['cum20'] / 1e6:+.1f}M", c.get("z5"), 0,
                "asia-prints", note="z is of the 5d flow")
    if kind in ("kr",) and margin and margin.get("z") is not None:
        row("KR margin balance (market)", fmt_krw(margin["level"], signed=False), margin["z"], +1,
            "asia-prints", margin.get("asof"))
    if kind == "us" and meta:
        si = meta.get("si") or {}
        if si.get("pct_float"):
            row("Short interest % float", f"{si['pct_float'] * 100:.1f}%", None, 0, "short-borrow",
                si.get("asof"), "bi-monthly, level only")
        if si.get("days_to_cover"):
            row("Days to cover", f"{si['days_to_cover']:.1f}", None, 0, "short-borrow", si.get("asof"))
    if kind == "us" and opt and opt.get("ok"):
        if opt.get("pc_oi") is not None:
            # pre-registered level rule: P/C OI < 0.7 call-crowded (+0.5), > 1.3 put-heavy (-0.5)
            lvl = 0.5 if opt["pc_oi"] < 0.7 else (-0.5 if opt["pc_oi"] > 1.3 else 0.0)
            rows.append({"label": "Put/Call OI (near expiry)", "value": f"{opt['pc_oi']:.2f}",
                         "z": None, "orient": 0, "group": "options", "asof": None,
                         "note": f"level rule adds {lvl:+.1f}" if lvl else ""})
            if lvl:
                score_in.append(lvl)
        if opt.get("atm_iv") is not None and px.get("rv20"):
            spread = opt["atm_iv"] - px["rv20"]
            row("ATM IV minus RV20", f"{spread * 100:+.1f} vol pts", None, 0, "options",
                note="complacency gauge, level only")
    if name == "COMPLEX":
        soxl = next((r for r in suite if r["etf"] == "SOXL"), None)
        if soxl:
            row("SOXL AUM", fmt_usd(soxl["aum"]), None, 0, "etf-flows", dt.date.today().isoformat(),
                "own archive arming (z after ~60 snapshots)")
        if engine.get("naaim"):
            na = engine["naaim"]
            row("NAAIM exposure (market)", f"{na['value']:.0f}", na.get("z"), +1, "context", na.get("asof"))
        if engine.get("cot_nq"):
            ct = engine["cot_nq"]
            row("COT NQ non-commercial net", f"{ct['value']:,.0f}", ct.get("z"), +1, "context", ct.get("asof"))
        if margin and margin.get("z") is not None:
            row("KR margin balance", fmt_krw(margin["level"], signed=False), margin["z"], +1,
                "asia-prints", margin.get("asof"))
    score = statistics.fmean(score_in) if score_in else None
    if score is None:
        v = verdict("UNARMED", "neutral", "N/A", "No z-scored crowd inputs armed yet for this name")
    elif score >= CROWD_HI:
        v = verdict("CROWDED-LONG", "warn", "MIXED-MED",
                    f"Crowd score {score:+.2f} (>= {CROWD_HI}) — dense positioning, violent resolution risk",
                    "Crowd density sets HOW VIOLENTLY anything resolves, not direction.",
                    f"Score decaying below {CROWD_HI} on margin/retail unwind.",
                    [f"{len(score_in)} armed inputs, equal-weighted (pre-registered)"])
    elif score <= CROWD_LO:
        v = verdict("WASHED-OUT", "good", "MIXED-MED",
                    f"Crowd score {score:+.2f} (<= {CROWD_LO}) — positioning flushed",
                    "Washed-out crowds mean forced sellers are spent; asymmetry improves.",
                    "Score re-rising while price falls = fresh crowding into weakness.",
                    [f"{len(score_in)} armed inputs, equal-weighted"])
    else:
        v = verdict("NEUTRAL", "neutral", "MIXED-MED", f"Crowd score {score:+.2f} — no density extreme",
                    "", "", [f"{len(score_in)} armed inputs of {len(rows)} displayed"])
    return v, {"rows": rows, "score": score}


def q5_priced(name: str, kind: str, px: dict, meta: dict | None, opt: dict | None,
              past_moves: list[float], smh_px: dict, kr_earn: dict | None) -> tuple[dict, dict]:
    """Q5: the expectations bar — implied vs realized event moves, run-up, revisions."""
    data: dict = {}
    ev = []
    earn_date, days_to = None, None
    if kind == "us" and meta:
        cand = [meta.get("next_earnings"), meta.get("next_earnings_alt")]
        cand = [c for c in cand if c]
        if cand:
            earn_date = min(cand)
            days_to = (dt.date.fromisoformat(earn_date) - dt.date.today()).days
            if len(set(cand)) > 1:
                ev.append(f"Earnings date sources disagree ({' vs '.join(sorted(set(cand)))}) — using earlier")
    elif kr_earn:
        earn_date, days_to = kr_earn["date"], (dt.date.fromisoformat(kr_earn["date"]) - dt.date.today()).days
        ev.append(f"Earnings from ffcal overrides: {kr_earn['label']}")
    data["earnings"] = {"date": earn_date, "days": days_to}

    implied = realized = None
    if opt and opt.get("event"):
        implied = opt["event"]["move"]
        data["implied"] = opt["event"]
        ev.append(f"Straddle-implied move to {opt['event']['expiry']}: {fmt_pct(implied, signed=False)} "
                  f"({opt['event']['days']}d, includes ambient drift)")
    elif opt and opt.get("ambient"):
        data["implied"] = opt["ambient"]
        ev.append(f"Ambient straddle ({opt['ambient']['expiry']}): "
                  f"{fmt_pct(opt['ambient']['move'], signed=False)} — no event expiry listed yet")
    if past_moves:
        realized = statistics.fmean([abs(m) for m in past_moves])
        data["realized"] = {"avg_abs": realized, "n": len(past_moves), "moves": past_moves}
        ev.append(f"Realized reaction, last {len(past_moves)} prints: avg |{fmt_pct(realized, signed=False)}| "
                  f"(close-to-close after report; AMC approximation)")
    runup = px.get("ret20")
    resid = None
    if runup is not None and smh_px.get("ret20") is not None:
        resid = runup - smh_px["ret20"]
        ev.append(f"Run-up into the event: 20d {fmt_pct(runup)} ({fmt_pct(resid)} vs SMH)")
    data["runup"] = {"ret20": runup, "resid20": resid, "z": px.get("ret20_z")}
    rev = (meta or {}).get("rev30") or {}
    if rev:
        parts = [f"{k}: {fmt_pct(v)}" for k, v in rev.items()]
        ev.append("EPS estimate drift 30d — " + ", ".join(parts))
    data["rev30"] = rev

    # pre-registered bar score: z(run-up resid proxy) + 0.5*sign(revisions)
    bar = 0.0
    armed = 0
    if px.get("ret20_z") is not None:
        bar += px["ret20_z"]
        armed += 1
    if rev.get("0y") is not None:
        bar += 0.5 * (1 if rev["0y"] > 0.005 else (-1 if rev["0y"] < -0.005 else 0))
        armed += 1
    label, chip = ("UNARMED", "neutral") if not armed else (
        ("BAR HIGH", "warn") if bar >= 1.0 else ("BAR LOW", "good") if bar <= -1.0 else ("BAR NEUTRAL", "neutral"))
    hyp = ("A priced record is a sell; the bar is what moves the stock, not the level. "
           "Score = run-up z + revision kick (pre-registered).")
    headline = f"{label.title()} (score {bar:+.1f})"
    if days_to is not None:
        headline += f" — {days_to}d to earnings"
    if implied is not None and realized:
        win = (data.get("implied") or {}).get("days", 99)
        if win <= 15:  # near-event straddle: the event premium dominates, comparison is fair
            rel = "above" if implied > realized else "below"
            headline += f"; implied {fmt_pct(implied, signed=False)} {rel} realized {fmt_pct(realized, signed=False)}"
        else:
            headline += (f"; straddle {fmt_pct(implied, signed=False)} over {win}d "
                         f"(ambient-vol-dominated, not an event read yet)")
    v = verdict(label, chip, "MIXED-MED" if armed else "N/A", headline, hyp,
                "Post-print: grade reaction vs this bar, not vs the fundamental level.", ev)
    return v, data


# ------------------------------------------------------------------ flags & assembly


def compute_flags(names_state: dict) -> list[dict]:
    """Design section-4 flag rules over the armed feeds."""
    flags = []
    for nid, st in names_state.items():
        cand = []  # (feed_label, group, z)
        coh = (st.get("q1data") or {}).get("cohort")
        if coh:
            for c in coh["cohorts"]:
                if c.get("z5") is not None:
                    cand.append((f"{c['label']} 5d flow", "asia-prints", c["z5"]))
        svr = (st.get("q1data") or {}).get("svr")
        if svr and svr.get("z") is not None:
            cand.append(("short-volume ratio", "short-borrow", svr["z"]))
        px = st.get("px") or {}
        pz = px.get("ret5_z")
        for label, grp, z in cand:
            if abs(z) >= FLAG_SINGLE:
                flags.append({"name": nid, "feed": label, "group": grp, "z": z, "rule": "single |z|>=3",
                              "text": f"{nid}: {label} z={z:+.1f}"})
        strong = [(la, g, z) for la, g, z in cand if abs(z) >= FLAG_DUAL]
        groups = {g for _, g, _ in strong}
        if len(strong) >= 2 and len(groups) >= 2:
            det = ", ".join(f"{la} z={z:+.1f}" for la, _, z in strong[:3])
            flags.append({"name": nid, "feed": "cross-group", "group": "+".join(sorted(groups)),
                          "z": max(abs(z) for _, _, z in strong), "rule": "dual-group |z|>=2",
                          "text": f"{nid}: {det}"})
        # divergence tells
        if pz is not None and abs(pz) >= 2 and coh:
            confirmed = any(abs(c.get("z5") or 0) >= 1 for c in coh["cohorts"])
            if not confirmed:
                flags.append({"name": nid, "feed": "price-without-cohort", "group": "divergence",
                              "z": pz, "rule": "divergence tell",
                              "text": f"{nid}: price z={pz:+.1f} without cohort confirmation"})
        if coh:
            by = {c["key"]: c for c in coh["cohorts"]}
            f, r = by.get("foreign_net"), by.get("retail_net")
            if f and r and (px.get("ret5") or 0) >= 0 and (f.get("z5") or 0) <= -1.5 and (r.get("z5") or 0) >= 1.5:
                flags.append({"name": nid, "feed": "retail-absorbs-foreign-distribution", "group": "divergence",
                              "z": f["z5"], "rule": "divergence tell",
                              "text": f"{nid}: foreign z={f['z5']:+.1f} selling into strength, retail z={r['z5']:+.1f} absorbing"})
    return flags


def build_state(args) -> dict:
    """Pull everything, compute the five questions per name, assemble the panel state."""
    offline = args.offline
    asof = dt.date.fromisoformat(args.asof) if args.asof else dt.date.today()
    t86_n = 15 if args.quick else 60
    finra_n = 10 if args.quick else 30

    print("[1/6] prices (yfinance)...")
    us_all = US_FOCUS + US_CONTEXT + ["SOXL"]
    px_raw = pull_us_prices(us_all + ["2330.TW", "2454.TW", "^KS11"], offline)
    live = pull_us_intraday(US_FOCUS + ["SOXX"], offline)

    print("[2/6] Asia anchors (Naver KR cohort, KOFIA margin, TWSE T86)...")
    kr_coh = {c: pull_kr_cohort(c, offline) for c in KR_NAMES}
    kofia = pull_kofia_margin(offline)
    tw_coh = {c: pull_tw_cohort(c, offline, sessions=t86_n) for c in TW_NAMES}

    print("[3/6] US inference layer (FINRA short volume, options, meta)...")
    svr = pull_finra_shortvol(US_FOCUS, offline, days=finra_n)
    metas = {t: pull_us_meta(t, offline) for t in US_FOCUS}
    suite = pull_letf_suite(offline)
    engine = pull_engine_context()

    print("[4/6] calendar (ffcal)...")
    cal_days = pull_ffcal(asof, horizon=args.horizon)
    kr_earn_map = {}
    # KR/TW earnings from ffcal overrides live in the events (feed F8/F15)
    try:
        sys.path.insert(0, str(FFCAL_DIR))
        import ffcal
        ov = ffcal.load_overrides()
        for e in ov.get("earnings", []):
            tk = str(e.get("ticker", ""))
            d0 = e.get("date")
            if tk.endswith(".KS") and d0 and dt.date.fromisoformat(str(d0)) >= asof:
                code = tk.split(".")[0]
                if code not in kr_earn_map or str(d0) < kr_earn_map[code]["date"]:
                    kr_earn_map[code] = {"date": str(d0), "label": e.get("label", "")}
    except Exception:
        pass

    print("[5/6] computing the five questions...")
    # margin pack
    margin = None
    if not kofia.empty:
        tot = kofia["total"].astype(float)
        ks11 = px_series(px_raw.get("^KS11"))
        margin = {"level": float(tot.iloc[-1]), "z": zscore(tot.tolist(), 250),
                  "d5": float(tot.iloc[-1] - tot.iloc[-6]) if len(tot) > 6 else None,
                  "asof": kofia["date"].iloc[-1].isoformat(),
                  "kospi_ret1": ks11.get("ret1") if ks11.get("ok") else None,
                  "series": {"dates": [d.isoformat() for d in kofia["date"].iloc[-120:]],
                             "total": [float(x) for x in tot.iloc[-120:]]}}

    smh = px_series(px_raw.get("SMH"))
    # reference day-returns for the MOC arithmetic
    ref_rets, is_live = {}, {}
    for ref in ["SOXX"] + US_FOCUS:
        pk = px_series(px_raw.get(ref))
        if not pk.get("ok"):
            continue
        r, lv = pk["ret1"], False
        li = live.get(ref)
        if li and li["session_date"] > pk["date"]:
            prev = pk["last"]
            r, lv = li["px"] / prev - 1, True
        elif li and li["session_date"] == pk["date"]:
            lv = False  # completed session
        ref_rets[ref], is_live[ref] = r, lv

    names_state: dict[str, dict] = {}

    def past_reaction_moves(tkr: str) -> list[float]:
        df, meta = px_raw.get(tkr), metas.get(tkr) or {}
        if df is None or df.empty:
            return []
        closes = df["Close"]
        moves = []
        for ds in (meta.get("past_earnings") or [])[:8]:
            d0 = pd.Timestamp(ds)
            idx = closes.index.tz_localize(None) if closes.index.tz is not None else closes.index
            pos = idx.searchsorted(d0)
            if pos + 1 < len(closes) and pos > 0:
                # AMC convention: reaction = next session vs report-day close
                moves.append(float(closes.iloc[pos + 1] / closes.iloc[pos] - 1))
        return moves

    # --- US focus names
    for tkr in US_FOCUS:
        pk = px_series(px_raw.get(tkr))
        meta = metas.get(tkr) or {}
        earn = meta.get("next_earnings") or meta.get("next_earnings_alt")
        earn_d = dt.date.fromisoformat(earn) if earn else None
        opt = pull_options(tkr, pk.get("last"), earn_d, offline)
        v1, d1 = q1_attribution(tkr, "us", pk, {}, svr.get(tkr), smh)
        v3, d3 = q3_forced_next(tkr, suite, ref_rets, cal_days, None,
                                {"gex_per_pct": opt.get("gex_per_pct"), "gex_flip": opt.get("gex_flip")},
                                {"is_live": is_live.get(tkr)})
        v2 = q2_whose_shares(tkr, "us", pk, {}, None, d3["moc_rows"])
        v4, d4 = q4_crowd(tkr, "us", pk, {}, meta, opt, None, engine, suite)
        v5, d5 = q5_priced(tkr, "us", pk, meta, opt, past_reaction_moves(tkr), smh, None)
        names_state[tkr] = {"id": tkr, "label": tkr, "tape": "US", "kind": "us", "px": pk,
                            "verdicts": {"q1": v1, "q2": v2, "q3": v3, "q4": v4, "q5": v5},
                            "q1data": d1, "q3data": d3, "q4data": d4, "q5data": d5,
                            "opt": {k: opt.get(k) for k in ("pc_oi", "pc_vol", "atm_iv", "gex_per_pct", "gex_flip")},
                            "live": {"ret": ref_rets.get(tkr), "is_live": is_live.get(tkr)}}

    # --- KR measured anchors
    for code, label in KR_NAMES.items():
        df = kr_coh.get(code, pd.DataFrame())
        if df.empty:
            continue
        pk = kr_px_pack(df)
        coh = cohort_pack(df, [("foreign_net", "Foreign"), ("inst_net", "Institution"),
                               ("retail_net", "Retail")], "KRW")
        v1, d1 = q1_attribution(code, "kr", pk, coh, None, smh)
        v3, d3 = q3_forced_next(code, [], {}, cal_days, margin, None, None)
        v2 = q2_whose_shares(code, "kr", pk, coh, margin, [])
        v4, d4 = q4_crowd(code, "kr", pk, coh, None, None, margin, engine, suite)
        v5, d5 = q5_priced(code, "kr", pk, None, None, [], smh, kr_earn_map.get(code))
        fh = df["foreign_hold"].dropna()
        names_state[code] = {"id": code, "label": f"{label} ({code})", "tape": "KR", "kind": "kr",
                             "px": pk, "verdicts": {"q1": v1, "q2": v2, "q3": v3, "q4": v4, "q5": v5},
                             "q1data": d1, "q3data": d3, "q4data": d4, "q5data": d5,
                             "foreign_hold": {"last": float(fh.iloc[-1]) if not fh.empty else None,
                                              "d20": float(fh.iloc[-1] - fh.iloc[-20]) if len(fh) > 20 else None}}

    # --- TW measured anchors
    for code, label in TW_NAMES.items():
        tdf = tw_coh.get(code, pd.DataFrame())
        ydf = px_raw.get(f"{code}.TW")
        pk = px_series(ydf)
        coh = {}
        if not tdf.empty:
            coh = cohort_pack(tdf, [("foreign_net", "Foreign"), ("trust_net", "Inv-trust"),
                                    ("dealer_net", "Dealer")], "shares")
        v1, d1 = q1_attribution(code, "tw", pk, coh, None, smh)
        v3, d3 = q3_forced_next(code, [], {}, cal_days, None, None, None)
        v2 = q2_whose_shares(code, "tw", pk, coh, None, [])
        v4, d4 = q4_crowd(code, "tw", pk, coh, None, None, None, engine, suite)
        v5, d5 = q5_priced(code, "tw", pk, None, None, [], smh, None)
        names_state[code] = {"id": code, "label": f"{label} ({code})", "tape": "TW", "kind": "tw",
                             "px": pk, "verdicts": {"q1": v1, "q2": v2, "q3": v3, "q4": v4, "q5": v5},
                             "q1data": d1, "q3data": d3, "q4data": d4, "q5data": d5}

    # --- complex view
    smh_pack = smh
    breadth_rows = []
    for nid, st in names_state.items():
        p = st["px"]
        if p.get("ok") and p.get("ret5") is not None:
            resid = p["ret5"] - smh_pack["ret5"] if smh_pack.get("ret5") is not None else None
            breadth_rows.append({"name": st["label"], "id": nid, "tape": st["tape"],
                                 "ret5": p["ret5"], "ret20": p.get("ret20"), "resid5": resid})
    breadth_rows.sort(key=lambda r: r.get("resid5") or 0)
    v3c, d3c = q3_forced_next("COMPLEX", suite, ref_rets, cal_days, margin, None,
                              {"is_live": is_live.get("SOXX")})
    v4c, d4c = q4_crowd("COMPLEX", "complex", smh_pack, {}, None, None, margin, engine, suite)
    anchors = []
    for aid in ["005930", "000660", "2330"]:
        if aid in names_state:
            a = names_state[aid]
            anchors.append({"id": aid, "label": a["label"], "q1": a["verdicts"]["q1"]["headline"],
                            "q2": a["verdicts"]["q2"]["verdict"], "ret5": a["px"].get("ret5")})
    complex_state = {"id": "COMPLEX", "label": "Semis complex", "tape": "US+ASIA", "kind": "complex",
                     "px": smh_pack,
                     "verdicts": {"q3": v3c, "q4": v4c},
                     "q3data": d3c, "q4data": d4c,
                     "breadth": breadth_rows, "anchors": anchors, "margin": margin}

    print("[6/6] flags + assembly...")
    flags = compute_flags(names_state)
    armed_groups = sorted({f.group for f in FEEDS if f.ok and f.group in GROUPS})
    state = {
        "generated": now_kst().strftime("%Y-%m-%d %H:%M KST"),
        "asof": asof.isoformat(),
        "feeds": [vars(f) for f in FEEDS],
        "armed_groups": armed_groups,
        "groups_total": len(GROUPS),
        "names_order": [n for n in ["NVDA", "AMD", "MU"] if n in names_state]
                       + [n for n in KR_NAMES if n in names_state]
                       + [n for n in TW_NAMES if n in names_state],
        "names": names_state,
        "complex": complex_state,
        "calendar": cal_days,
        "flags": flags,
        "contract": ("This tool detects POSITIONING and PRESSURE, not intent. Every attribution is a "
                     "hypothesis with a confidence and a falsifier — never a bare 'institutions bought'. "
                     "(The MU 2026-06-23 lesson: a cascade that looked exactly like informed selling.)"),
        "aum_history_days": len(list(AUMDIR.glob("aum-*.json"))),
    }
    return state


# ------------------------------------------------------------------------ brief


def render_brief(state: dict) -> str:
    L = []
    L.append(f"FLOW READ — {state['generated']} (as of {state['asof']})")
    fr = {f["name"]: f for f in state["feeds"]}
    fl = []
    for key, lab in (("us-prices", "US"), ("kr-cohort:005930", "KR prints"),
                     ("tw-cohort:2330", "TW prints"), ("kr-margin", "KR margin"),
                     ("finra-shortvol", "FINRA")):
        f = fr.get(key)
        fl.append(f"{lab} {f['asof'] or 'FAIL'}" if f else f"{lab} -")
    L.append("data: " + " | ".join(fl) + f" | evidence groups armed: {len(state['armed_groups'])}/{state['groups_total']}")
    L.append("-" * 78)
    for nid in state["names_order"]:
        if nid not in state["names"]:
            continue
        st = state["names"][nid]
        if nid not in BRIEF_NAMES:
            continue
        p = st["px"]
        vs = st["verdicts"]
        px_s = f"{p.get('last'):,.0f}" if st["kind"] != "us" else f"${p.get('last'):,.2f}"
        L.append(f"{st['label']:<28} {px_s:>10}  5d {fmt_pct(p.get('ret5')):>7}  20d {fmt_pct(p.get('ret20')):>7}")
        L.append(f"  Q1 owned-by : {vs['q1']['headline']}")
        L.append(f"  Q2 shares   : [{vs['q2']['verdict']}] {vs['q2']['headline']}")
        L.append(f"  Q3 forced   : {vs['q3']['headline']}")
        L.append(f"  Q4 crowd    : [{vs['q4']['verdict']}] {vs['q4']['headline']}")
        L.append(f"  Q5 priced   : {vs['q5']['headline']}")
    c = state["complex"]
    L.append("-" * 78)
    L.append(f"COMPLEX  Q3: {c['verdicts']['q3']['headline']}")
    L.append(f"         Q4: [{c['verdicts']['q4']['verdict']}] {c['verdicts']['q4']['headline']}")
    if state["flags"]:
        L.append(f"FLAGS ({len(state['flags'])}):")
        for f in state["flags"][:8]:
            L.append(f"  ! [{f['rule']}] {f['text']}")
    else:
        L.append("FLAGS: none fired (|z|>=3 single / |z|>=2 dual-group / divergence tells)")
    nxt = []
    for d in state["calendar"][:5]:
        big = [e["label"] for e in d["events"] if e["size"] in ("L", "XL") and not e.get("span")]
        if big:
            nxt.append(f"{d['date'][5:]} {d['dow']}: " + "; ".join(big[:3]))
    if nxt:
        L.append("CALENDAR: " + " | ".join(nxt[:4]))
    L.append(f"contract: positioning & pressure, never intent — hypotheses carry falsifiers.")
    return "\n".join(L)


# --------------------------------------------------------------------- selftest


def selftest() -> int:
    ok = True

    def check(cond, msg):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + msg)
        ok = ok and bool(cond)

    # L4 arithmetic anchors (design section 11 worked example)
    k3 = 3.0 * 3.0 - 3.0
    check(k3 == 6.0, "L=3 -> (L^2-L) = 6")
    check((-3.0) ** 2 - (-3.0) == 12.0, "L=-3 -> (L^2-L) = 12")
    check(abs(k3 * 26e9 * 0.02 - 3.12e9) < 1e6, "SOXL $26B @ +2% -> ~$3.12B MOC buy")
    check(_leverage_from_name("Direxion Daily Semiconductor Bear 3X Shares", 3.0) == -3.0, "bear-3x name parse")
    check(_leverage_from_name("GraniteShares 2x Long NVDA Daily ETF", 2.0) == 2.0, "2x-long name parse")
    # parsing
    check(parse_num("-2,018,562") == -2018562.0, "signed comma number")
    check(parse_num("+625,985") == 625985.0, "plus-signed number")
    # z-score
    z = zscore([0.0] * 59 + [1.0] + [10.0], win=60)
    check(z is not None and z > 3, "z-score fires on an outlier")
    # flag rules truth table
    st = {"X": {"px": {"ret5_z": 0.5},
                "q1data": {"cohort": {"cohorts": [
                    {"key": "foreign_net", "label": "Foreign", "z5": 3.4, "cum5": -1, "streak": -4},
                    {"key": "retail_net", "label": "Retail", "z5": 1.0, "cum5": 1, "streak": 2}]},
                           "svr": {"z": 2.2}}}}
    fl = compute_flags(st)
    check(any(f["rule"] == "single |z|>=3" for f in fl), "single-feed |z|>=3 fires")
    check(any(f["rule"] == "dual-group |z|>=2" for f in fl), "dual-group |z|>=2 fires (asia-prints x short-borrow)")
    st2 = {"X": {"px": {"ret5_z": 0.5},
                 "q1data": {"cohort": {"cohorts": [
                     {"key": "foreign_net", "label": "Foreign", "z5": 2.2, "cum5": -1, "streak": -1},
                     {"key": "inst_net", "label": "Institution", "z5": 2.4, "cum5": 1, "streak": 1}]}}}}
    fl2 = compute_flags(st2)
    check(not any(f["rule"] == "dual-group |z|>=2" for f in fl2), "same-group 2.2/2.4 does NOT dual-fire")
    st3 = {"X": {"px": {"ret5_z": 2.5, "ret5": 0.01},
                 "q1data": {"cohort": {"cohorts": [
                     {"key": "foreign_net", "label": "Foreign", "z5": -1.6, "cum5": -1, "streak": -3},
                     {"key": "retail_net", "label": "Retail", "z5": 1.7, "cum5": 1, "streak": 3}]}}}}
    fl3 = compute_flags(st3)
    check(any(f["rule"] == "divergence tell" for f in fl3), "divergence tells fire")
    # streak
    check(_streak(pd.Series([1, 2, -1, -2, -3])) == -3, "streak sign/length")
    print("selftest:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


# ------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="flowmap — the five-question flow read")
    sub = ap.add_subparsers(dest="cmd")
    rd = sub.add_parser("read", help="pull + compute + dashboard (default)")
    rd.add_argument("--quick", action="store_true", help="shallow backfills (T86 15d, FINRA 10d)")
    rd.add_argument("--offline", action="store_true", help="caches/lake only, no network")
    rd.add_argument("--no-open", action="store_true", help="do not open the dashboard")
    rd.add_argument("--asof", default=None, help="calendar as-of date YYYY-MM-DD")
    rd.add_argument("--horizon", type=int, default=10)
    sub.add_parser("selftest", help="arithmetic anchors, no network")
    args = ap.parse_args()
    if args.cmd == "selftest":
        return selftest()
    if args.cmd is None:
        args = ap.parse_args(["read"])

    for d in (STORE, CACHE, SNAPS, AUMDIR):
        d.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    state = build_state(args)

    brief = render_brief(state)
    print()
    print(brief)

    from webui import render_dashboard
    html = render_dashboard(state)
    out = STORE / "dashboard.html"
    out.write_text(html, encoding="utf-8")

    snap = SNAPS / f"read-{now_kst():%Y%m%d-%H%M}.json"
    snap.write_text(json.dumps(jsonify({**state, "grade": None, "graded_at": None}),
                               ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {out}")
    print(f"wrote {snap}  ({time.time() - t0:.0f}s total)")
    if not args.no_open:
        webbrowser.open(out.as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
