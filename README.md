# XAUUSD Market Context v1.4.1

STATUS: PUBLIC_RELEASE_METADATA_HOTFIX  
MODE: CONTROL  
TRADING_MODE: MONITOR_ONLY  
AUTO_EXECUTION: NO  
DIRECTIONAL_TRADE_CALLS: NO

Generate auditable XAUUSD market-context artifacts from local MT5/broker CSV exports, spread snapshots, and manual USD event files. v1.4.1 aligns the public repository naming, package metadata URLs, and static demo title after the initial public release. The package is a monitor-only sidecar for XAU research workflows; it does not modify the LFX-2 Pine baseline and does not place orders or produce execution instructions.

## Why this exists

Most retail XAUUSD workflows depend on one broker feed and opaque indicator output. This repo takes a stricter route:

- ingest local CSV files that the user controls;
- validate schema, freshness, spread stability, and MTF coverage;
- preserve broker tick activity as `tick_volume`, not centralized volume;
- generate JSON and Markdown artifacts that can be audited or used by another dashboard;
- cap confidence when source quality, spread, or event risk is weak.

## Hard rules

- Does not modify LFX-2 v7.1-F Pine source.
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
pip install pytest

python -m xau_lfx.pipeline validate-sources \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv

python -m xau_lfx.pipeline run-once \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv \
  --out-dir artifacts

python -m xau_lfx.pipeline report --artifact-dir artifacts --write-md
python -m xau_lfx.pipeline site --artifact-dir artifacts --out-dir site
```

Open `site/index.html` for the static demo. This is the same output shape intended for GitHub Pages.

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

## Static demo

```bash
python -m xau_lfx.pipeline site --artifact-dir examples/sample-artifacts --out-dir site
```

The generated page summarizes artifact quality, source coverage, event risk context, and exported artifacts. It is intentionally static so it can be hosted by GitHub Pages without backend services.

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
