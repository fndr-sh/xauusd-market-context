# Changelog

## v1.9.0 - CLI usability polish

### Added

- `xau-lfx demo` to validate synthetic fixtures and generate JSON, Markdown, and static HTML outputs in one command.
- Absolute generated-file paths in `run-once` and `demo` terminal output.
- `docs/CLI_USAGE.md` with sample, validation, report, and static-site commands.
- CLI smoke tests and a direct demo command in the GitHub Actions test matrix.

### Changed

- Reduced the README sample quickstart to the one-command demo path.
- Updated release-readiness metadata and required docs for v1.9.0.

### Preserved

- Existing CLI commands and no-source compatibility behavior.
- Existing connector, engine, schema, and artifact calculations.
- Existing monitor-only safety contract.
- No execution, account-risk, directional trade-call, or profitability claims.

## v1.8.0 - Demo artifact polish

### Added

- Demo walkthrough for clone-to-artifact usage.
- `examples/sample-artifacts/README.md` to explain each committed sample artifact.
- Release-readiness check for `xau_context_summary.json` in sample artifacts.
- Demo documentation tests.

### Changed

- Regenerated sample artifacts from synthetic fixture data so the committed demo output includes the context summary artifact.

### Preserved

- Existing runtime engine behavior.
- Existing CSV validation behavior.
- Existing context-summary calculation.
- Existing monitor-only safety contract.
- No execution, account-risk, buy/sell, or profitability claims.

## v1.7.0 - GitHub adoption pack

### Added

- README status badges for tests, Pages, latest release, and Apache-2.0 license.
- Public use-case and audience sections.
- MT5 export guide for local XAUUSD CSV preparation.
- Adoption guide for first-run and GitHub topic setup.
- Issue backlog seed for good-first-issue, enhancement, and research tasks.
- Additional issue templates for validation, context-summary, and docs improvements.
- Public adoption docs tests.

### Preserved

- Existing runtime behavior.
- Existing artifact contract.
- Existing monitor-only safety contract.
- No execution, account-risk, buy/sell, or profitability claims.

## v1.6.0 - Useful context summary

### Added

- Added `xau_context_summary.json` as a compact monitor-only operator summary.
- Added latest close, freshness age, nearest session level, spread state, event risk state, confidence explanation, and monitor focus.
- Added context-summary section to Markdown report and static demo site.
- Added context-summary documentation and tests.

### Preserved

- Existing artifact contract remains compatible.
- Existing monitor-only behavior remains locked.
- No execution, account-risk, or profitability claims.

## v1.5.0 - Source validation hardening

### Added

- Strict OHLCV row validation for high/low/open/close consistency.
- Duplicate and non-increasing timestamp rejection for OHLCV and spread CSV files.
- Negative tick-volume rejection.
- Spread sanity checks for ask/bid and negative spread points.
- Source validation documentation.

### Preserved

- Monitor-only behavior.
- Existing artifact contract.
- No execution, account-risk, or profitability claims.

## v1.4.1 - Public metadata hotfix

### Fixed

- Replaced placeholder package URLs with the public GitHub repository URLs.
- Aligned README title with the public repository name.
- Aligned static demo page title and heading with the public repository name.

### Preserved

- Existing package distribution name for v1.x continuity.
- Monitor-only behavior.
- No execution, account-risk, or profitability claims.

## v1.4.0 - Public GitHub publish pack

### Added

- Apache-2.0 `LICENSE`.
- `NOTICE` attribution file.
- `DATA_LICENSE.md` synthetic fixture and third-party data redistribution policy.
- `docs/LICENSE_POLICY.md`.
- Release-readiness checker updated to require license, notice, data policy, and Apache package metadata.

### Changed

- Package version bumped to `1.4.0`.
- README release-readiness status changed from blocked to ready.
- GitHub/OSS positioning updated for public publish readiness.

### Preserved

- Monitor-only behavior.
- No execution, account-risk, or profitability claims.
- No mutation of the LFX-2 Pine baseline.

## v1.3.0 - GitHub release readiness foundation

### Added

- Python package metadata via `pyproject.toml`.
- CLI script aliases: `xau-lfx` and `xau-lfx-api`.
- Static demo site generator: `python -m xau_lfx.pipeline site`.
- GitHub Pages workflow for sample-artifact demo publishing.
- Release-readiness checker: `scripts/check_release_readiness.py`.
- Pull request template and issue templates.
- Code of conduct.
- License-selection blocker documentation.
- Claude for Open Source positioning note.
- Schema reference document.

### Preserved

- Monitor-only behavior.
- Local CSV source policy.
- No execution, account-risk, or profitability claims.
- No mutation of the LFX-2 Pine baseline.

## v1.2.0 - Local Data Utility Foundation

- Added MT5/local CSV ingestion for XAUUSD M5/M15/H1 OHLCV files.
- Added broker spread CSV ingestion.
- Added manual USD event CSV ingestion.
- Added artifact quality scoring.
- Added Markdown market-context report.
- Added sample data fixtures.
- Added docs and GitHub CI workflow.

## v1.1.0 - User Insight Layer

- Added human-readable monitor-only insight artifact.

## v1.0.0 - External Data Foundation Skeleton

- Added no-source monitor skeleton and local API artifacts.
