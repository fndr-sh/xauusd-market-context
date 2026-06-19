# Issue Backlog Seed

STATUS: PHASE_E_PUBLIC_BACKLOG
MODE: CONTROL
TRADING_MODE: MONITOR_ONLY

These twelve issues are ready for public creation. Each task is independently scoped and must preserve `docs/LFX_EXTERNAL_BASELINE.md`.

## Good first issues

### Add a README screenshot for the static demo

Labels: `good first issue`, `docs`, `demo`

Scope:

- Generate the site from committed synthetic fixtures.
- Add one readable screenshot to the README or demo walkthrough.
- Do not include broker/vendor data or change runtime behavior.

Acceptance:

- The image shows the current static demo.
- Its source and refresh command are documented.

### Improve MT5 CSV export examples

Labels: `good first issue`, `docs`

Scope:

- Clarify M5, M15, H1, and spread CSV export examples.
- Use synthetic rows and the existing schemas.
- Do not add a live account connection.

Acceptance:

- A reader can identify the required headers, UTC timestamp format, and file names.

### Add malformed CSV test fixtures

Labels: `good first issue`, `validation`

Scope:

- Add small synthetic fixtures for duplicate timestamps, non-increasing timestamps, invalid OHLC relationships, and invalid spread values.
- Preserve current validation semantics.

Acceptance:

- Each fixture has a focused test that asserts the existing error behavior.

### Add CLI output examples for supported operating systems

Labels: `good first issue`, `docs`

Scope:

- Document `xau-lfx demo` output on Windows, Linux, and macOS.
- Show generated-file paths without machine-specific personal directories.

Acceptance:

- `docs/CLI_USAGE.md` includes concise platform examples and activation commands.

### Add artifact reading order to the static demo

Labels: `good first issue`, `docs`, `demo`

Scope:

- Explain which generated artifact a new user should inspect first.
- Limit the change to static HTML wording and documentation.

Acceptance:

- The demo identifies artifact quality, context summary, report, and source policy in a clear order.

## Validation and documentation issues

### Add context-summary fixture snapshots

Labels: `help wanted`, `validation`

Scope:

- Add stable snapshot coverage for `xau_context_summary.json` using synthetic data.
- Preserve monitor-only wording and existing calculations.

Acceptance:

- Tests identify intentional field or wording changes without relying on live data.

### Add source-quality explanation examples

Labels: `help wanted`, `docs`

Scope:

- Document stale data, missing timeframe, unstable spread, and high-impact USD event cases.
- Explain confidence effects without changing the scoring formula.

Acceptance:

- Each example links an input condition to an observable artifact field.

### Document sanitized validation-report sharing

Labels: `help wanted`, `docs`

Scope:

- Explain how users can share validation output without raw broker/vendor data, credentials, or account identifiers.
- Include a short redaction checklist.

Acceptance:

- A user can prepare a reproducible issue using synthetic or sanitized evidence.

## Schema and research issues

### Define an artifact schema compatibility policy

Labels: `schema`, `research`

Scope:

- Propose compatibility rules for generated JSON artifacts.
- Treat v2.1.0 schema implementation as skipped and not delivered.
- Do not change artifact fields in this issue.

Acceptance:

- The proposal distinguishes compatible additions from breaking changes.

### Propose JSON schema validation coverage

Labels: `schema`, `research`

Scope:

- Inventory generated JSON artifacts and propose validation ownership.
- Identify required fields and uncertainty without adding fake precision.
- Proposal only; implementation requires a separately locked scope.

Acceptance:

- Every current JSON artifact is listed with a validation recommendation.

### Document LFX monitor vocabulary mapping

Labels: `research`, `docs`

Scope:

- Map past/current/conditional-next, reset, barrier, release-reference, structural-reference, and density-reference language to external artifact documentation.
- Keep density as confluence or reference only.
- Do not copy Pine thresholds, score weights, or route logic.

Acceptance:

- The mapping cites `docs/LFX_EXTERNAL_BASELINE.md` and preserves hypothesis/proxy language.

### Define an optional local reference-data adapter contract

Labels: `research`, `help wanted`

Scope:

- Draft a contract for future user-owned local reference CSV files.
- Cover source rights, timezone, freshness, validation, and confidence impact.
- No live scraping, vendor redistribution, or production adapter in this issue.

Acceptance:

- The proposal is optional, monitor-only, and cannot change the base run when data is absent.

## Maintainer execution note

Create the required labels before publishing these issues. The public issues must use the titles, scopes, and acceptance criteria above without adding runtime promises or unsupported market claims.
