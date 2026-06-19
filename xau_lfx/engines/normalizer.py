from __future__ import annotations

from xau_lfx.utils import utc_now_iso


def normalize_raw_scan(source_payloads: list[dict], symbol: str = "XAUUSD") -> dict:
    flags: list[str] = []
    for payload in source_payloads:
        flags.extend(payload.get("quality_flags", []))
    if not source_payloads:
        flags.append("NO_SOURCE_PAYLOADS")
    return {
        "ts_utc": utc_now_iso(),
        "symbol": symbol,
        "monitor_only": True,
        "source_payloads": source_payloads,
        "quality_flags": sorted(set(flags)),
    }
