@echo off
cd /d %~dp0
python -m xau_lfx.pipeline run-once
python -m xau_lfx.web serve --host 127.0.0.1 --port 8766
pause
