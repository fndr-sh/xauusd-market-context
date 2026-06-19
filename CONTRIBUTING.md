# Contributing

Contributions should improve reproducibility, validation, documentation, tests, or source adapters without changing the monitor-only contract.

Start with `ROADMAP.md`, `docs/ISSUE_BACKLOG_SEED.md`, and the public issue backlog. Use an existing issue when possible so the scope, owner, and acceptance criteria are visible before implementation.

## Accepted contribution types

- CSV parser improvements.
- Data-quality checks.
- Docs and examples.
- Tests.
- Optional adapters that do not require paid services by default.
- Community documentation and demo clarity.

## Not accepted in this branch

- Execution logic.
- Account-risk or position sizing logic.
- Directional trade-call language.
- Claims of centralized XAUUSD orderflow.
- Hidden external scraping.

## LFX external boundary

Read `docs/LFX_EXTERNAL_BASELINE.md` before proposing LFX-derived work. Contributions must not copy Pine thresholds, score weights, route logic, or private screenshot assumptions into the Python project. Density remains a future reference-only proposal until a separate module specification is locked.

## Pull-request checks

Run:

```bash
python scripts/check_release_readiness.py --strict
python -m compileall xau_lfx scripts
python -m pytest -q
python -m build
```

State which issue the change addresses and list the affected files. Maintainer ownership and review expectations are documented in `MAINTAINERS.md`.
