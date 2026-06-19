from __future__ import annotations

import argparse

import uvicorn
from fastapi import FastAPI

from xau_lfx.config import ARTIFACTS
from xau_lfx.pipeline import run_once
from xau_lfx.utils import read_json

app = FastAPI(title="XAU-LFX External Data Foundation", version="1.4.0")


@app.get("/api/xau/state")
def get_state() -> dict:
    return read_json(ARTIFACTS["state"])


@app.get("/api/xau/data-quality")
def get_data_quality() -> dict:
    return read_json(ARTIFACTS["data_quality"])


@app.get("/api/xau/session-context")
def get_session_context() -> dict:
    return read_json(ARTIFACTS["session_context"])


@app.get("/api/xau/macro-pressure")
def get_macro_pressure() -> dict:
    return read_json(ARTIFACTS["macro_pressure"])


@app.get("/api/xau/event-risk")
def get_event_risk() -> dict:
    return read_json(ARTIFACTS["event_risk"])


@app.get("/api/xau/composite-ohlcv")
def get_composite_ohlcv() -> dict:
    return read_json(ARTIFACTS["composite_ohlcv"])


@app.get("/api/xau/user-insight")
def get_user_insight() -> dict:
    return read_json(ARTIFACTS["user_insight"])


@app.get("/api/xau/artifact-quality")
def get_artifact_quality() -> dict:
    return read_json(ARTIFACTS["artifact_quality"])


def serve(host: str, port: int) -> None:
    run_once()
    uvicorn.run("xau_lfx.web:app", host=host, port=port, reload=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="XAU-LFX External Data API")
    sub = parser.add_subparsers(dest="command", required=True)
    serve_parser = sub.add_parser("serve")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    if args.command == "serve":
        serve(args.host, args.port)


if __name__ == "__main__":
    main()
