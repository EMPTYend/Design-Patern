from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, TypeVar

from .dynamic_context import DynamicContext
from .key_registry import TypedKey

T = TypeVar("T")


@dataclass
class Entity:
    entity_id: str
    entity_type: str
    properties: DynamicContext = field(default_factory=DynamicContext)

    def set(self, key: TypedKey[T], value: T) -> None:
        self.properties.set(key, value)

    def get(self, key: TypedKey[T], default: Optional[T] = None) -> Optional[T]:
        return self.properties.get(key, default)

    def require(self, key: TypedKey[T]) -> T:
        return self.properties.require(key)

    def snapshot(self) -> Dict[str, Any]:
        data = self.properties.snapshot()
        data["__entity_id"] = self.entity_id
        data["__entity_type"] = self.entity_type
        return data
