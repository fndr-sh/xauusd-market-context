# XAU-LFX Phase 2 — User Insight Layer

STATUS: PHASE_2_USER_INSIGHT_LAYER
MODE: CONTROL
TRADING_MODE: MONITOR_ONLY

## Objective

Upgrade the system from a runnable skeleton to a user-useful monitor by adding an explanation layer.

The layer must answer:

1. What can the system say now?
2. Why is confidence capped?
3. What should the operator monitor next?
4. What source/data must be activated before stronger context is allowed?

## Added module

```text
xau_lfx/engines/user_insight.py
```

## Added artifact

```text
artifacts/xau_user_insight.json
```

## Added endpoint

```text
/api/xau/user-insight
```

## Guardrails

- No execution wording.
- No position instruction.
- No centralized XAUUSD orderbook claim.
- No real inventory claim.
- No confidence upgrade above Data Quality Gate.

## Current behavior in no-source mode

The system reports that external XAU context is not decision-grade yet, then gives the operator a concrete checklist:

- activate at least two independent source families;
- prioritize MT5/broker feed freshness;
- add public macro/futures reference;
- add event-calendar risk state;
- keep Pine v7.1-F as the baseline visual field monitor until external data passes the gate.

## Validation

```text
python -m xau_lfx.pipeline run-once
PYTHONPATH=. pytest -q
```

Expected:

```text
INSUFFICIENT_SOURCE_COVERAGE
4 passed
```
