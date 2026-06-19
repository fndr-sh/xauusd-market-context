from xau_lfx.config import artifact_paths
from xau_lfx.forbidden_language import assert_clean_language
from xau_lfx.pipeline import run_once
from xau_lfx.reports.market_context_report import write_market_context_report


def test_market_context_report_writes_markdown(tmp_path):
    run_once(input_dir="examples/sample-data", event_file="examples/sample-data/usd_events.csv", out_dir=tmp_path)
    report = write_market_context_report(tmp_path, write_md=True)
    assert "# XAUUSD Market Context Report" in report
    assert "Artifact Quality" in report
    assert artifact_paths(tmp_path)["market_context_report"].exists()
    assert_clean_language(report)
