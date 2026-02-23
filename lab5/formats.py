from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias


@dataclass(frozen=True)
class JsonFormatContext:
    tag: Literal["json"] = "json"
    indent: int = 2


@dataclass(frozen=True)
class CsvFormatContext:
    tag: Literal["csv"] = "csv"
    delimiter: str = ","
    include_header: bool = True


@dataclass(frozen=True)
class TextFormatContext:
    tag: Literal["text"] = "text"
    include_index: bool = True


OutputFormat: TypeAlias = JsonFormatContext | CsvFormatContext | TextFormatContext
