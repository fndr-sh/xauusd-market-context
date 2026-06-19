# Source Validation Hardening

Version: v1.5.0

This project treats local MT5/broker CSV files as user-provided evidence, not as trusted truth. The source validator rejects malformed rows before the pipeline builds market-context artifacts.

## OHLCV validation

Required columns:

```text
ts_utc,open,high,low,close,tick_volume
```

Rules:

- `ts_utc` must be ISO-8601 and timezone-aware.
- Timestamps must be strictly increasing.
- Duplicate timestamps are rejected.
- Numeric fields must be finite numbers.
- `high` must be greater than or equal to `open`, `close`, and `low`.
- `low` must be less than or equal to `open`, `close`, and `high`.
- Negative `tick_volume` is rejected.
- `tick_volume` remains broker tick activity, not centralized real volume.

## Spread validation

Required columns:

```text
ts_utc,bid,ask,spread_points
```

Rules:

- `ts_utc` must be ISO-8601 and timezone-aware.
- Timestamps must be strictly increasing.
- Duplicate timestamps are rejected.
- Numeric fields must be finite numbers.
- `ask` must be greater than or equal to `bid`.
- `spread_points` must not be negative.

The validator does not infer point size or pip conversion. Broker-specific spread conventions remain explicit user responsibility.

## Safety contract

Validation hardening does not create trade signals, execution instructions, profitability claims, real dealer-inventory claims, or real retail-positioning claims.
