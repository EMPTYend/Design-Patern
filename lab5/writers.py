from __future__ import annotations

from pathlib import Path
from typing import Sequence

from abstractions import RecordSerializer, SourceWriter
from formats import OutputFormat
from models import DataRecord


class FileSourceWriter(SourceWriter):
    def __init__(self, path: str, serializer: RecordSerializer) -> None:
        self._path = Path(path)
        self._serializer = serializer

    def write(self, records: Sequence[DataRecord], output_format: OutputFormat) -> None:
        content = self._serializer.serialize(records, output_format)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(content, encoding="utf-8")


class ConsoleSourceWriter(SourceWriter):
    def __init__(self, serializer: RecordSerializer) -> None:
        self._serializer = serializer

    def write(self, records: Sequence[DataRecord], output_format: OutputFormat) -> None:
        content = self._serializer.serialize(records, output_format)
        print(content)
