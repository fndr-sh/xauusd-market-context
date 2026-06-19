# Changelog

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
