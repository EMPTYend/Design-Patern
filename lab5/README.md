# Lab 5: Abstraction Dependencies

## Goal

This lab implements a data flow system that:

1. Reads data from multiple sources.
2. Applies transformations.
3. Writes data to another destination in another format.

The design follows SRP, IoC, DI, and dependency inversion ideas.

## Implemented Features

- Multiple readers (`SourceReader`):
  - `FileJsonSourceReader`
  - `RandomSourceReader`
  - `HttpJsonSourceReader` (extra)
- Multiple writers (`SourceWriter`):
  - `FileSourceWriter`
  - `ConsoleSourceWriter`
- Multiple output formats using tagged union:
  - `JsonFormatContext`
  - `CsvFormatContext`
  - `TextFormatContext`
- Full chain execution wrapped in a service:
  - `DataFlowService`
- DI container usage:
  - `ServiceCollection`
  - `ServiceProvider`
  - `DataFlowServiceFactory` builds a new container for each chain
- Data processing:
  - `update_scores(records, params)`
  - `sort_records(records, params)`
  - adapter steps for DI pipeline:
    - `UpdateScoresStep`
    - `SortRecordsStep`

## Folder Structure

- `models.py` - record model.
- `formats.py` - tagged union format contexts.
- `abstractions.py` - interfaces/abstractions.
- `readers.py` - source readers.
- `serializers.py` - format serializers.
- `writers.py` - output writers.
- `transform_params.py` - parameter structs for transformation functions.
- `transforms.py` - static transformation functions over iterables.
- `transform_steps.py` - adapters from functions to pipeline steps.
- `services.py` - orchestrator services and chain executor.
- `di_container.py` - simple DI container.
- `config.py` - chain configuration models.
- `factory.py` - factory building a service from config via DI.
- `main.py` - demo app with multiple chains.
- `APPROACH.md` - design notes and tradeoffs.

## How to Run

From repository root:

```powershell
python lab5/main.py
```

Or from `lab5` folder:

```powershell
python main.py
```

## Expected Output Files

After running demo chains:

- `lab5/data/output_file_to_csv.csv`
- `lab5/data/output_random_to_json.json`

And one chain prints text output to console.

