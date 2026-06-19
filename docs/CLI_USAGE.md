# CLI Usage

The `xau-lfx` command validates local XAUUSD CSV files and generates monitor-only context artifacts. It does not require broker credentials for the synthetic demo.

## One-command demo

Run from a source checkout after `pip install -e .`:

```bash
xau-lfx demo
```

The command validates the committed synthetic fixtures, writes JSON and Markdown artifacts under `artifacts/`, and builds `site/index.html`. Its terminal summary prints the absolute path of every generated file.

Custom output directories are supported:

```bash
xau-lfx demo --out-dir demo-artifacts --site-dir demo-site
```

The demo reads only `examples/sample-data`. It does not read broker or vendor data.

## Validate local sources

```bash
xau-lfx validate-sources \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv
```

Validation reports source coverage, errors, and quality flags without writing market-context artifacts.

## Generate JSON artifacts

```bash
xau-lfx run-once \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv \
  --out-dir artifacts
```

The command keeps its existing state output and then prints the absolute path of each generated JSON artifact.

Running `xau-lfx run-once` without local files preserves the existing low-confidence readiness behavior.

## Generate the Markdown report

```bash
xau-lfx report --artifact-dir artifacts --write-md
```

## Generate the static site

```bash
xau-lfx site --artifact-dir artifacts --out-dir site
```

Open `site/index.html` locally. The generated outputs remain monitor-only research context and do not contain execution or account-risk logic.
