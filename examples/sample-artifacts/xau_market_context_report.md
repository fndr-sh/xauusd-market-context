# XAUUSD Market Context Report

Generated: 2026-06-19T17:55:25.911894+00:00  
Mode: monitor-only research artifact  
Symbol: XAUUSD

## Artifact Quality

- Status: OK
- Quality score: 96.33 / 100
- Quality grade: A
- Confidence cap: 0.75
- Source count: 2

## Source Coverage

- Present timeframes: M5, M15, H1
- Freshness score: 84.83 / 100
- Coverage score: 100.0 / 100
- Schema score: 100.0 / 100
- Spread score: 86.05 / 100
- Event score: 100.0 / 100

## Context Summary

- Latest close: 2338.83
- Freshness age minutes: 655.43
- Nearest session level: OFF_SESSION low at 2337.15, distance=1.68
- Spread state: STABLE
- Event risk state: CONTEXT
- Quality status: OK
- Quality grade: A

## Confidence Explanation

- M5/M15/H1 local bar coverage is complete.
- Latest local bars are fresh relative to the 72-hour freshness window.
- Spread source is stable enough for monitor context.
- Event file is loaded and used as risk context only.


## Monitor Focus

- Observe behavior around OFF_SESSION low (2337.15); distance 1.68 points.
- Compare M15 context with M5 confirmation behavior and H1 structural context.
- Keep spread stability on the monitor list during active sessions.
- Keep the event file current before major USD macro windows.


## M15 Session Map

- ASIA: bars=28, high=2342.0, low=2336.93, range=5.07
- LONDON: bars=1, high=2340.73, low=2336.93, range=3.8
- OFF_SESSION: bars=3, high=2341.5, low=2337.15, range=4.35

## Event Risk Context

- Risk state: CONTEXT
- Event count: 2
- High-impact USD events: 1
- Note: Event CSV loaded. Events are used only as risk context.

## Current Read

- Latest cross-timeframe median close: 2338.83
- Headline: External XAU context has passed the initial data-readiness gate.
- Now: The system can provide bounded monitor context from validated external sources.

## What This Artifact Cannot Claim

- It cannot infer centralized spot-gold orderflow from broker CSV files.
- It cannot infer actual dealer inventory or actual retail-side positioning.
- It cannot provide execution instructions or profitability claims.
- It cannot treat broker tick activity as centralized traded volume.

## Limitations

- Monitor-only context summary; not an execution plan.
- Broker tick activity remains a local activity proxy, not centralized volume.
- Session levels are references from supplied CSV data only.

## Warnings

- USD_HIGH_IMPACT_EVENT_PRESENT

## Errors

- No schema or source errors were emitted.
