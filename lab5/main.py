from __future__ import annotations

import json
from pathlib import Path

from config import ChainConfig, FileReaderConfig, FileWriterConfig, RandomReaderConfig
from factory import DataFlowServiceFactory
from formats import CsvFormatContext, JsonFormatContext, TextFormatContext
from transform_params import SortRecordsParams, UpdateScoresParams


def ensure_demo_file(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    demo_records = [
        {"record_id": 1, "name": "Mia", "score": 78.5, "active": True, "source": "file"},
        {"record_id": 2, "name": "Noah", "score": 61.0, "active": False, "source": "file"},
        {"record_id": 3, "name": "Liam", "score": 90.2, "active": True, "source": "file"},
        {"record_id": 4, "name": "Emma", "score": 55.1, "active": True, "source": "file"},
    ]
    path.write_text(json.dumps(demo_records, indent=2, ensure_ascii=True), encoding="utf-8")


def run_file_to_csv(base_dir: Path) -> None:
    input_path = base_dir / "data" / "input_records.json"
    output_path = base_dir / "data" / "output_file_to_csv.csv"
    ensure_demo_file(input_path)

    config = ChainConfig(
        reader=FileReaderConfig(path=str(input_path)),
        writer=FileWriterConfig(path=str(output_path)),
        output_format=CsvFormatContext(delimiter=";", include_header=True),
        update_scores=UpdateScoresParams(delta=5.0, only_active=True, deactivate_below=40.0),
        sort_records=SortRecordsParams(by="score", descending=True),
    )

    flow_service = DataFlowServiceFactory.create(config)
    result = flow_service.execute()

    print("Chain #1: file -> csv")
    print(" read_count =", result.read_count)
    print(" written_count =", result.written_count)
    print(" steps =", ", ".join(result.steps))
    print(" output_file =", output_path)
    print()


def run_random_to_json(base_dir: Path) -> None:
    output_path = base_dir / "data" / "output_random_to_json.json"

    config = ChainConfig(
        reader=RandomReaderConfig(count=6, seed=42),
        writer=FileWriterConfig(path=str(output_path)),
        output_format=JsonFormatContext(indent=2),
        update_scores=UpdateScoresParams(delta=-3.0, only_active=False, deactivate_below=20.0),
        sort_records=SortRecordsParams(by="name", descending=False),
    )

    flow_service = DataFlowServiceFactory.create(config)
    result = flow_service.execute()

    print("Chain #2: random -> json")
    print(" read_count =", result.read_count)
    print(" written_count =", result.written_count)
    print(" steps =", ", ".join(result.steps))
    print(" output_file =", output_path)
    print()


def run_random_to_console_text() -> None:
    from config import ConsoleWriterConfig

    config = ChainConfig(
        reader=RandomReaderConfig(count=3, seed=7),
        writer=ConsoleWriterConfig(),
        output_format=TextFormatContext(include_index=True),
        update_scores=UpdateScoresParams(delta=2.5, only_active=True),
        sort_records=SortRecordsParams(by="id", descending=False),
    )

    flow_service = DataFlowServiceFactory.create(config)
    result = flow_service.execute()

    print("Chain #3: random -> text console")
    print(" read_count =", result.read_count)
    print(" written_count =", result.written_count)
    print(" steps =", ", ".join(result.steps))
    print()


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    run_file_to_csv(base_dir)
    run_random_to_json(base_dir)
    run_random_to_console_text()


if __name__ == "__main__":
    main()
