from __future__ import annotations

from xau_lfx.forbidden_language import assert_clean_language
from xau_lfx.utils import utc_now_iso


def _flag_set(*blocks: dict) -> set[str]:
    flags: set[str] = set()
    for block in blocks:
        flags.update(block.get("quality_flags", []))
        quality = block.get("quality", {})
        if isinstance(quality, dict):
            flags.update(quality.get("quality_flags", []))
    return flags


def build_user_insight(data_quality: dict, composite: dict, session: dict, macro: dict, event: dict, state: dict) -> dict:
    """Build a monitor-only explanation layer that is useful to a human operator.

    The output must not contain execution language. It answers:
    - what the system can say now,
    - why confidence is capped,
    - what the user should monitor next,
    - what data is required to upgrade the state.
    """
    flags = sorted(_flag_set(data_quality, composite, session, macro, event, state))
    confidence_cap = float(data_quality.get("confidence_cap", 0.0))
    source_count = int(data_quality.get("source_count", 0))
    risk_state = event.get("risk_state", "CAUTION")

    if confidence_cap <= 0.0 or source_count < 2:
        headline = "External XAU context is not decision-grade yet. Treat output as a data-readiness monitor."
        now_read = "The system has not validated enough independent external sources to describe live XAU pressure."
        next_watch = [
            "Activate at least two independent source families before interpreting pressure context.",
            "Prioritize broker feed freshness, session range completeness, and event-calendar status.",
            "Keep LFX-2 v7.1-F Pine baseline as the visual field monitor until external data passes the gate.",
        ]
        useful_limits = [
            "Current value: identifies missing data and blocks false confidence.",
            "Not available yet: pressure ranking, session handoff read, and composite reference levels.",
        ]
    else:
        headline = "External XAU context has passed the initial data-readiness gate."
        now_read = "The system can provide bounded monitor context from validated external sources."
        next_watch = [
            "Compare M15 strategic field state against external pressure and session context.",
            "Monitor whether M5 confirmation behavior agrees with the M15 field condition.",
            "Reduce confidence when event risk or spread instability appears.",
        ]
        useful_limits = [
            "Available: bounded context, evidence list, and data-quality cap.",
            "Still excluded: centralized spot orderbook assumption and real inventory claims.",
        ]

    insight = {
        "ts_utc": utc_now_iso(),
        "symbol": data_quality.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "headline": headline,
        "now_read": now_read,
        "operator_focus": next_watch,
        "evidence_map": [
            f"source_count={source_count}",
            f"confidence_cap={confidence_cap}",
            f"risk_state={risk_state}",
            f"state={state.get('state', 'UNKNOWN')}",
        ],
        "useful_limits": useful_limits,
        "upgrade_requirements": [
            "Configure MT5 or broker feed exporter for XAUUSD M5/M15/H1 bars and spread snapshots.",
            "Configure one public reference family for macro or futures context.",
            "Configure event calendar feed or manual high-impact event file.",
            "Add historical replay samples before claiming dashboard usefulness beyond data readiness.",
        ],
        "quality_flags": flags,
    }
    assert_clean_language(insight)
    return insight
