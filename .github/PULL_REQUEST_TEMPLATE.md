## Scope

Describe the module changed and why it is needed.

## Release contract check

- [ ] Monitor-only behavior preserved.
- [ ] No execution/order/account-risk logic added.
- [ ] No claim of true dealer inventory or real retail positioning added.
- [ ] No statistical/profitability claim added.
- [ ] Tests added or updated.
- [ ] Documentation updated when user-facing behavior changed.

## Validation

Paste the commands run:

```text
python -m compileall xau_lfx scripts
PYTHONPATH=. pytest -q
```
