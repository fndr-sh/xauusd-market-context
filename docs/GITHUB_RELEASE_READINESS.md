# GitHub Release Readiness

Status: `v1.4.0-public-publish-ready`

## Required checks

Run from the repository root:

```bash
python -m compileall xau_lfx scripts
PYTHONPATH=. pytest -q
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
- local CSV docs
- artifact quality docs
- schema reference
- sample data fixtures
- sample generated artifacts
- GitHub issue templates
- GitHub test workflow
- GitHub Pages workflow

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
