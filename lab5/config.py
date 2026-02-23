from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from formats import OutputFormat
from transform_params import SortRecordsParams, UpdateScoresParams


@dataclass(frozen=True)
class FileReaderConfig:
    kind: Literal["file"] = "file"
    path: str = "data/input_records.json"


@dataclass(frozen=True)
class RandomReaderConfig:
    kind: Literal["random"] = "random"
    count: int = 5
    seed: int | None = None


ReaderConfig: TypeAlias = FileReaderConfig | RandomReaderConfig


@dataclass(frozen=True)
class FileWriterConfig:
    kind: Literal["file"] = "file"
    path: str = "data/output.txt"


@dataclass(frozen=True)
class ConsoleWriterConfig:
    kind: Literal["console"] = "console"


WriterConfig: TypeAlias = FileWriterConfig | ConsoleWriterConfig


@dataclass(frozen=True)
class ChainConfig:
    reader: ReaderConfig
    writer: WriterConfig
    output_format: OutputFormat
    update_scores: UpdateScoresParams
    sort_records: SortRecordsParams
