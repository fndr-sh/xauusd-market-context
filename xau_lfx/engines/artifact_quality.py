from __future__ import annotations

from typing import Any

from xau_lfx.utils import utc_now_iso


def quality_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 65:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def _pct(value: float | int | None) -> float:
    if value is None:
        return 0.0
    return round(max(0.0, min(1.0, float(value))) * 100.0, 2)


def build_artifact_quality(
    data_quality: dict[str, Any],
    composite: dict[str, Any],
    session: dict[str, Any],
    event: dict[str, Any],
) -> dict[str, Any]:
    errors = list(data_quality.get("errors", []))
    warnings = sorted(
        set(
            data_quality.get("quality_flags", [])
            + composite.get("quality_flags", [])
            + session.get("quality_flags", [])
            + event.get("quality_flags", [])
        )
    )

    freshness_score = _pct(data_quality.get("freshness_score", 0.0))
    coverage_score = _pct(data_quality.get("coverage_score", 0.0))
    schema_score = _pct(data_quality.get("schema_score", 0.0))
    session_score = 100.0 if session.get("session_ranges") else 0.0
    spread_score = _pct(data_quality.get("spread_stability", 0.0))
    event_score = 100.0 if event.get("event_count", 0) > 0 else 50.0
    if event.get("near_high_impact_events"):
        event_score = min(event_score, 65.0)

    score = round(
        freshness_score * 0.15
        + coverage_score * 0.25
        + schema_score * 0.25
        + session_score * 0.15
        + spread_score * 0.10
        + event_score * 0.10,
        2,
    )
    if errors:
        score = min(score, 49.0)
    if data_quality.get("source_count", 0) == 0:
        score = min(score, 35.0)

    if errors:
        status = "ERROR"
    elif score < 65 or data_quality.get("news_risk_flag"):
        status = "WARN"
    else:
        status = "OK"

    return {
        "ts_utc": utc_now_iso(),
        "symbol": data_quality.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "status": status,
        "quality_score": score,
        "quality_grade": quality_grade(score),
        "freshness_score": freshness_score,
        "coverage_score": coverage_score,
        "schema_score": schema_score,
        "session_score": session_score,
        "spread_score": spread_score,
        "event_score": event_score,
        "source_count": data_quality.get("source_count", 0),
        "warnings": warnings,
        "errors": errors,
        "confidence_cap": data_quality.get("confidence_cap", 0.0),
    }
