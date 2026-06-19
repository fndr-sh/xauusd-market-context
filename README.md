# XAUUSD Market Context v2.3.0

[![tests](https://github.com/thanhlq8-max/xauusd-market-context/actions/workflows/tests.yml/badge.svg)](https://github.com/thanhlq8-max/xauusd-market-context/actions/workflows/tests.yml)
[![pages-demo](https://github.com/thanhlq8-max/xauusd-market-context/actions/workflows/pages.yml/badge.svg)](https://github.com/thanhlq8-max/xauusd-market-context/actions/workflows/pages.yml)
[![Release](https://img.shields.io/github/v/release/thanhlq8-max/xauusd-market-context)](https://github.com/thanhlq8-max/xauusd-market-context/releases)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

STATUS: COMMUNITY_BACKLOG_EXECUTION
MODE: CONTROL  
TRADING_MODE: MONITOR_ONLY  
AUTO_EXECUTION: NO  
DIRECTIONAL_TRADE_CALLS: NO

Generate auditable XAUUSD market-context artifacts from local MT5/broker CSV exports, spread snapshots, and manual USD event files. v2.3.0 adds a public community backlog, maintainer policy, feedback path, and narrowly scoped issue triage. The package is a monitor-only sidecar for XAU research workflows; it uses the LFX-2 material as a semantic and safety baseline without modifying or reproducing the Pine source.

## Why this exists

Most retail XAUUSD workflows depend on one broker feed and opaque indicator output. This repo takes a stricter route:

- ingest local CSV files that the user controls;
- validate schema, freshness, spread stability, and MTF coverage;
- preserve broker tick activity as `tick_volume`, not centralized volume;
- generate JSON and Markdown artifacts that can be audited or used by another dashboard;
- cap confidence when source quality, spread, or event risk is weak.

## Use cases

- Validate local XAUUSD CSV exports before using them in research dashboards.
- Generate auditable market-context artifacts from broker-controlled source files.
- Inspect MTF coverage, source freshness, spread state, event-risk state, and context summary.
- Produce static HTML/Markdown outputs that can be shared without a backend service.
- Maintain a monitor-only workflow that avoids trading-signal, execution, and profitability claims.

## Who this is for

- XAUUSD researchers who want reproducible local artifacts.
- Systematic traders who need source-quality gates before downstream analysis.
- Tool builders who need a small, static, auditable market-context sidecar.
- Contributors looking for focused OSS issues around validation, docs, and report quality.

## Hard rules

- Does not modify or reproduce the LFX-2 v7.1-F/v7.2-A-R5 Pine source.
- Does not create order execution, position sizing, or account-risk logic.
- Does not claim centralized XAUUSD spot orderbook.
- Does not treat CFD tick activity as centralized traded volume.
- Does not claim actual dealer inventory or actual retail-side positioning.
- Does not claim statistical edge or profitability.

## Install

For local development:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -e .
```

CLI commands after editable install:

```bash
xau-lfx --help
xau-lfx-api --help
```

## Quickstart with sample data

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -e .
xau-lfx demo
```

The command validates the committed synthetic fixtures, generates JSON and Markdown artifacts, prints their absolute paths, and builds `site/index.html`. Open that file for the static demo used by GitHub Pages.


Demo walkthrough:

```text
docs/DEMO_WALKTHROUGH.md
```

The walkthrough explains how to rebuild sample artifacts, inspect `xau_context_summary.json`, open the generated Markdown report, and generate the static demo site without broker credentials.

Complete CLI reference: [`docs/CLI_USAGE.md`](docs/CLI_USAGE.md).

No-argument compatibility mode still works:

```bash
python -m xau_lfx.pipeline run-once
```

That mode intentionally returns a low-confidence readiness state until local sources are provided.

## Local CSV schemas

### OHLCV files

Expected files:

```text
XAUUSD_M5.csv
XAUUSD_M15.csv
XAUUSD_H1.csv
```

Required columns:

```text
ts_utc,open,high,low,close,tick_volume
```

Rules:

- `ts_utc` must include a timezone and parse as UTC-compatible ISO-8601.
- OHLC values must be numeric.
- `tick_volume` is preserved as broker tick activity.
- Missing columns fail validation; missing OHLC values are not filled.

### Spread file

Expected file:

```text
XAUUSD_spread.csv
```

Required columns:

```text
ts_utc,bid,ask,spread_points
```

Spread is broker-specific. Instability reduces artifact quality.

### Event file

Required columns:

```text
ts_utc,currency,impact,title
```

Allowed impact values:

```text
LOW,MEDIUM,HIGH
```

Only high-impact USD events may cap confidence for XAUUSD, and only as risk context. The system does not infer direction from events.

## Artifact outputs

```text
artifacts/xau_raw_scan.json
artifacts/xau_data_quality.json
artifacts/xau_composite_ohlcv.json
artifacts/xau_session_context.json
artifacts/xau_event_risk_state.json
artifacts/xau_lfx_external_state.json
artifacts/xau_user_insight.json
artifacts/xau_artifact_quality.json
artifacts/xau_context_summary.json
artifacts/xau_market_context_report.md
```

Example quality excerpt:

```json
{
  "status": "OK",
  "quality_score": 86.5,
  "quality_grade": "B",
  "source_count": 2,
  "confidence_cap": 0.75
}
```

## Local API

```bash
python -m xau_lfx.web serve --host 127.0.0.1 --port 8766
```

Endpoints:

- `/api/xau/state`
- `/api/xau/data-quality`
- `/api/xau/session-context`
- `/api/xau/macro-pressure`
- `/api/xau/event-risk`
- `/api/xau/composite-ohlcv`
- `/api/xau/user-insight`
- `/api/xau/artifact-quality`
- `artifacts/xau_context_summary.json` is generated by `run-once` for report/static-site use.

## Static demo

```bash
python -m xau_lfx.pipeline site --artifact-dir examples/sample-artifacts --out-dir site
```

The generated page summarizes artifact quality, source coverage, event risk context, and exported artifacts. It is intentionally static so it can be hosted by GitHub Pages without backend services.


Sample demo artifacts are documented here:

```text
examples/sample-artifacts/README.md
```

The committed sample artifacts are synthetic fixture outputs. They are included for output-shape inspection and GitHub Pages demo generation, not as market data.

## GitHub adoption resources

This repo includes public-facing adoption material:

```text
docs/MT5_EXPORT_GUIDE.md
docs/ADOPTION_GUIDE.md
docs/ISSUE_BACKLOG_SEED.md
docs/CONTEXT_SUMMARY.md
docs/CLI_USAGE.md
docs/LFX_EXTERNAL_BASELINE.md
ROADMAP.md
MAINTAINERS.md
```

Suggested GitHub topics:

```text
xauusd, market-data, mt5, research, tradingview, monitor-only, csv-validation, static-site, python
```

These resources are intentionally documentation-first. They improve discoverability and contributor onboarding without changing the monitor-only runtime contract.

## Community participation

- Review [`ROADMAP.md`](ROADMAP.md) before proposing a new module.
- Use the [public issue backlog](https://github.com/thanhlq8-max/xauusd-market-context/issues) for independently scoped work.
- Use the user workflow feedback template for setup, validation, artifact, report, or demo feedback.
- Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`MAINTAINERS.md`](MAINTAINERS.md) before opening a pull request.
- Treat [`docs/LFX_EXTERNAL_BASELINE.md`](docs/LFX_EXTERNAL_BASELINE.md) as the boundary for any LFX-derived external documentation or proposal.

## License

This repository is licensed under Apache-2.0. See:

```text
LICENSE
NOTICE
DATA_LICENSE.md
docs/LICENSE_POLICY.md
```

The bundled sample data is synthetic fixture data for parser/report/static-demo validation. Do not commit broker, vendor, or third-party market data unless redistribution rights are verified and documented.

## Release readiness

```bash
python scripts/check_release_readiness.py --strict
```

Expected public-release status: `READY`.

## Development

```bash
python -m compileall xau_lfx scripts
PYTHONPATH=. pytest -q
python -m xau_lfx.pipeline run-once --input-dir examples/sample-data --event-file examples/sample-data/usd_events.csv --out-dir artifacts
python -m xau_lfx.pipeline report --artifact-dir artifacts --write-md
python -m xau_lfx.pipeline site --artifact-dir artifacts --out-dir site
```

See `CONTRIBUTING.md`, `SECURITY.md`, `DISCLAIMER.md`, and `docs/` for source policy and contribution rules.
