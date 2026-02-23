from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List

from .dynamic_context import DynamicContext
from .entity import Entity

Operation = Callable[[Entity, "OperationContext"], None]


@dataclass
class OperationContext:
    items: DynamicContext = field(default_factory=DynamicContext)
    is_done: bool = False


class EntityPipeline:
    def __init__(self) -> None:
        self._operations: List[Operation] = []

    def add(self, operation: Operation) -> "EntityPipeline":
        self._operations.append(operation)
        return self

    def execute(self, entity: Entity, context: OperationContext) -> None:
        for operation in self._operations:
            if context.is_done:
                break
            operation(entity, context)

    def describe(self) -> List[str]:
        return [operation.__name__ for operation in self._operations]
