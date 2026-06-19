FORBIDDEN_TERMS = [
    "BUY",
    "SELL",
    "LONG NOW",
    "SHORT NOW",
    "ENTRY",
    "STOP LOSS",
    "TAKE PROFIT",
    "WIN RATE",
    "GUARANTEED",
    "TRUE MM INVENTORY",
    "REAL RETAIL POSITIONING",
]

ALLOWED_STATES = {
    "WATCH",
    "CONTEXT",
    "NO_TRADE",
    "CAUTION",
    "INSUFFICIENT_SOURCE_COVERAGE",
    "RESEARCH_ONLY",
}


def scan_forbidden_language(value: object) -> list[str]:
    text = str(value).upper()
    return [term for term in FORBIDDEN_TERMS if term in text]


def assert_clean_language(value: object) -> None:
    hits = scan_forbidden_language(value)
    if hits:
        raise ValueError(f"Forbidden monitor-only language detected: {hits}")
