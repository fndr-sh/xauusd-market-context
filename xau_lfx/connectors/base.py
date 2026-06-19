from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SourceRequest:
    source_id: str
    symbol: str
    timeframe: str
    limit: int = 300


class Connector(Protocol):
    source_id: str

    def fetch(self, request: SourceRequest) -> dict:
        ...
