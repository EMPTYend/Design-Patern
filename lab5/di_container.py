from __future__ import annotations

from typing import Any, Callable, Dict

Factory = Callable[["ServiceProvider"], Any]


class ServiceCollection:
    def __init__(self) -> None:
        self._singleton_factories: Dict[str, Factory] = {}
        self._singletons: Dict[str, Any] = {}
        self._transient_factories: Dict[str, Factory] = {}

    def add_singleton(self, key: str, factory_or_instance: Factory | Any) -> None:
        if callable(factory_or_instance):
            self._singleton_factories[key] = factory_or_instance
        else:
            self._singletons[key] = factory_or_instance

    def add_transient(self, key: str, factory: Factory) -> None:
        self._transient_factories[key] = factory

    def build_provider(self) -> "ServiceProvider":
        return ServiceProvider(
            singleton_factories=dict(self._singleton_factories),
            singletons=dict(self._singletons),
            transient_factories=dict(self._transient_factories),
        )


class ServiceProvider:
    def __init__(
        self,
        singleton_factories: Dict[str, Factory],
        singletons: Dict[str, Any],
        transient_factories: Dict[str, Factory],
    ) -> None:
        self._singleton_factories = singleton_factories
        self._singletons = singletons
        self._transient_factories = transient_factories

    def get(self, key: str) -> Any:
        if key in self._singletons:
            return self._singletons[key]

        if key in self._singleton_factories:
            instance = self._singleton_factories[key](self)
            self._singletons[key] = instance
            return instance

        if key in self._transient_factories:
            return self._transient_factories[key](self)

        raise KeyError(f"Service not registered: {key}")
