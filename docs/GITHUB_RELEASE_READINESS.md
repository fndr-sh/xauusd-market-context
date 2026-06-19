# GitHub Release Readiness

Status: `v2.3.0-community-backlog-ready`

## Required checks

Run from the repository root:

```bash
python -m compileall xau_lfx scripts
PYTHONPATH=. pytest -q
python -m xau_lfx.pipeline demo --out-dir demo-artifacts --site-dir demo-site
python scripts/check_release_readiness.py --strict
python -m build
```

## Required files

The public release pack must include:

- `README.md`
- `LICENSE`
- `NOTICE`
- `DATA_LICENSE.md`
- `DISCLAIMER.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `CHANGELOG.md`
- `pyproject.toml`
- `MANIFEST.in`
- `ROADMAP.md`
- `MAINTAINERS.md`
- local CSV docs
- artifact quality docs
- schema reference
- CLI usage guide
- LFX external baseline contract
- sample data fixtures
- sample generated artifacts
- GitHub issue templates
- GitHub test workflow
- GitHub Pages workflow
- GitHub issue triage workflow
- user feedback issue template

## Expected readiness result

```json
{
  "status": "READY",
  "blockers": [],
  "warnings": []
}
```

## Release contract

Publishing this repository does not unlock trading behavior. The project remains:

```text
MONITOR_ONLY
NO_EXECUTION
NO_BUY_SELL_SIGNAL
NO_FINANCIAL_ADVICE
NO_STATISTICAL_EDGE_CLAIM
```
