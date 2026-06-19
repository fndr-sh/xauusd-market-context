from __future__ import annotations

from typing import Any

from xau_lfx.config import PRIMARY_TIMEFRAME
from xau_lfx.utils import parse_iso_utc, utc_now_iso

SESSION_BUCKETS = {
    "ASIA": (0, 7 * 60),
    "LONDON": (7 * 60, 12 * 60 + 30),
    "NY": (12 * 60 + 30, 19 * 60),
}


def _session_name(ts_utc: str) -> str:
    parsed = parse_iso_utc(ts_utc)
    minutes = parsed.hour * 60 + parsed.minute
    for name, (start, end) in SESSION_BUCKETS.items():
        if start <= minutes < end:
            return name
    return "OFF_SESSION"


def _summarize_session(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {name: [] for name in [*SESSION_BUCKETS.keys(), "OFF_SESSION"]}
    for row in rows:
        grouped[_session_name(row["ts_utc"])].append(row)
    summary: dict[str, Any] = {}
    for name, session_rows in grouped.items():
        if not session_rows:
            continue
        highs = [float(row["high"]) for row in session_rows]
        lows = [float(row["low"]) for row in session_rows]
        closes = [float(row["close"]) for row in session_rows]
        summary[name] = {
            "bar_count": len(session_rows),
            "high": max(highs),
            "low": min(lows),
            "last_close": closes[-1],
            "range_points": round(max(highs) - min(lows), 4),
        }
    return summary


def build_session_context(data_quality: dict, composite: dict | None = None) -> dict:
    composite = composite or {}
    primary_rows = composite.get("bars", [])
    session_ranges = _summarize_session(primary_rows) if primary_rows else {}
    flags = list(data_quality.get("quality_flags", []))
    if not session_ranges:
        flags.append("SESSION_CONTEXT_NO_SOURCE_MODE")

    return {
        "ts_utc": utc_now_iso(),
        "symbol": data_quality.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "session_state": "CONTEXT" if session_ranges else "RESEARCH_ONLY",
        "primary_timeframe": composite.get("primary_timeframe", PRIMARY_TIMEFRAME),
        "session_ranges": session_ranges,
        "handoff_state": "CONTEXT_ONLY" if session_ranges else "RESEARCH_ONLY",
        "confidence_cap": data_quality.get("confidence_cap", 0.0),
        "quality_flags": sorted(set(flags)),
    }
