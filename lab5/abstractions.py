from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from formats import OutputFormat
from models import DataRecord


class SourceReader(ABC):
    @abstractmethod
    def read(self) -> list[DataRecord]:
        raise NotImplementedError


class SourceWriter(ABC):
    @abstractmethod
    def write(self, records: Sequence[DataRecord], output_format: OutputFormat) -> None:
        raise NotImplementedError


class RecordSerializer(ABC):
    @abstractmethod
    def serialize(self, records: Sequence[DataRecord], output_format: OutputFormat) -> str:
        raise NotImplementedError


class TransformationStep(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def apply(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        raise NotImplementedError
