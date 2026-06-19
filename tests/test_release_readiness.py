import importlib.util
from pathlib import Path


def _load_release_module():
    path = Path("scripts/check_release_readiness.py")
    spec = importlib.util.spec_from_file_location("check_release_readiness", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_release_readiness_is_ready_after_license_lock():
    module = _load_release_module()
    result = module.check_readiness(".")
    assert result["status"] == "READY"
    assert result["blockers"] == []
    assert result["warnings"] == []
    assert result["license"] == "Apache-2.0"


def test_release_readiness_checks_expected_files():
    module = _load_release_module()
    result = module.check_readiness(".")
    assert result["checked_files"] >= 25
    assert not any("Missing required" in blocker for blocker in result["blockers"])
