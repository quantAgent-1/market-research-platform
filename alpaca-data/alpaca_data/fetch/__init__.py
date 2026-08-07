"""Historical fetchers: one module per Alpaca data family.

Each fetcher takes an AlpacaDataClient, pulls data in resumable chunks, and writes
partitioned Parquet into the lake (updating the incremental catalog as it goes).
"""
from . import contracts, corporate_actions, news, options, stocks

__all__ = ["stocks", "options", "contracts", "news", "corporate_actions"]
