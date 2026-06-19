# Schema Reference

## OHLCV CSV

Required file names:

```text
XAUUSD_M5.csv
XAUUSD_M15.csv
XAUUSD_H1.csv
```

Required columns:

| Column | Type | Rule |
|---|---|---|
| `ts_utc` | string | ISO-8601 timestamp with timezone |
| `open` | number | finite numeric value |
| `high` | number | finite numeric value |
| `low` | number | finite numeric value |
| `close` | number | finite numeric value |
| `tick_volume` | number | broker tick activity, not centralized volume |

## Spread CSV

Required file name:

```text
XAUUSD_spread.csv
```

Required columns:

| Column | Type | Rule |
|---|---|---|
| `ts_utc` | string | ISO-8601 timestamp with timezone |
| `bid` | number | finite numeric value |
| `ask` | number | finite numeric value |
| `spread_points` | number | finite numeric value |

## Event CSV

Required columns:

| Column | Type | Rule |
|---|---|---|
| `ts_utc` | string | ISO-8601 timestamp with timezone |
| `currency` | string | example: `USD` |
| `impact` | enum | `LOW`, `MEDIUM`, `HIGH` |
| `title` | string | event label |

Event rows are used only as risk context. They do not imply direction.
