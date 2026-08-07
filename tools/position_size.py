#!/usr/bin/env python3
"""
position_size.py - volatility-scaled stop + risk-based position sizing.

For each ticker it pulls daily prices (yfinance), computes ATR(14), and prints a
volatility-scaled stop plus the share count that risks a fixed % of the account
if that stop is hit:

    stop$  = atr_mult * ATR$            (long stop = price - stop$)
    shares = (account * risk%) / stop$
    a normal 1-ATR day moves the account ~ risk% / atr_mult

Usage:
    python tools/position_size.py NVDA MU INTC --account 100000 --risk 1 --atr-mult 2

Educational risk-sizing helper, NOT financial advice. It caps loss-per-trade and
makes normal noise tolerable; it does not make a trade profitable, and a stop does
not protect against overnight/earnings gaps. Console output is forced to UTF-8
(this machine's console codepage is cp949).
"""
import sys
import argparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import pandas as pd
import yfinance as yf


def _col(d, name, t):
    """Return a 1-D Series for column `name`, handling yfinance MultiIndex frames."""
    s = d[name]
    if isinstance(s, pd.DataFrame):
        return s[t] if t in s.columns else s.iloc[:, 0]
    return s


def analyze(t, account, risk_pct, k, period):
    d = yf.download(t, period=period, interval="1d", auto_adjust=True, progress=False)
    if d is None or len(d) == 0:
        print(f"\n{t}: no data")
        return
    H, L, C = _col(d, "High", t), _col(d, "Low", t), _col(d, "Close", t)
    pc = C.shift(1)
    tr = pd.concat([H - L, (H - pc).abs(), (L - pc).abs()], axis=1).max(axis=1)
    atr = float(tr.rolling(14).mean().iloc[-1])
    px = float(C.iloc[-1])
    if not (atr > 0 and px > 0):
        print(f"\n{t}: insufficient data for ATR")
        return
    atr_pct = atr / px * 100.0
    stop_d = k * atr
    stop_pct = k * atr_pct
    risk_usd = account * risk_pct / 100.0
    shares = risk_usd / stop_d
    pos_usd = shares * px
    pos_pct = pos_usd / account * 100.0
    atr_day = risk_pct / k  # a 1-ATR day as % of account

    print(f"\n{t}: ${px:,.2f} | ATR(14) ${atr:,.2f} ({atr_pct:.1f}%/day)")
    print(f"  stop {k:g}x ATR = {stop_pct:.0f}%  ->  long stop ${px - stop_d:,.2f}")
    print(f"  risk {risk_pct:g}% of ${account:,.0f} (= ${risk_usd:,.0f})  ->  "
          f"{shares:,.1f} shares = ${pos_usd:,.0f} ({pos_pct:.1f}% of account)")
    print(f"  a normal 1-ATR day moves the account ~{atr_day:.2f}%")


def main():
    ap = argparse.ArgumentParser(
        description="Volatility-scaled stop + risk-based position size (educational, not advice).")
    ap.add_argument("tickers", nargs="+", help="one or more tickers, e.g. NVDA MU INTC")
    ap.add_argument("--account", type=float, default=100_000.0, help="account size in $ (default 100000)")
    ap.add_argument("--risk", type=float, default=1.0, help="%% of account risked per trade (default 1.0)")
    ap.add_argument("--atr-mult", type=float, default=2.0, help="stop distance in ATR multiples (default 2.0)")
    ap.add_argument("--period", default="6mo", help="yfinance window for ATR, e.g. 3mo/6mo/1y (default 6mo)")
    a = ap.parse_args()

    print(f"account ${a.account:,.0f} | risk {a.risk:g}%/trade | stop {a.atr_mult:g}x ATR | ATR window {a.period}")
    print("formula: shares = (account x risk%) / (atr_mult x ATR$)")
    for t in a.tickers:
        try:
            analyze(t.upper(), a.account, a.risk, a.atr_mult, a.period)
        except Exception as e:  # noqa: BLE001 - keep the CLI robust across tickers
            print(f"\n{t}: error - {e}")


if __name__ == "__main__":
    main()
