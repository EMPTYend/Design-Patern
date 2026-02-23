from __future__ import annotations

from typing import Iterable

from abstractions import TransformationStep
from models import DataRecord
from transform_params import SortRecordsParams, UpdateScoresParams
from transforms import sort_records, update_scores


class UpdateScoresStep(TransformationStep):
    def __init__(self, params: UpdateScoresParams) -> None:
        self._params = params

    @property
    def name(self) -> str:
        return (
            f"UpdateScores(delta={self._params.delta},"
            f" only_active={self._params.only_active})"
        )

    def apply(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        return update_scores(records, self._params)


class SortRecordsStep(TransformationStep):
    def __init__(self, params: SortRecordsParams) -> None:
        self._params = params

    @property
    def name(self) -> str:
        return (
            f"SortRecords(by={self._params.by},"
            f" descending={self._params.descending})"
        )

    def apply(self, records: Iterable[DataRecord]) -> list[DataRecord]:
        return sort_records(records, self._params)
