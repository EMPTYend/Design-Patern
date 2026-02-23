from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized in {"1", "true", "yes", "y"}
    return bool(value)


@dataclass(frozen=True)
class DataRecord:
    record_id: int
    name: str
    score: float
    active: bool
    source: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "DataRecord":
        return DataRecord(
            record_id=int(data["record_id"]),
            name=str(data["name"]),
            score=float(data["score"]),
            active=_to_bool(data["active"]),
            source=str(data.get("source", "unknown")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "name": self.name,
            "score": self.score,
            "active": self.active,
            "source": self.source,
        }
