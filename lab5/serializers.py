from __future__ import annotations

import csv
import io
import json
from typing import Sequence

from abstractions import RecordSerializer
from formats import CsvFormatContext, JsonFormatContext, OutputFormat, TextFormatContext
from models import DataRecord


class TaggedUnionRecordSerializer(RecordSerializer):
    def serialize(self, records: Sequence[DataRecord], output_format: OutputFormat) -> str:
        if isinstance(output_format, JsonFormatContext):
            return self._serialize_json(records, output_format)
        if isinstance(output_format, CsvFormatContext):
            return self._serialize_csv(records, output_format)
        if isinstance(output_format, TextFormatContext):
            return self._serialize_text(records, output_format)
        raise TypeError(f"Unsupported format type: {type(output_format).__name__}")

    def _serialize_json(
        self,
        records: Sequence[DataRecord],
        output_format: JsonFormatContext,
    ) -> str:
        rows = [record.to_dict() for record in records]
        return json.dumps(rows, indent=output_format.indent, ensure_ascii=True)

    def _serialize_csv(
        self,
        records: Sequence[DataRecord],
        output_format: CsvFormatContext,
    ) -> str:
        buffer = io.StringIO()
        field_names = ["record_id", "name", "score", "active", "source"]
        writer = csv.DictWriter(
            buffer,
            fieldnames=field_names,
            delimiter=output_format.delimiter,
            lineterminator="\n",
        )
        if output_format.include_header:
            writer.writeheader()
        for record in records:
            writer.writerow(record.to_dict())
        return buffer.getvalue()

    def _serialize_text(
        self,
        records: Sequence[DataRecord],
        output_format: TextFormatContext,
    ) -> str:
        lines: list[str] = []
        for index, record in enumerate(records, start=1):
            prefix = f"{index}. " if output_format.include_index else ""
            lines.append(
                (
                    f"{prefix}id={record.record_id}, name={record.name},"
                    f" score={record.score}, active={record.active}, source={record.source}"
                )
            )
        return "\n".join(lines)
