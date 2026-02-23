from .key_registry import GLOBAL_KEY_REGISTRY

ENTITY_NAME = GLOBAL_KEY_REGISTRY.register(
    owner="dynamiclib",
    name="entity.name",
    value_type=str,
)
