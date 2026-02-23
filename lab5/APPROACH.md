# Design Notes and Reasoning

## 1) Why this architecture

The assignment asks for abstraction dependencies and SRP.  
So the system is split into clear responsibilities:

- `SourceReader`: only reads.
- `TransformationStep` + pure functions: only transforms.
- `SourceWriter`: only writes.
- `RecordSerializer`: only converts to target format.
- `DataFlowService`: only orchestrates the chain.
- DI container/factory: only creates and wires dependencies.

This keeps each class focused and replaceable.

## 2) Dependency Inversion and IoC

High-level orchestration (`DataFlowService`) depends on interfaces:

- `SourceReader`
- `TransformationStep`
- `SourceWriter`

Concrete implementations are selected by config and instantiated through `DataFlowServiceFactory`, using a small DI container.

IoC is applied because service construction and dependency wiring are externalized from business logic.

## 3) Tagged Union for format

Format is represented as a tagged union:

- `JsonFormatContext`
- `CsvFormatContext`
- `TextFormatContext`

Serializer dispatches by concrete context type.  
This makes format-specific settings explicit and type-checked.

## 4) Data processing functions and parameter structs

Two static transformation functions are implemented over iterables:

- `update_scores(records, params)`
- `sort_records(records, params)`

Their dependencies are grouped into dedicated structs:

- `UpdateScoresParams`
- `SortRecordsParams`

Then adapter classes (`UpdateScoresStep`, `SortRecordsStep`) wrap these functions for pipeline/DI integration.

## 5) Why build a new container per chain

The assignment allows multiple DI approaches.  
This implementation uses the simplest and most explicit one:

- build a new container for each chain execution.

Benefits:

- no global mutable container state;
- each chain has isolated configuration;
- easy to understand and debug for a lab project.

## 6) Sources and formats coverage

At least two sources are implemented:

- file
- random generator

At least two formats are implemented:

- JSON
- CSV
- text (extra)

This satisfies the practical requirements and demonstrates extension points.

