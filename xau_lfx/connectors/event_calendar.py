from __future__ import annotations

from xau_lfx.connectors.base import SourceRequest
from xau_lfx.utils import utc_now_iso


class EventCalendarConnector:
    source_id = "EVENT_CALENDAR_STUB"

    def fetch(self, request: SourceRequest) -> dict:
        return {
            "ts_utc": utc_now_iso(),
            "source_id": self.source_id,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "status": "NO_SOURCE_MODE",
            "payload": [],
            "quality_flags": ["EVENT_CALENDAR_NOT_CONFIGURED", "DUMMY_NO_SOURCE_MODE"],
        }
