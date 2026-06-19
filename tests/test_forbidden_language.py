import pytest

from xau_lfx.forbidden_language import assert_clean_language, scan_forbidden_language


def test_forbidden_language_detects_terms():
    assert "BUY" in scan_forbidden_language("BUY")
    with pytest.raises(ValueError):
        assert_clean_language({"summary": "ENTRY now"})


def test_allowed_monitor_language_passes():
    assert_clean_language({"state": "WATCH", "summary": "Monitor context only"})
