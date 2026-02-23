from __future__ import annotations

import json
import random
from pathlib import Path
from urllib.request import urlopen

from abstractions import SourceReader
from models import DataRecord


class FileJsonSourceReader(SourceReader):
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def read(self) -> list[DataRecord]:
        payload = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Expected top-level JSON array for records")
        return [DataRecord.from_dict(item) for item in payload]


class RandomSourceReader(SourceReader):
    def __init__(self, count: int, seed: int | None = None) -> None:
        self._count = count
        self._seed = seed

    def read(self) -> list[DataRecord]:
        rng = random.Random(self._seed)
        names = [
            "Alice",
            "Bob",
            "Carol",
            "David",
            "Eve",
            "Frank",
            "Grace",
            "Heidi",
        ]
        records: list[DataRecord] = []
        for index in range(self._count):
            records.append(
                DataRecord(
                    record_id=1000 + index,
                    name=rng.choice(names),
                    score=round(rng.uniform(10, 100), 2),
                    active=rng.choice([True, True, False]),
                    source="random",
                )
            )
        return records


class HttpJsonSourceReader(SourceReader):
    def __init__(self, url: str, timeout_sec: float = 5.0) -> None:
        self._url = url
        self._timeout_sec = timeout_sec

    def read(self) -> list[DataRecord]:
        with urlopen(self._url, timeout=self._timeout_sec) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Expected top-level JSON array for records")
        return [DataRecord.from_dict(item) for item in payload]
