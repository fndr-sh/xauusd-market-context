from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean
from typing import Any

from xau_lfx.config import DEFAULT_TIMEFRAMES
from xau_lfx.utils import parse_iso_utc, utc_now_iso


def _collect_mt5_payload(raw_scan: dict[str, Any]) -> dict[str, Any] | None:
    for payload in raw_scan.get("source_payloads", []):
        if payload.get("source_id") == "MT5_CSV":
            data = payload.get("payload", {})
            return data if isinstance(data, dict) else None
    return None


def _collect_event_payload(raw_scan: dict[str, Any]) -> list[dict[str, Any]]:
    for payload in raw_scan.get("source_payloads", []):
        if payload.get("source_id") == "EVENT_CSV" and isinstance(payload.get("payload"), list):
            return payload["payload"]
    return []


def _latest_timestamp(ohlcv: dict[str, list[dict[str, Any]]]) -> datetime | None:
    latest: datetime | None = None
    for rows in ohlcv.values():
        for row in rows:
            try:
                ts = parse_iso_utc(row["ts_utc"])
            except (KeyError, ValueError):
                continue
            latest = ts if latest is None or ts > latest else latest
    return latest


def _spread_stability(spread_rows: list[dict[str, Any]]) -> float:
    if not spread_rows:
        return 0.0
    values = [float(row["spread_points"]) for row in spread_rows if "spread_points" in row]
    if not values:
        return 0.0
    avg = mean(values)
    if avg <= 0:
        return 0.0
    spread_range = max(values) - min(values)
    instability = min(spread_range / avg, 1.0)
    return round(max(0.0, 1.0 - instability), 4)


def build_data_quality(raw_scan: dict) -> dict:
    payloads = raw_scan.get("source_payloads", [])
    active_payloads = [p for p in payloads if p.get("payload") and p.get("status") in {"OK", "WARN", "PARTIAL"}]
    flags = list(raw_scan.get("quality_flags", []))
    errors: list[str] = []
    for source in payloads:
        errors.extend(source.get("errors", []))

    mt5_payload = _collect_mt5_payload(raw_scan)
    ohlcv = mt5_payload.get("ohlcv", {}) if mt5_payload else {}
    spread_rows = mt5_payload.get("spread", []) if mt5_payload else []
    event_rows = _collect_event_payload(raw_scan)

    present_timeframes = [tf for tf in DEFAULT_TIMEFRAMES if ohlcv.get(tf)]
    coverage_score = len(present_timeframes) / len(DEFAULT_TIMEFRAMES) if DEFAULT_TIMEFRAMES else 0.0
    if len(present_timeframes) < len(DEFAULT_TIMEFRAMES):
        flags.append("MTF_COVERAGE_INCOMPLETE")
    if len(active_payloads) < 1:
        flags.append("INSUFFICIENT_SOURCE_COVERAGE")

    latest = _latest_timestamp(ohlcv)
    freshness_score = 0.0
    if latest is not None:
        age_hours = max(0.0, (datetime.now(timezone.utc) - latest).total_seconds() / 3600.0)
        freshness_score = max(0.0, min(1.0, 1.0 - age_hours / 72.0))
    else:
        flags.append("NO_VALID_OHLCV_ROWS")

    spread_stability = _spread_stability(spread_rows)
    if not spread_rows:
        flags.append("SPREAD_SOURCE_MISSING")
    elif spread_stability < 0.6:
        flags.append("SPREAD_INSTABILITY_DETECTED")

    usd_high_events = [e for e in event_rows if e.get("currency") == "USD" and e.get("impact") == "HIGH"]
    near_usd_high_events = []
    now = datetime.now(timezone.utc)
    for event in usd_high_events:
        try:
            distance_hours = abs((parse_iso_utc(event["ts_utc"]) - now).total_seconds()) / 3600.0
        except (KeyError, ValueError):
            continue
        if distance_hours <= 24.0:
            near_usd_high_events.append(event)
    news_risk_flag = bool(near_usd_high_events)
    if usd_high_events:
        flags.append("USD_HIGH_IMPACT_EVENT_PRESENT")
    if news_risk_flag:
        flags.append("USD_HIGH_IMPACT_EVENT_NEARBY")

    schema_score = 0.0 if errors or not ohlcv else 1.0
    confidence_cap = min(
        0.75,
        max(0.0, coverage_score * 0.35 + freshness_score * 0.20 + spread_stability * 0.20 + schema_score * 0.25),
    )
    if news_risk_flag:
        confidence_cap = min(confidence_cap, 0.45)

    return {
        "ts_utc": utc_now_iso(),
        "symbol": raw_scan.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "freshness_score": round(freshness_score, 4),
        "coverage_score": round(coverage_score, 4),
        "schema_score": round(schema_score, 4),
        "source_count": len(active_payloads),
        "missing_field_count": len(errors),
        "dispersion_score": 0.0,
        "session_completeness": round(coverage_score, 4),
        "spread_stability": round(spread_stability, 4),
        "news_risk_flag": news_risk_flag,
        "confidence_cap": round(confidence_cap, 4),
        "present_timeframes": present_timeframes,
        "event_count": len(event_rows),
        "errors": errors,
        "quality_flags": sorted(set(flags)),
    }
