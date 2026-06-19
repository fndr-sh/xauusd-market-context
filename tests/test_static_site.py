from pathlib import Path

from xau_lfx.forbidden_language import assert_clean_language
from xau_lfx.pipeline import run_once
from xau_lfx.reports.market_context_report import write_market_context_report
from xau_lfx.reports.static_site import build_static_site_html, write_static_site


def test_static_site_builds_from_sample_artifacts(tmp_path):
    artifact_dir = tmp_path / "artifacts"
    site_dir = tmp_path / "site"
    run_once(input_dir="examples/sample-data", event_file="examples/sample-data/usd_events.csv", out_dir=artifact_dir)
    write_market_context_report(artifact_dir, write_md=True)

    index_path = write_static_site(artifact_dir=artifact_dir, out_dir=site_dir)
    html = index_path.read_text(encoding="utf-8")

    assert index_path.exists()
    assert "XAUUSD Market Context" in html
    assert "Quality" in html
    assert (site_dir / "artifacts" / "xau_artifact_quality.json").exists()
    assert (site_dir / "artifacts" / "xau_market_context_report.md").exists()
    assert_clean_language(html)


def test_static_site_html_contains_artifact_links():
    html = build_static_site_html("examples/sample-artifacts", out_dir="examples/sample-site")
    assert "xau_artifact_quality.json" in html
    assert "xau_market_context_report.md" in html
    assert_clean_language(html)
