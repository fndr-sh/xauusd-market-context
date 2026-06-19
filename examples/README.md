# Examples

## sample-data

Local CSV fixtures that let users run the full pipeline without broker credentials.

## sample-artifacts

Generated JSON and Markdown artifacts from the sample data. These are included so new users can inspect output shape before running the tool.

## Rebuild artifacts

```bash
python -m xau_lfx.pipeline run-once --input-dir examples/sample-data --event-file examples/sample-data/usd_events.csv --out-dir examples/sample-artifacts
python -m xau_lfx.pipeline report --artifact-dir examples/sample-artifacts --write-md
```
