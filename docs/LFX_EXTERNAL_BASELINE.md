# LFX External Baseline Contract

STATUS: LOCKED_REFERENCE
MODE: CONTROL
TARGET: External Python repository only

This contract defines how the external `xauusd-market-context` repository may use the user-provided LFX-2 material without modifying or reproducing the Pine baseline.

## Reviewed sources

- `LFX-2_PROJECT_STATE_v7.1-F_FULL_FINAL (1).md`
- `LFX-2_v7.1-F-FINAL-READABILITY-LOCK (1).txt`
- `LFX-2_v7.2-A-R5-PRACTICAL-DENSITY-ROLE-TEXT.txt`

The v7.1-F source is the locked Mission Control readability baseline. The v7.2-A-R5 source adds a behavior-gated density adapter and practical density role text. Neither source is copied into this repository.

## External-use boundary

The external repository may preserve these concepts as documentation and monitor-only artifact semantics:

- separate past, current, and conditional-next context;
- structural context must not be presented as an intraday instruction;
- manual event risk may reduce confidence but must not infer direction;
- practical zone text may describe sweep, reset, barrier, release-reference, structural-reference, reaction, or absorption context;
- inventory language must remain a footprint hypothesis;
- retail inducement language must remain a footprint proxy;
- density may only be treated as confluence or reference context after a separate implementation scope is locked.

## Density boundary

The v7.2-A-R5 density adapter is reference material, not an implemented Python feature in v2.3.0.

Any future external density work must satisfy all of the following:

- use user-owned or rights-cleared local data;
- preserve broker tick activity as `tick_volume`, not centralized traded volume;
- keep density subordinate to validated source quality and monitor context;
- treat a distant profile concentration as reference only;
- avoid mechanical target, execution, or directional trade-call semantics;
- document source family, freshness, limitations, and confidence impact;
- require a separately locked module specification and tests before implementation.

## Prohibited transfer

The external repository must not silently copy or reinterpret:

- Pine thresholds, constants, score weights, or state transitions;
- route or debt decision logic;
- private runtime assumptions from TradingView screenshots;
- claims of actual dealer inventory or actual retail positioning;
- broker tick activity as centralized market volume;
- predictive, profitability, or financial-advice behavior.

## Phase E effect

Phase E uses the LFX material only to constrain documentation, contributor tasks, issue wording, and roadmap boundaries. It does not add an external density engine, mutate artifact calculations, or change the Pine source.
