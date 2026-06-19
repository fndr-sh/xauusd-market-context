# Local CSV Quickstart

Run validation first:

```bash
python -m xau_lfx.pipeline validate-sources --input-dir examples/sample-data --event-file examples/sample-data/usd_events.csv
```

Generate artifacts:

```bash
python -m xau_lfx.pipeline run-once --input-dir examples/sample-data --event-file examples/sample-data/usd_events.csv --out-dir artifacts
```

Generate Markdown report:

```bash
python -m xau_lfx.pipeline report --artifact-dir artifacts --write-md
```

Inspect:

```text
artifacts/xau_artifact_quality.json
artifacts/xau_market_context_report.md
```
