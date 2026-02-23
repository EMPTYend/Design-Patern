from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateScoresParams:
    delta: float
    only_active: bool = True
    deactivate_below: float | None = None


@dataclass(frozen=True)
class SortRecordsParams:
    by: str = "score"
    descending: bool = True
