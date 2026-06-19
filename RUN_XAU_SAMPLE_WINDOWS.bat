@echo off
cd /d %~dp0
python -m xau_lfx.pipeline validate-sources --input-dir examples\sample-data --event-file examples\sample-data\usd_events.csv
python -m xau_lfx.pipeline run-once --input-dir examples\sample-data --event-file examples\sample-data\usd_events.csv --out-dir artifacts
python -m xau_lfx.pipeline report --artifact-dir artifacts --write-md
python -m xau_lfx.pipeline site --artifact-dir artifacts --out-dir site
echo.
echo Static demo generated at: site\index.html
pause
