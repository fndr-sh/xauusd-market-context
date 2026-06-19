# Sample Artifacts

This directory contains generated output from the synthetic fixture data in `examples/sample-data`.

The purpose is to let users inspect artifact shape before running the tool on their own local broker/MT5 exports.

## Rebuild

```bash
python -m xau_lfx.pipeline run-once \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv \
  --out-dir examples/sample-artifacts

python -m xau_lfx.pipeline report \
  --artifact-dir examples/sample-artifacts \
  --write-md
```

## Key files

```text
xau_artifact_quality.json
xau_context_summary.json
xau_market_context_report.md
```

## What to inspect first

1. `xau_artifact_quality.json` - quality score, grade, warnings, and confidence cap.
2. `xau_context_summary.json` - compact operator-facing context summary.
3. `xau_market_context_report.md` - human-readable report.
4. `xau_data_quality.json` - source coverage, freshness, spread, and confidence details.

## Data policy

These artifacts are generated from synthetic fixture data. They are not live market data and must not be used as trading guidance.

Do not commit broker, vendor, or third-party data unless redistribution rights are verified and documented.
