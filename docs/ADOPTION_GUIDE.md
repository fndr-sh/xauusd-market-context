# Adoption Guide

STATUS: PUBLIC_ADOPTION_DOC  
MODE: CONTROL  
TRADING_MODE: MONITOR_ONLY

This document explains how to evaluate and adopt `xauusd-market-context`.

## What the repo gives you

- local CSV ingestion for XAUUSD OHLCV and spread snapshots;
- schema and consistency validation;
- source quality scoring;
- session context;
- event-risk context;
- useful context summary;
- Markdown report output;
- static HTML demo generation.
- optional OANDA Practice M5/M15/H1 candle dashboard on a private host.

## What it does not give you

- no directional trade-call behavior;
- no execution logic;
- no position sizing;
- no account-risk logic;
- no profitability or statistical-edge claim;
- no claim of centralized XAUUSD spot volume or orderbook.

## Recommended first run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
pip install pytest build

python -m xau_lfx.pipeline validate-sources --input-dir examples/sample-data --event-file examples/sample-data/usd_events.csv
python -m xau_lfx.pipeline run-once --input-dir examples/sample-data --event-file examples/sample-data/usd_events.csv --out-dir artifacts
python -m xau_lfx.pipeline report --artifact-dir artifacts --write-md
python -m xau_lfx.pipeline site --artifact-dir artifacts --out-dir site
```

Open:

```text
site/index.html
```

## Optional private live dashboard

The OANDA path is separate from the synthetic demo and local CSV pipeline. It requires an OANDA Practice token stored only in the local process environment.

After completing the credential steps in [`OANDA_LIVE_DASHBOARD.md`](OANDA_LIVE_DASHBOARD.md), bind the service to an explicit private address:

```powershell
.\.venv\Scripts\python.exe -m xau_lfx.web serve-oanda `
  --host 192.168.1.20 `
  --port 8766 `
  --request-timeout-seconds 10
```

Open `http://192.168.1.20:8766/` from a phone or PC on the same private network. The browser receives candle/context data but never receives the OANDA token. Do not expose the service through public port forwarding.

## GitHub topics

Recommended repository topics:

```text
xauusd
market-data
mt5
research
tradingview
monitor-only
csv-validation
static-site
python
dashboard
fastapi
oanda
```

Topics are set in the GitHub UI:

```text
Repo -> About gear icon -> Topics
```

## Adoption signals to build

Useful public signals for the project:

- issues with clear labels;
- `good first issue` tasks;
- real user questions around CSV validation;
- demo screenshots or generated static outputs;
- documented limitations and safety contract;
- reproducible sample artifacts.
- external forks that progress into reviewable pull requests;
- release-asset downloads and documented user workflows;
- private-dashboard feedback that contains no credential or redistributed market payload.

## Participate

- Public roadmap: `ROADMAP.md`
- Maintainer policy: `MAINTAINERS.md`
- LFX external boundary: `docs/LFX_EXTERNAL_BASELINE.md`
- Curated backlog source: `docs/ISSUE_BACKLOG_SEED.md`
- User feedback: select the user workflow feedback template when opening an issue.
