from pprint import pprint

from consumer_project_a import (
    build_pipeline_for,
    create_operation_context,
    create_warrior,
    read_trace,
)
from consumer_project_b import demonstrate_registry_conflict
from dynamiclib import GLOBAL_KEY_REGISTRY


def main() -> None:
    warrior = create_warrior(
        entity_id="E-100",
        name="Arthas",
        faction="Alliance",
        health=120,
        armor=25,
        damage=40,
    )

    context = create_operation_context(xp_multiplier=1.5, stop_on_dead=True)
    pipeline = build_pipeline_for(warrior)

    print("Pipeline steps:", ", ".join(pipeline.describe()))
    pipeline.execute(warrior, context)

    print("\nFinal entity snapshot:")
    pprint(warrior.snapshot(), sort_dicts=True)

    print("\nOperation trace:")
    for line in read_trace(context):
        print("-", line)

    print("\nCross-project registry check:")
    print(demonstrate_registry_conflict())

    print("\nRegistered keys in global registry:")
    for key in GLOBAL_KEY_REGISTRY.all_keys():
        print(
            f"[{key.id}] {key.name} ({key.value_type.__name__})"
            f" owner={key.owner}"
        )


if __name__ == "__main__":
    main()
