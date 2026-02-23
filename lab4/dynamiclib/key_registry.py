from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generic, Type, TypeVar, cast

T = TypeVar("T")


@dataclass(frozen=True)
class TypedKey(Generic[T]):
    id: int
    name: str
    value_type: Type[T]
    owner: str


class KeyConflictError(ValueError):
    pass


class KeyRegistry:
    def __init__(self) -> None:
        self._next_id = 1
        self._by_name: Dict[str, TypedKey[Any]] = {}

    def register(self, owner: str, name: str, value_type: Type[T]) -> TypedKey[T]:
        if not owner or not owner.strip():
            raise ValueError("owner cannot be empty")
        if not name or not name.strip():
            raise ValueError("name cannot be empty")

        existing = self._by_name.get(name)
        if existing is not None:
            if existing.value_type is not value_type:
                raise KeyConflictError(
                    f"Key '{name}' already registered with type "
                    f"{existing.value_type.__name__}, requested {value_type.__name__}"
                )
            return cast(TypedKey[T], existing)

        key: TypedKey[T] = TypedKey(
            id=self._next_id,
            name=name,
            value_type=value_type,
            owner=owner,
        )
        self._next_id += 1
        self._by_name[name] = key
        return key

    def all_keys(self) -> list[TypedKey[Any]]:
        return list(self._by_name.values())


GLOBAL_KEY_REGISTRY = KeyRegistry()
