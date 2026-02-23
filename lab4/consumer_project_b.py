from dynamiclib import GLOBAL_KEY_REGISTRY, KeyConflictError


def demonstrate_registry_conflict() -> str:
    shared_key = GLOBAL_KEY_REGISTRY.register("consumer_b", "game.health", int)
    try:
        GLOBAL_KEY_REGISTRY.register("consumer_b", "game.health", str)
    except KeyConflictError as exc:
        return (
            f"Shared key id={shared_key.id} reused safely. "
            f"Conflict blocked: {exc}"
        )
    return "No conflict detected (unexpected)"
