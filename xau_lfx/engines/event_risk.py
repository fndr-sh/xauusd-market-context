from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from xau_lfx.utils import parse_iso_utc, utc_now_iso


def _event_rows(raw_scan: dict[str, Any] | None) -> list[dict[str, Any]]:
    if raw_scan is None:
        return []
    for payload in raw_scan.get("source_payloads", []):
        if payload.get("source_id") == "EVENT_CSV" and isinstance(payload.get("payload"), list):
            return payload["payload"]
    return []


def build_event_risk(data_quality: dict, raw_scan: dict | None = None) -> dict:
    events = _event_rows(raw_scan)
    high_impact_usd = [event for event in events if event.get("currency") == "USD" and event.get("impact") == "HIGH"]
    now = datetime.now(timezone.utc)
    near_high_impact: list[dict[str, Any]] = []
    for event in high_impact_usd:
        try:
            event_ts = parse_iso_utc(event["ts_utc"])
        except (KeyError, ValueError):
            continue
        distance_hours = abs((event_ts - now).total_seconds()) / 3600.0
        if distance_hours <= 24.0:
            near_high_impact.append(event)

    if near_high_impact:
        risk_state = "CAUTION"
        note = "High-impact USD event is inside the local risk window. Confidence is capped; no direction is inferred."
    elif events:
        risk_state = "CONTEXT"
        note = "Event CSV loaded. Events are used only as risk context."
    else:
        risk_state = "CAUTION"
        note = "Event calendar disabled until explicit source is configured."

    flags = list(data_quality.get("quality_flags", []))
    if not events:
        flags.append("EVENT_SOURCE_NOT_CONFIGURED")
    if near_high_impact:
        flags.append("USD_HIGH_IMPACT_EVENT_NEARBY")

    return {
        "ts_utc": utc_now_iso(),
        "symbol": data_quality.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "risk_state": risk_state,
        "event_count": len(events),
        "high_impact_events": high_impact_usd,
        "near_high_impact_events": near_high_impact,
        "note": note,
        "confidence_cap": data_quality.get("confidence_cap", 0.0),
        "quality_flags": sorted(set(flags)),
    }
