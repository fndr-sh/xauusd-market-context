# Demo Walkthrough

This walkthrough shows the shortest path from a fresh clone to inspectable XAUUSD market-context artifacts.

The demo uses only synthetic fixture data under `examples/sample-data`. It does not require broker credentials, MT5, vendor data, TradingView, or a live account.

## 1. Install locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -e .
```

## 2. Validate sample sources

```bash
python -m xau_lfx.pipeline validate-sources \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv
```

Expected result: the command should report a valid local source set. If validation fails, the failure should identify the CSV file and row-level issue.

## 3. Generate sample artifacts

```bash
python -m xau_lfx.pipeline run-once \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv \
  --out-dir artifacts
```

Important outputs:

```text
artifacts/xau_artifact_quality.json
artifacts/xau_context_summary.json
artifacts/xau_market_context_report.md
```

## 4. Inspect the context summary

Open:

```text
artifacts/xau_context_summary.json
```

This file is the compact operator-facing summary. It can include latest close, source freshness age, nearest session level context, spread state, event-risk state, confidence explanation, and monitor-focus bullets.

It is monitor-only. It must not be interpreted as directional trade-call guidance, execution instruction, position sizing, or profitability evidence.

## 5. Build the Markdown report

```bash
python -m xau_lfx.pipeline report --artifact-dir artifacts --write-md
```

Open:

```text
artifacts/xau_market_context_report.md
```

The report is the most readable artifact for human review.

## 6. Build the static demo site

```bash
python -m xau_lfx.pipeline site --artifact-dir artifacts --out-dir site
```

Open:

```text
site/index.html
```

The static site is backend-free and suitable for GitHub Pages. It summarizes artifact quality, context summary, source coverage, warnings, errors, and exported artifact links.

## 7. Rebuild committed sample artifacts

Maintainers can refresh the committed sample artifacts with:

```bash
python -m xau_lfx.pipeline run-once \
  --input-dir examples/sample-data \
  --event-file examples/sample-data/usd_events.csv \
  --out-dir examples/sample-artifacts

python -m xau_lfx.pipeline report \
  --artifact-dir examples/sample-artifacts \
  --write-md
```

Do not replace synthetic fixture artifacts with broker, vendor, or third-party market data unless redistribution rights are verified and documented.

## Safety contract

This project is a monitor-only market-context artifact generator.

It does not provide:

- trade execution;
- directional trade-call calls;
- account-risk logic;
- position sizing;
- profitability claims;
- centralized spot-gold orderbook claims;
- real dealer inventory or retail positioning claims.

