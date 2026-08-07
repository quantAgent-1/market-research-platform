"""Real-time capture via alpaca-py's WebSocket streams.

We use alpaca-py here (not raw REST): its StockDataStream / OptionDataStream
handle the auth handshake, msgpack decoding, subscription management, and
reconnection. Incoming messages are buffered and flushed to rotating Parquet
files by a background thread, so disk I/O never blocks the event loop.

Layout:
    stocks/stream/kind=<bars|trades|quotes>/symbol=<S>/date=<d>/part-*.parquet
    options/stream/kind=<trades|quotes>/underlying=<U>/date=<d>/part-*.parquet

Note: each stream.run() blocks its thread, so a single process streams one asset
class. Run stocks and options as two processes (or terminals) for both at once.
"""
from __future__ import annotations

import logging
import threading
import time
from collections import defaultdict
from datetime import datetime, timezone

import pandas as pd

from ..config import get_settings
from ..store import write_df
from ..utils import is_occ, parse_occ

log = logging.getLogger("alpaca_data.stream")


def _model_to_row(msg) -> dict:
    row = {k: v for k, v in vars(msg).items() if not k.startswith("_")}
    if isinstance(row.get("conditions"), list):
        row["conditions"] = ",".join(str(x) for x in row["conditions"])
    return row


class _Buffer:
    """Thread-safe message buffer with size- and time-based flushing."""

    def __init__(self, flush_interval: float = 10.0, max_rows: int = 5000):
        self.flush_interval = flush_interval
        self.max_rows = max_rows
        self._data: dict[tuple, list] = defaultdict(list)
        self._lock = threading.Lock()
        self._seq = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self._thread.start()

    def add(self, key: tuple, row: dict):
        with self._lock:
            self._data[key].append(row)
            over = len(self._data[key]) >= self.max_rows
        if over:
            self.flush()

    def _drain(self):
        with self._lock:
            data, self._data = self._data, defaultdict(list)
            self._seq += 1
            return data, self._seq

    def flush(self):
        data, seq = self._drain()
        stamp = int(time.time() * 1000)
        for (asset, kind, gid, d), rows in data.items():
            if not rows:
                continue
            if asset == "stocks":
                parts = ["stocks", "stream", f"kind={kind}", f"symbol={gid}", f"date={d}"]
            else:
                parts = ["options", "stream", f"kind={kind}", f"underlying={gid}", f"date={d}"]
            write_df(pd.DataFrame(rows), *parts, filename=f"part-{stamp}-{seq}.parquet")

    def _loop(self):
        while not self._stop.wait(self.flush_interval):
            try:
                self.flush()
            except Exception:
                log.exception("stream flush error")

    def stop(self):
        self._stop.set()
        self.flush()


class StreamRecorder:
    def __init__(self, *, flush_interval: float = 10.0, max_rows: int = 5000):
        self.buf = _Buffer(flush_interval, max_rows)

    def _handler(self, asset: str, kind: str):
        async def handler(msg):
            row = _model_to_row(msg)
            sym = row.get("symbol")
            ts = row.get("timestamp")
            d = (ts.astimezone(timezone.utc).date().isoformat()
                 if hasattr(ts, "astimezone") else datetime.now(timezone.utc).date().isoformat())
            if asset == "options":
                gid = parse_occ(sym).underlying if is_occ(str(sym)) else str(sym)
                row["contract"] = sym
                row["underlying"] = gid
            else:
                gid = sym
            self.buf.add((asset, kind, gid, d), row)
        return handler

    def run_stocks(self, symbols, kinds=("bars", "trades", "quotes")):
        from alpaca.data.enums import DataFeed
        from alpaca.data.live import StockDataStream

        s = get_settings()
        stream = StockDataStream(s.api_key, s.api_secret, feed=DataFeed(s.stock_feed))
        syms = [x.upper() for x in symbols]
        if "bars" in kinds:
            stream.subscribe_bars(self._handler("stocks", "bars"), *syms)
        if "trades" in kinds:
            stream.subscribe_trades(self._handler("stocks", "trades"), *syms)
        if "quotes" in kinds:
            stream.subscribe_quotes(self._handler("stocks", "quotes"), *syms)
        log.info("streaming stocks %s (%s) feed=%s", syms, ",".join(kinds), s.stock_feed)
        self._run(stream)

    def run_options(self, contract_symbols, kinds=("trades", "quotes")):
        from alpaca.data.enums import OptionsFeed
        from alpaca.data.live import OptionDataStream

        s = get_settings()
        stream = OptionDataStream(s.api_key, s.api_secret, feed=OptionsFeed(s.options_feed))
        syms = list(contract_symbols)
        if "trades" in kinds:
            stream.subscribe_trades(self._handler("options", "trades"), *syms)
        if "quotes" in kinds:
            stream.subscribe_quotes(self._handler("options", "quotes"), *syms)
        if "bars" in kinds and hasattr(stream, "subscribe_bars"):
            stream.subscribe_bars(self._handler("options", "bars"), *syms)
        log.info("streaming options %d contracts (%s) feed=%s", len(syms), ",".join(kinds), s.options_feed)
        self._run(stream)

    def _run(self, stream):
        self.buf.start()
        try:
            stream.run()
        except KeyboardInterrupt:
            log.info("interrupted — flushing buffers")
        finally:
            self.buf.stop()
