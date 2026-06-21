# MT5 Export Guide

STATUS: PUBLIC_ADOPTION_DOC  
MODE: CONTROL  
TRADING_MODE: MONITOR_ONLY

This guide describes how to prepare local MT5-style CSV files for `xauusd-market-context`.

The project does not connect to a live trading account, does not place orders, and does not infer execution instructions.

## Required files

Place files in a local folder such as:

```text
data/xauusd/
```

Expected names:

```text
XAUUSD_M5.csv
XAUUSD_M15.csv
XAUUSD_H1.csv
XAUUSD_spread.csv
usd_events.csv
```

The sample folder uses:

```text
examples/sample-data/
```

## OHLCV schema

Each timeframe CSV must use this header:

```text
ts_utc,open,high,low,close,tick_volume
```

Rules:

* `ts_utc` must include timezone information.
* timestamps must be strictly increasing.
* duplicate timestamps are rejected.
* `high` must be greater than or equal to `open`, `close`, and `low`.
* `low` must be less than or equal to `open`, `close`, and `high`.
* `tick_volume` must not be negative.
* `tick_volume` is broker tick activity, not centralized XAUUSD volume.

Example:

```csv
ts_utc,open,high,low,close,tick_volume
2026-06-18T14:00:00Z,2339.70,2341.50,2338.10,2339.34,120
2026-06-18T15:00:00Z,2339.19,2341.09,2337.49,2338.95,123
```

## Spread schema

`XAUUSD_spread.csv` must use this header:

```text
ts_utc,bid,ask,spread_points
```

Rules:

* `ask` must be greater than or equal to `bid`.
* `spread_points` must not be negative.
* spread is broker-specific and is used only as source-quality context.

Example:

```csv
ts_utc,bid,ask,spread_points
2026-06-19T05:25:00Z,2340.00,2340.02,2.00
2026-06-19T05:30:00Z,2340.05,2340.07,2.10
```

## Event schema

`usd_events.csv` must use this header:

```text
ts_utc,currency,impact,title
```

Allowed `impact` values:

```text
LOW,MEDIUM,HIGH
```

High-impact USD events may cap confidence. The project does not infer event direction.

Example:

```csv
ts_utc,currency,impact,title
2026-06-18T12:30:00Z,USD,HIGH,Core Retail Sales m/m
```

## Run

```bash
python -m xau_lfx.pipeline validate-sources --input-dir data/xauusd --event-file data/xauusd/usd_events.csv

python -m xau_lfx.pipeline run-once --input-dir data/xauusd --event-file data/xauusd/usd_events.csv --out-dir artifacts

python -m xau_lfx.pipeline report --artifact-dir artifacts --write-md

python -m xau_lfx.pipeline site --artifact-dir artifacts --out-dir site
```

## Do not commit private broker data

Do not commit broker/vendor exports unless redistribution rights are verified and documented. Use synthetic or explicitly redistributable samples for public examples.
