# Data Source Policy

This project accepts local, user-controlled data first.

## Supported in v1.2

- MT5 or broker OHLCV CSV files for `XAUUSD_M5`, `XAUUSD_M15`, and `XAUUSD_H1`.
- Broker spread CSV file.
- Manual USD event CSV file.

## Source limits

- Broker OHLCV is broker-specific.
- `tick_volume` is broker tick activity, not centralized traded volume.
- Broker spread is not institutional consensus.
- Event data is risk context only.
- No centralized XAUUSD spot orderbook is claimed.

## Deferred source families

- Live MT5 bridge.
- Paid futures or macro vendors.
- Licensed open interest datasets.
- Telegram or desktop alerting.
- Pine bridge.
