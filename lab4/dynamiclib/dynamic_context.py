from __future__ import annotations

from typing import Any, Dict, Optional, TypeVar, cast

from .key_registry import TypedKey

T = TypeVar("T")


class DynamicContext:
    def __init__(self) -> None:
        self._values: Dict[int, tuple[TypedKey[Any], Any]] = {}

    def set(self, key: TypedKey[T], value: T) -> None:
        if not isinstance(value, key.value_type):
            raise TypeError(
                f"Key '{key.name}' expects {key.value_type.__name__}, "
                f"got {type(value).__name__}"
            )
        self._values[key.id] = (cast(TypedKey[Any], key), value)

    def has(self, key: TypedKey[Any]) -> bool:
        return key.id in self._values

    def get(self, key: TypedKey[T], default: Optional[T] = None) -> Optional[T]:
        payload = self._values.get(key.id)
        if payload is None:
            return default
        _, raw = payload
        return cast(T, raw)

    def require(self, key: TypedKey[T]) -> T:
        payload = self._values.get(key.id)
        if payload is None:
            raise KeyError(f"Missing required key '{key.name}'")
        _, raw = payload
        return cast(T, raw)

    def remove(self, key: TypedKey[Any]) -> None:
        self._values.pop(key.id, None)

    def snapshot(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for typed_key, value in self._values.values():
            result[typed_key.name] = value
        return result
