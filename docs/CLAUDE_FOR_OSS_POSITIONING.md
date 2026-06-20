# Claude for Open Source Positioning

This repository is positioned as a practical OSS utility for auditable XAUUSD market-context artifacts, not as a trading-signal system.

## Fit

The project is strongest as:

```text
Local data artifact generator + quality gate + private live monitor + static research report/demo
```

It helps users:

- validate local MT5/broker CSV exports;
- generate auditable JSON artifacts;
- inspect data quality and confidence caps;
- produce Markdown and static HTML reports;
- inspect OANDA Practice M5/M15/H1 candles on a private-host dashboard without exposing the token to browser code;
- avoid false precision around XAUUSD broker-fragmented data.

## OSS readiness foundation

v2.4.0 includes:

- Apache-2.0 license;
- data redistribution policy;
- disclaimer;
- contribution guide;
- security policy;
- code of conduct;
- issue templates;
- CI test workflow;
- GitHub Pages static demo workflow;
- sample synthetic fixtures;
- release-readiness checker;
- public contributor backlog and triage workflow;
- four synthetic real-world usage cases and sanitized report-sharing guidance;
- optional OANDA Practice live dashboard with fixed five-second refresh.

## What should not be claimed

Do not position this as:

- a profitable trading bot;
- a directional-call indicator;
- a real dealer-inventory feed;
- a real retail-positioning feed;
- an institutional XAUUSD orderbook;
- a statistical edge engine.

## Adoption strategy

The immediate goal is to make the repo useful enough that users can clone it, run the sample workflow, inspect the generated artifacts, and adapt local CSV files safely.

Current progression gates:

1. `v2.4.x`: convert the active external fork into a reviewed contribution and close only the remaining Phase F documentation gaps.
2. `v2.5.0`: implement optional local reference-data adapters only after a separate Phase G specification is locked.
3. `v3.0.0`: declare a stable schema, CLI, documentation, and package path only after real usage feedback supports that claim.
4. Claude for Open Source track: record verifiable adoption and maintainer evidence, then re-check the official program criteria immediately before any application.

Technical releases alone are not impact evidence. Stars, forks, external issues, external pull requests, release downloads, Pages traffic, and documented user workflows must be reported as observed facts without artificial engagement.
