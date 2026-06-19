# XAU-LFX External Data Foundation v1.0

STATUS: SPEC_LOCK_CANDIDATE  
MODE: CONTROL  
BASELINE: LFX-2 v7.1-F Mission Control / Behavior Surveillance OS  
REFERENCE_ARCHITECTURE: BTC-LFX v3.5 Composite Market Data Foundation  
TARGET_SYMBOL: XAUUSD / GOLD reference  
TARGET_USE: External-data liquidity surveillance foundation for discretionary XAUUSD MM-following workflow  
TRADING_MODE: MONITOR_ONLY  
AUTO_ENTRY: NO  
BUY_SELL_SIGNAL: NO  
STRATEGY_MODE: NO  
REAL_MM_INVENTORY_CLAIM: NO  
REAL_RETAIL_POSITIONING_CLAIM: NO  
STATISTICAL_EDGE_CLAIM: NO

---

## 1. OBJECTIVE_LOCK

Build a sidecar external-data foundation that extends LFX-2 beyond normal TradingView/Pine constraints by collecting, normalizing, scoring, and exposing XAUUSD-relevant boundary data.

The system must not replace or mutate LFX-2 v7.1-F. It runs beside it and produces external state for dashboard / MT5 / Telegram / optional Pine visualization.

Core questions remain locked:

1. MM đã làm gì?
2. MM đang làm gì?
3. MM có thể làm gì tiếp?
4. Trader nên theo dõi gì để đi theo MM?

External data must improve evidence quality, not convert the system into a trade-signal engine.

---

## 2. WHY THIS BRANCH EXISTS

TradingView Pine is suitable for chart overlay and local market-structure monitoring, but it is not suitable as the main collector for external market data.

This branch separates concerns:

```text
External Collector
→ Normalizer
→ Composite / Proxy Engine
→ XAU Liquidity State Engine
→ API / Dashboard / MT5 / Telegram
→ Optional Pine display bridge
```

LFX-2 v7.1-F remains the baseline Pine monitor. The new foundation supplies external context that Pine alone cannot reliably collect.

---

## 3. HARD_RULES

Forbidden:

- No BUY / SELL command.
- No entry, SL, TP, position sizing, or auto execution.
- No strategy() conversion.
- No claim of true centralized XAUUSD orderbook.
- No claim of real MM inventory.
- No claim of real retail positioning.
- No statistical edge claim before forward validation.
- No direct mutation of LFX-2 v7.1-F locked Pine logic.
- No fake precision from weak proxy data.
- No using one broker CFD feed as institutional truth.

Allowed:

- External data collection.
- Public/proxy market-data normalization.
- Composite OHLCV / session pressure proxy.
- Futures-market reference proxy.
- News / volatility / spread-risk state.
- Confidence caps based on data quality.
- WATCH / CONTEXT / NO_TRADE alert wording only.
- MT5/Python dashboard bridge.
- Optional Pine visualization bridge using manually hosted/simplified state.

---

## 4. DATA_SOURCE_CONTRACT

### 4.1 Primary XAU data groups

| Group | Source Type | Examples | Purpose | Confidence Treatment |
|---|---|---|---|---|
| Spot/CFD Broker Feed | XAUUSD OHLC/tick from broker/MT5 | ICMarkets, other broker feeds if available | local traded feed / execution environment context | broker-specific, never institutional truth |
| Futures Reference | COMEX GC futures OHLC/volume/open interest if accessible | GC front contract / continuous reference | volume/OI pressure proxy | higher value than CFD tick volume but still proxy for spot XAUUSD |
| Macro Cross-Asset | DXY, US10Y, US real-yield proxy, USD index proxy | public market APIs / broker symbols | context filter, pressure regime | context-only; cannot override local liquidity event |
| Session Context | Asia/London/NY ranges, session volume/tick activity | computed internally | behavior timing / handoff state | high confidence if local data complete |
| Event Risk | CPI/FOMC/NFP calendar, high-impact USD events | calendar/manual feed | hard-block / caution state | binary risk cap, not directional signal |
| Spread/Volatility | broker spread, ATR expansion, gap/spike state | MT5/local feed | execution-risk monitor | cap confidence when unstable |

### 4.2 Explicit exclusions

- No centralized spot XAUUSD orderbook assumption.
- No retail-positioning truth unless source is explicitly provided and validated.
- No dealer gamma/options positioning unless a licensed/valid source is added later.
- No hidden paid/API dependency in default spec.

---

## 5. MODULE_MAP

### MODULE-X01 — Connector Layer

Role: Fetch raw external data from approved sources.

Inputs:
- source_id
- symbol mapping
- timeframe
- limit/window
- optional API key if user provides one later

Outputs:
- raw source payloads
- source metadata
- collection timestamp

Files proposed:

```text
xau_lfx/connectors/base.py
xau_lfx/connectors/mt5_feed.py
xau_lfx/connectors/public_market.py
xau_lfx/connectors/event_calendar.py
```

Notes:
- MT5 connector is preferred for broker-specific XAUUSD feed.
- Public market connector may cover DXY/US10Y/GC if accessible.
- No private execution API.

---

### MODULE-X02 — Normalizer

Role: Normalize all source payloads into strict internal schemas.

Outputs:

```text
xau_raw_ohlcv.json
xau_raw_tick_proxy.json
xau_raw_macro_context.json
xau_raw_event_risk.json
xau_raw_spread_state.json
```

Required fields:

```text
ts_utc
source_id
symbol
asset_class
timeframe
open
high
low
close
volume
volume_type
bid
ask
spread
quality_flags
```

Rules:
- Missing fields must be marked as missing, not autofilled.
- Tick volume must be tagged as `tick_volume`, not real volume.
- Futures volume must be tagged separately from CFD tick volume.

---

### MODULE-X03 — Data Quality Gate

Role: Score coverage, freshness, dispersion, completeness, and source reliability.

Outputs:

```text
xau_data_quality.json
```

Quality dimensions:

```text
freshness_score
coverage_score
source_count
missing_field_count
dispersion_score
session_completeness
spread_stability
news_risk_flag
confidence_cap
```

Rules:
- Weak data must cap downstream confidence.
- No module may upgrade confidence above the Data Quality Gate cap.
- If source_count is insufficient, output must state `INSUFFICIENT_SOURCE_COVERAGE`.

---

### MODULE-X04 — Composite OHLCV / Reference Engine

Role: Build a reference XAU price/flow context from available validated sources.

Outputs:

```text
xau_composite_ohlcv.json
```

Methods allowed:

```text
time alignment
median close
VWAP-like reference if true volume exists
broker-local primary with futures/macro confirmation
```

Rules:
- CFD tick volume cannot be treated as real traded volume.
- Composite must preserve source dispersion.
- If only one source exists, output is `single_source_reference`, not composite.

---

### MODULE-X05 — Session Liquidity Context Engine

Role: Compute Asia/London/NY ranges and session pressure state.

Outputs:

```text
xau_session_context.json
```

Computed states:

```text
asia_range
london_sweep_state
ny_handoff_state
prior_ny_high_low
session_displacement
session_absorption_proxy
session_reclaim_state
```

Purpose:
- Improve LFX-2 Mission Control context.
- Detect session handoff and sweep/reclaim behavior with stronger data quality awareness.

---

### MODULE-X06 — Macro Pressure Proxy Engine

Role: Contextualize XAUUSD movement against USD/rates proxies.

Outputs:

```text
xau_macro_pressure.json
```

States:

```text
usd_tailwind
usd_headwind
rates_tailwind
rates_headwind
macro_conflict
macro_neutral
```

Rules:
- Macro state is context only.
- Macro state cannot override a confirmed local liquidity event.
- Macro conflict reduces confidence, not generates direction.

---

### MODULE-X07 — Event / News Risk Gate

Role: Create hard block / caution state around high-impact USD events.

Outputs:

```text
xau_event_risk_state.json
```

States:

```text
NORMAL
PRE_EVENT_CAUTION
EVENT_HARD_BLOCK
POST_EVENT_SPREAD_NORMALIZATION
```

Rules:
- Event risk may block alert confidence.
- It must not create directional prediction.

---

### MODULE-X08 — XAU Liquidity-State Adapter

Role: Convert external evidence into LFX-compatible state rows.

Outputs:

```text
xau_lfx_external_state.json
```

State rows:

```text
external_context_label
external_pressure_label
external_quality_label
session_state_label
macro_state_label
event_risk_label
confidence_cap_label
watch_note
```

This is the only output layer that should be consumed by dashboard/MT5/Pine bridge.

---

### MODULE-X09 — Dashboard / API Layer

Role: Serve the external state locally.

Endpoints proposed:

```text
/api/xau/state
/api/xau/data-quality
/api/xau/session-context
/api/xau/macro-pressure
/api/xau/event-risk
/api/xau/composite-ohlcv
```

Default host:

```text
127.0.0.1
```

Default port:

```text
8766
```

Note: This port is proposed for the XAU sidecar and must not override BTC-LFX port 8765 unless user approves.

---

### MODULE-X10 — Pine / TradingView Bridge

Role: Optional visualization bridge.

Allowed bridge modes:

1. Manual state input table.
2. Lightweight webhook/text bridge through alerts if the user implements external relay.
3. Separate dashboard beside TradingView.
4. MT5 chart overlay instead of forcing Pine to consume external data.

Rules:
- Pine cannot be treated as the collector.
- Pine should not receive high-frequency external state directly.
- v7.1-F locked logic remains unchanged unless a dedicated integration branch is approved.

---

## 6. MTF_RULE_LOCK_FOR_XAU

Default XAU operational hierarchy:

```text
M15 = strategic zone / mission context
M5  = trigger confirmation context only
H1  = structural context only
```

Rules:
- M15 decides practical strategic zones.
- M5 cannot create strategic zones.
- H1 cannot trigger entry state.
- External data can cap or annotate confidence but cannot turn monitor-only output into direct signal.

---

## 7. ARTIFACT_CONTRACT

Default runtime artifacts:

```text
artifacts/xau_raw_scan.json
artifacts/xau_data_quality.json
artifacts/xau_composite_ohlcv.json
artifacts/xau_session_context.json
artifacts/xau_macro_pressure.json
artifacts/xau_event_risk_state.json
artifacts/xau_lfx_external_state.json
```

Retention:
- Keep timestamped snapshots for forward validation.
- Do not overwrite validation history unless user approves cleanup.

---

## 8. VALIDATION_PROTOCOL

Minimum forward validation before confidence language is upgraded:

```text
sample_count_min = 100 observed sessions/events
manual_review_required = true
asset = XAUUSD
timeframes = M5/M15/H1
```

Validation labels:

```text
RESEARCH_ONLY
INSUFFICIENT_SAMPLE
FORWARD_VALIDATION_ACTIVE
VALIDATED_CONTEXT_ASSISTANT
```

Invalid claims before validation:

```text
high edge
win rate
true MM intent
guaranteed follow-through
institutional orderflow proof
```

---

## 9. IMPLEMENTATION_PHASES

### Phase 1 — Spec + Skeleton

Deliver:
- package skeleton
- schema definitions
- config files
- artifact directory
- dummy local state output

No external API assumptions.

### Phase 2 — MT5 Local Feed Connector

Deliver:
- XAUUSD OHLC/tick/spread export path from MT5 or CSV
- local broker feed quality gate
- session context engine

### Phase 3 — Public Macro / Futures Reference

Deliver:
- optional public reference connector
- DXY/rates/GC proxy adapter if user provides source access
- macro pressure state

### Phase 4 — Mission Control Adapter

Deliver:
- external state rows compatible with LFX dashboard language
- WATCH / CONTEXT / NO_TRADE alert wording

### Phase 5 — MT5 / Dashboard / Pine Bridge

Deliver:
- local web dashboard
- MT5 overlay option
- optional Pine visualization bridge only after user approves integration route

---

## 10. ACCEPTANCE_CRITERIA

PASS if:

- v7.1-F Pine remains unchanged.
- External collector produces auditable JSON artifacts.
- Every source is tagged with source_id and quality flags.
- Data Quality Gate caps confidence.
- No BUY/SELL/entry semantics appear.
- M15/M5/H1 hierarchy remains locked.
- Weak proxy data is explicitly labeled as proxy.

FAIL if:

- Any module claims true centralized XAU orderbook.
- Tick volume is treated as real volume.
- Macro context becomes directional trade instruction.
- Pine is used as collector.
- Output becomes auto-entry / trade signal.

---

## 11. NEXT_ACTION_LOCK

Proceed next with:

```text
XAU-LFX External Data Foundation v1.0 — Phase 1 Skeleton
```

Required user-provided decision before Phase 2:

```text
Which local feed bridge will be used?
A = MT5 CSV/export from ICMarkets
B = Python pulls from broker/API source supplied by user
C = dashboard-only manual/public references first
```

Until that decision, implementation must stop at skeleton/spec/state contract.
