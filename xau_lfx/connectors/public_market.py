from __future__ import annotations

from xau_lfx.connectors.base import SourceRequest
from xau_lfx.utils import utc_now_iso


class PublicMarketConnector:
    source_id = "PUBLIC_MARKET_STUB"

    def fetch(self, request: SourceRequest) -> dict:
        return {
            "ts_utc": utc_now_iso(),
            "source_id": self.source_id,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "status": "NO_SOURCE_MODE",
            "payload": [],
            "quality_flags": ["PUBLIC_MARKET_API_NOT_CONFIGURED", "DUMMY_NO_SOURCE_MODE"],
        }
