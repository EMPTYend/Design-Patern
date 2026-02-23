from __future__ import annotations

from dataclasses import replace
from typing import Callable, Iterable

from models import DataRecord
from transform_params import SortRecordsParams, UpdateScoresParams


def update_scores(records: Iterable[DataRecord], params: UpdateScoresParams) -> list[DataRecord]:
    transformed: list[DataRecord] = []
    for record in records:
        if params.only_active and not record.active:
            transformed.append(record)
            continue

        next_score = round(record.score + params.delta, 2)
        next_active = record.active
        if params.deactivate_below is not None and next_score < params.deactivate_below:
            next_active = False

        transformed.append(
            replace(record, score=next_score, active=next_active)
        )
    return transformed


def sort_records(records: Iterable[DataRecord], params: SortRecordsParams) -> list[DataRecord]:
    selectors: dict[str, Callable[[DataRecord], object]] = {
        "id": lambda record: record.record_id,
        "name": lambda record: record.name,
        "score": lambda record: record.score,
        "active": lambda record: record.active,
        "source": lambda record: record.source,
    }
    selector = selectors.get(params.by)
    if selector is None:
        raise ValueError(f"Unsupported sort field: {params.by}")
    return sorted(records, key=selector, reverse=params.descending)
