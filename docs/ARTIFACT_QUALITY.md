# Artifact Quality

`xau_artifact_quality.json` summarizes whether the current artifact set is usable for monitor-only research inspection.

## Fields

- `status`: `OK`, `WARN`, or `ERROR`.
- `quality_score`: 0 to 100.
- `quality_grade`: `A`, `B`, `C`, `D`, or `F`.
- `freshness_score`: timestamp recency.
- `coverage_score`: M5/M15/H1 coverage.
- `schema_score`: CSV schema validity.
- `session_score`: whether an M15 session map could be built.
- `spread_score`: broker spread stability.
- `event_score`: event file availability and caution state.
- `source_count`: active source families.
- `warnings`: source-quality flags.
- `errors`: schema or source errors.

## Grade thresholds

```text
A >= 90
B >= 80
C >= 65
D >= 50
F < 50
```

Quality score does not imply predictive performance. It only describes source and artifact readiness.
