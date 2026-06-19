from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_VERSION = "1.5.0"
EXPECTED_LICENSE_MARKER = "Apache License"
EXPECTED_DATA_POLICY_MARKER = "synthetic fixtures"

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "NOTICE",
    "DATA_LICENSE.md",
    "pyproject.toml",
    "MANIFEST.in",
    "DISCLAIMER.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "docs/DATA_SOURCE_POLICY.md",
    "docs/LOCAL_CSV_QUICKSTART.md",
    "docs/ARTIFACT_QUALITY.md",
    "docs/GITHUB_RELEASE_READINESS.md",
    "docs/GITHUB_PAGES_DEMO.md",
    "docs/LICENSE_POLICY.md",
    "docs/CLAUDE_FOR_OSS_POSITIONING.md",
    "docs/SCHEMA_REFERENCE.md",
    ".github/workflows/tests.yml",
    ".github/workflows/pages.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

REQUIRED_SAMPLE_FILES = [
    "examples/sample-data/XAUUSD_M5.csv",
    "examples/sample-data/XAUUSD_M15.csv",
    "examples/sample-data/XAUUSD_H1.csv",
    "examples/sample-data/XAUUSD_spread.csv",
    "examples/sample-data/usd_events.csv",
    "examples/sample-artifacts/xau_artifact_quality.json",
    "examples/sample-artifacts/xau_market_context_report.md",
]

FORBIDDEN_PUBLIC_FILES = [
    "docs/LICENSE_SELECTION_REQUIRED.md",
]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def check_readiness(root: str | Path = ".") -> dict:
    repo = Path(root)
    missing = [path for path in REQUIRED_FILES + REQUIRED_SAMPLE_FILES if not (repo / path).exists()]
    blockers: list[str] = []
    warnings: list[str] = []

    if missing:
        blockers.append("Missing required release-readiness files: " + ", ".join(missing))

    forbidden_present = [path for path in FORBIDDEN_PUBLIC_FILES if (repo / path).exists()]
    if forbidden_present:
        blockers.append("Remove obsolete pre-license blocker docs: " + ", ".join(forbidden_present))

    license_file = repo / "LICENSE"
    if license_file.exists() and EXPECTED_LICENSE_MARKER not in _read_text(license_file):
        blockers.append("LICENSE exists but does not look like Apache-2.0 text.")

    data_license = repo / "DATA_LICENSE.md"
    if data_license.exists() and EXPECTED_DATA_POLICY_MARKER not in _read_text(data_license).lower():
        blockers.append("DATA_LICENSE.md does not document synthetic fixture policy.")

    pyproject = repo / "pyproject.toml"
    init_file = repo / "xau_lfx" / "__init__.py"
    if pyproject.exists() and init_file.exists():
        py_text = _read_text(pyproject)
        init_text = _read_text(init_file)
        if f'version = "{EXPECTED_VERSION}"' not in py_text or f'__version__ = "{EXPECTED_VERSION}"' not in init_text:
            blockers.append(f"Package version is not consistently set to {EXPECTED_VERSION}.")
        if 'license = "Apache-2.0"' not in py_text or 'license-files = ["LICENSE", "NOTICE"]' not in py_text:
            blockers.append("pyproject.toml does not declare Apache-2.0 packaging metadata.")

    readme = repo / "README.md"
    if readme.exists():
        text = _read_text(readme).lower()
        for phrase in ["monitor-only", "local csv", "artifact quality", "static demo", "apache-2.0"]:
            if phrase not in text:
                warnings.append(f"README does not mention required phrase: {phrase}")

    issue_dir = repo / ".github" / "ISSUE_TEMPLATE"
    issue_templates = list(issue_dir.glob("*.md")) if issue_dir.exists() else []
    if len(issue_templates) < 3:
        warnings.append("Fewer than 3 issue templates are present.")

    status = "BLOCKED" if blockers else ("WARN" if warnings else "READY")
    return {
        "status": status,
        "blockers": blockers,
        "warnings": warnings,
        "checked_files": len(REQUIRED_FILES) + len(REQUIRED_SAMPLE_FILES),
        "license": "Apache-2.0" if license_file.exists() and EXPECTED_LICENSE_MARKER in _read_text(license_file) else "UNKNOWN",
        "version": EXPECTED_VERSION,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check release readiness for XAU-LFX External Data Foundation.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when blockers or warnings are present.")
    args = parser.parse_args()
    result = check_readiness(args.root)
    print(json.dumps(result, indent=2))
    if args.strict and result["status"] != "READY":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
