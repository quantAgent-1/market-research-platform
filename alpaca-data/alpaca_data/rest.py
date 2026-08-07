"""Low-level Alpaca REST client: auth + rate limit + retry + pagination.

We deliberately use raw REST (not alpaca-py) for historical pulls. The SDK
auto-paginates the entire result into memory, which is unsafe for tick
(trades/quotes) data that can run to tens of millions of rows. Here `paginate()`
is a generator, so callers stream pages to disk with bounded memory.
(alpaca-py is still used for the WebSocket streaming layer.)
"""
from __future__ import annotations

import logging
import time
from typing import Any, Iterator

import requests

from .config import Settings
from .ratelimit import TokenBucket

log = logging.getLogger("alpaca_data.rest")

_RETRY_STATUS = {429, 500, 502, 503, 504}


class AlpacaDataClient:
    def __init__(self, settings: Settings, *, max_retries: int = 6, timeout: int = 30):
        self.settings = settings
        self.max_retries = max_retries
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(settings.auth_headers)
        self._session.headers["Accept"] = "application/json"
        self._limiter = TokenBucket(settings.max_requests_per_min)

    def get(self, url: str, params: dict[str, Any] | None = None) -> dict:
        """Single rate-limited GET with retry/backoff. Returns parsed JSON."""
        clean = {k: v for k, v in (params or {}).items() if v is not None}
        attempt = 0
        while True:
            self._limiter.acquire()
            try:
                resp = self._session.get(url, params=clean, timeout=self.timeout)
            except requests.RequestException as exc:
                attempt += 1
                if attempt > self.max_retries:
                    raise
                backoff = min(60.0, 2.0 ** attempt)
                log.warning("network error (%s); retry %d/%d in %.1fs",
                            exc, attempt, self.max_retries, backoff)
                time.sleep(backoff)
                continue

            if resp.status_code in _RETRY_STATUS:
                attempt += 1
                if attempt > self.max_retries:
                    resp.raise_for_status()
                retry_after = resp.headers.get("Retry-After")
                backoff = float(retry_after) if retry_after else min(60.0, 2.0 ** attempt)
                log.warning("HTTP %d on %s; retry %d/%d in %.1fs",
                            resp.status_code, resp.url, attempt, self.max_retries, backoff)
                time.sleep(backoff)
                continue

            if not resp.ok:
                # Non-retryable 4xx (e.g. 401 bad key, 403 not entitled): fail loud.
                raise requests.HTTPError(
                    f"{resp.status_code} {resp.reason} for {resp.url}: {resp.text[:500]}",
                    response=resp,
                )
            return resp.json()

    def paginate(
        self,
        path_or_url: str,
        params: dict[str, Any] | None = None,
        *,
        base: str | None = None,
        max_pages: int | None = None,
    ) -> Iterator[dict]:
        """Yield JSON pages, following `next_page_token` until exhausted.

        `path_or_url` may be an absolute URL or a path joined onto `base`
        (defaults to the market-data URL; pass settings.trading_url for the
        option-contracts endpoint).
        """
        base = (base or self.settings.data_url).rstrip("/")
        url = path_or_url if path_or_url.startswith("http") else f"{base}{path_or_url}"
        params = dict(params or {})
        pages = 0
        while True:
            page = self.get(url, params)
            yield page
            pages += 1
            token = page.get("next_page_token")
            if not token or (max_pages is not None and pages >= max_pages):
                return
            params["page_token"] = token
