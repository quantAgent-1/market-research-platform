"""Thread-safe token-bucket rate limiter.

Alpaca's Algo Trader Plus market-data limit is a hard 10,000 requests/min,
enforced per *account* (extra API keys do not raise it). We default to 9,000/min
for headroom. The bucket refills continuously, smoothing bursts instead of
clipping at minute boundaries, and is thread-safe so parallel backfills share one
limiter.
"""
from __future__ import annotations

import threading
import time


class TokenBucket:
    def __init__(self, rate_per_min: int, burst: int | None = None):
        self.rate_per_sec = rate_per_min / 60.0
        # default burst ~= one second's worth of tokens
        self.capacity = float(burst if burst is not None else max(1, round(self.rate_per_sec)))
        self._tokens = self.capacity
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, n: int = 1) -> None:
        """Block until *n* tokens are available, then consume them."""
        while True:
            with self._lock:
                now = time.monotonic()
                self._tokens = min(
                    self.capacity, self._tokens + (now - self._last) * self.rate_per_sec
                )
                self._last = now
                if self._tokens >= n:
                    self._tokens -= n
                    return
                wait = (n - self._tokens) / self.rate_per_sec
            time.sleep(max(wait, 0.0))
