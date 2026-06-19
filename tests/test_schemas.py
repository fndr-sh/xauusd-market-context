from xau_lfx.pipeline import run_once


def test_run_once_creates_monitor_state():
    state = run_once()
    assert state["monitor_only"] is True
    assert state["state"] in {"WATCH", "INSUFFICIENT_SOURCE_COVERAGE"}
    assert "quality" in state
    assert state["quality"]["confidence_cap"] == 0.0
