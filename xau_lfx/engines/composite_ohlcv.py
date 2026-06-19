from __future__ import annotations

from statistics import median
from typing import Any

from xau_lfx.config import DEFAULT_TIMEFRAMES, PRIMARY_TIMEFRAME
from xau_lfx.utils import utc_now_iso


def _collect_ohlcv(raw_scan: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    for payload in raw_scan.get("source_payloads", []):
        if payload.get("source_id") == "MT5_CSV":
            source_payload = payload.get("payload", {})
            if isinstance(source_payload, dict):
                ohlcv = source_payload.get("ohlcv", {})
                return ohlcv if isinstance(ohlcv, dict) else {}
    return {}


def _normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: row["ts_utc"])


def build_composite_ohlcv(raw_scan: dict, data_quality: dict) -> dict:
    ohlcv = _collect_ohlcv(raw_scan)
    timeframe_bars = {tf: _normalize_rows(ohlcv.get(tf, [])) for tf in DEFAULT_TIMEFRAMES if ohlcv.get(tf)}
    primary_bars = timeframe_bars.get(PRIMARY_TIMEFRAME, [])
    latest_by_timeframe = {
        tf: rows[-1] for tf, rows in timeframe_bars.items() if rows
    }
    closes = [float(row["close"]) for row in latest_by_timeframe.values()]
    median_close = median(closes) if closes else None

    flags = list(data_quality.get("quality_flags", []))
    if not primary_bars:
        flags.append("NO_M15_PRIMARY_BARS")
    if len(timeframe_bars) < len(DEFAULT_TIMEFRAMES):
        flags.append("COMPOSITE_MTF_INCOMPLETE")

    return {
        "ts_utc": utc_now_iso(),
        "symbol": raw_scan.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "timeframes": list(DEFAULT_TIMEFRAMES),
        "mtf_rule": "M15_STRATEGIC__M5_CONFIRMATION_ONLY__H1_CONTEXT_ONLY",
        "primary_timeframe": PRIMARY_TIMEFRAME,
        "bars": primary_bars,
        "timeframe_bars": timeframe_bars,
        "latest_by_timeframe": latest_by_timeframe,
        "median_latest_close": median_close,
        "volume_policy": "tick_volume is retained as broker activity proxy only",
        "confidence_cap": data_quality.get("confidence_cap", 0.0),
        "quality_flags": sorted(set(flags)),
    }
