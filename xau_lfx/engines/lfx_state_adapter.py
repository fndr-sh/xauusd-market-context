from __future__ import annotations

from xau_lfx.forbidden_language import assert_clean_language
from xau_lfx.utils import utc_now_iso


def build_external_state(data_quality: dict, composite: dict, session: dict, macro: dict, event: dict) -> dict:
    flags = sorted(set(
        data_quality.get("quality_flags", [])
        + composite.get("quality_flags", [])
        + session.get("quality_flags", [])
        + macro.get("quality_flags", [])
        + event.get("quality_flags", [])
    ))
    confidence_cap = float(data_quality.get("confidence_cap", 0.0))
    source_count = int(data_quality.get("source_count", 0))

    if data_quality.get("errors"):
        state_name = "INSUFFICIENT_SOURCE_COVERAGE"
        summary = "Source validation errors are present. Use the artifacts to repair the local CSV inputs."
    elif event.get("near_high_impact_events"):
        state_name = "CAUTION"
        summary = "Local CSV sources are loaded, but nearby high-impact USD event risk caps confidence."
    elif source_count >= 1 and confidence_cap > 0.0:
        state_name = "CONTEXT"
        summary = "Local XAU source artifacts are available for monitor-only market context."
    else:
        state_name = "INSUFFICIENT_SOURCE_COVERAGE"
        summary = "External XAU context is in research-only no-source mode. Use as monitor context only."

    evidence = [
        f"source_count={source_count}",
        f"confidence_cap={confidence_cap}",
        "M15 remains strategic; M5 is confirmation-only; H1 is context-only.",
        "Downstream confidence is capped by Data Quality Gate.",
    ]
    if composite.get("median_latest_close") is not None:
        evidence.append(f"median_latest_close={composite.get('median_latest_close')}")
    if event.get("risk_state"):
        evidence.append(f"event_risk_state={event.get('risk_state')}")

    state = {
        "ts_utc": utc_now_iso(),
        "symbol": data_quality.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "state": state_name,
        "summary": summary,
        "evidence": evidence,
        "quality": {
            "quality_flags": flags,
            "confidence_cap": confidence_cap,
            "source_count": source_count,
            "missing_field_count": data_quality.get("missing_field_count", 0),
        },
    }
    assert_clean_language(state)
    return state
