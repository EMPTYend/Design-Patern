from __future__ import annotations

from typing import Sequence

from abstractions import RecordSerializer, SourceReader, SourceWriter, TransformationStep
from config import (
    ChainConfig,
    ConsoleWriterConfig,
    FileReaderConfig,
    FileWriterConfig,
    RandomReaderConfig,
)
from di_container import ServiceCollection
from readers import FileJsonSourceReader, RandomSourceReader
from serializers import TaggedUnionRecordSerializer
from services import DataFlowService, ReadService, SaveService, TransformationPipelineService
from transform_steps import SortRecordsStep, UpdateScoresStep
from writers import ConsoleSourceWriter, FileSourceWriter


def _build_reader(config: ChainConfig) -> SourceReader:
    if isinstance(config.reader, FileReaderConfig):
        return FileJsonSourceReader(path=config.reader.path)
    if isinstance(config.reader, RandomReaderConfig):
        return RandomSourceReader(count=config.reader.count, seed=config.reader.seed)
    raise TypeError(f"Unsupported reader config type: {type(config.reader).__name__}")


def _build_writer(config: ChainConfig, serializer: RecordSerializer) -> SourceWriter:
    if isinstance(config.writer, FileWriterConfig):
        return FileSourceWriter(path=config.writer.path, serializer=serializer)
    if isinstance(config.writer, ConsoleWriterConfig):
        return ConsoleSourceWriter(serializer=serializer)
    raise TypeError(f"Unsupported writer config type: {type(config.writer).__name__}")


def _build_transform_steps(config: ChainConfig) -> Sequence[TransformationStep]:
    return [
        UpdateScoresStep(config.update_scores),
        SortRecordsStep(config.sort_records),
    ]


class DataFlowServiceFactory:
    @staticmethod
    def create(config: ChainConfig) -> DataFlowService:
        services = ServiceCollection()

        services.add_singleton("config", config)
        services.add_singleton("serializer", lambda _: TaggedUnionRecordSerializer())
        services.add_singleton("reader", lambda _: _build_reader(config))
        services.add_singleton(
            "writer",
            lambda provider: _build_writer(
                config=config,
                serializer=provider.get("serializer"),
            ),
        )
        services.add_singleton("transform_steps", lambda _: _build_transform_steps(config))
        services.add_singleton("read_service", lambda provider: ReadService(provider.get("reader")))
        services.add_singleton(
            "transform_service",
            lambda provider: TransformationPipelineService(provider.get("transform_steps")),
        )
        services.add_singleton("save_service", lambda provider: SaveService(provider.get("writer")))
        services.add_singleton(
            "flow_service",
            lambda provider: DataFlowService(
                read_service=provider.get("read_service"),
                transform_service=provider.get("transform_service"),
                save_service=provider.get("save_service"),
                output_format=config.output_format,
            ),
        )

        provider = services.build_provider()
        return provider.get("flow_service")
