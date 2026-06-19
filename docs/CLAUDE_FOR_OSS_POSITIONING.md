# Claude for Open Source Positioning

This repository is positioned as a practical OSS utility for auditable XAUUSD market-context artifacts, not as a trading-signal system.

## Fit

The project is strongest as:

```text
Local data artifact generator + quality gate + static research report/demo
```

It helps users:

- validate local MT5/broker CSV exports;
- generate auditable JSON artifacts;
- inspect data quality and confidence caps;
- produce Markdown and static HTML reports;
- avoid false precision around XAUUSD broker-fragmented data.

## OSS readiness foundation

v1.4.0 includes:

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
- release-readiness checker.

## What should not be claimed

Do not position this as:

- a profitable trading bot;
- a buy/sell indicator;
- a real dealer-inventory feed;
- a real retail-positioning feed;
- an institutional XAUUSD orderbook;
- a statistical edge engine.

## Adoption strategy

The immediate goal is to make the repo useful enough that users can clone it, run the sample workflow, inspect the generated artifacts, and adapt local CSV files safely.

Recommended next public milestones:

1. v1.4.0: public publish pack and first GitHub release.
2. v1.5.0: static report polish and downloadable sample artifacts.
3. v1.6.0: local export compatibility matrix for broker CSV shapes.
4. v1.7.0: optional additional non-redistributed reference-source adapters.
