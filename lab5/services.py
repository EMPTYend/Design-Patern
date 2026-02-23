from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from abstractions import SourceReader, SourceWriter, TransformationStep
from formats import OutputFormat
from models import DataRecord


class ReadService:
    def __init__(self, reader: SourceReader) -> None:
        self._reader = reader

    def execute(self) -> list[DataRecord]:
        return self._reader.read()


class TransformationPipelineService:
    def __init__(self, steps: Sequence[TransformationStep]) -> None:
        self._steps = list(steps)

    def execute(self, records: Sequence[DataRecord]) -> list[DataRecord]:
        current = list(records)
        for step in self._steps:
            current = step.apply(current)
        return current

    def describe_steps(self) -> list[str]:
        return [step.name for step in self._steps]


class SaveService:
    def __init__(self, writer: SourceWriter) -> None:
        self._writer = writer

    def execute(self, records: Sequence[DataRecord], output_format: OutputFormat) -> None:
        self._writer.write(records, output_format)


@dataclass(frozen=True)
class FlowResult:
    read_count: int
    written_count: int
    steps: list[str]


class DataFlowService:
    def __init__(
        self,
        read_service: ReadService,
        transform_service: TransformationPipelineService,
        save_service: SaveService,
        output_format: OutputFormat,
    ) -> None:
        self._read_service = read_service
        self._transform_service = transform_service
        self._save_service = save_service
        self._output_format = output_format

    def execute(self) -> FlowResult:
        source_records = self._read_service.execute()
        transformed = self._transform_service.execute(source_records)
        self._save_service.execute(transformed, self._output_format)
        return FlowResult(
            read_count=len(source_records),
            written_count=len(transformed),
            steps=self._transform_service.describe_steps(),
        )
