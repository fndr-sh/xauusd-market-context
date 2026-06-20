from pathlib import Path

from xau_lfx.forbidden_language import assert_clean_language


ROOT = Path(__file__).resolve().parents[1]


def test_phase_f_usage_and_sharing_docs_exist_and_are_monitor_only():
    paths = [
        ROOT / "docs" / "OANDA_LIVE_DASHBOARD.md",
        ROOT / "docs" / "REAL_WORLD_USAGE.md",
        ROOT / "docs" / "SHARING_VALIDATION_REPORTS.md",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "report_export_issue.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    for path in paths:
        assert path.exists()
    for phrase in [
        "malformed CSV is rejected",
        "spread instability lowers quality",
        "event proximity caps confidence",
        "nearest session level is explicit",
        "stale data reduces freshness",
        "missing timeframe reduces coverage",
        "freshness_age_minutes",
        "MTF_COVERAGE_INCOMPLETE",
        "OANDA_API_TOKEN",
        "private LAN",
        "5 seconds",
        "NOT_INFERRED",
    ]:
        assert phrase in text
    assert_clean_language(text)


def test_readme_links_live_dashboard_and_phase_f_guides():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/OANDA_LIVE_DASHBOARD.md" in readme
    assert "docs/REAL_WORLD_USAGE.md" in readme
    assert "docs/SHARING_VALIDATION_REPORTS.md" in readme
    assert "serve-oanda" in readme
