from __future__ import annotations

from typing import List

from dynamiclib import Entity, EntityPipeline, GLOBAL_KEY_REGISTRY, OperationContext
from dynamiclib.library_keys import ENTITY_NAME

HEALTH_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "game.health", int)
ARMOR_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "game.armor", int)
DAMAGE_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "game.damage", int)
XP_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "game.xp", int)
FACTION_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "game.faction", str)
ELITE_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "game.elite", bool)

XP_MULTIPLIER_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "ctx.xp_multiplier", float)
STOP_ON_DEAD_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "ctx.stop_on_dead", bool)
TRACE_KEY = GLOBAL_KEY_REGISTRY.register("consumer_a", "ctx.trace", list)


def create_warrior(
    entity_id: str,
    name: str,
    faction: str,
    health: int,
    armor: int,
    damage: int,
) -> Entity:
    entity = Entity(entity_id=entity_id, entity_type="warrior")
    entity.set(ENTITY_NAME, name)
    entity.set(FACTION_KEY, faction)
    entity.set(HEALTH_KEY, health)
    entity.set(ARMOR_KEY, armor)
    entity.set(DAMAGE_KEY, damage)
    entity.set(XP_KEY, 0)
    entity.set(ELITE_KEY, False)
    return entity


def create_operation_context(xp_multiplier: float, stop_on_dead: bool) -> OperationContext:
    context = OperationContext()
    context.items.set(XP_MULTIPLIER_KEY, xp_multiplier)
    context.items.set(STOP_ON_DEAD_KEY, stop_on_dead)
    context.items.set(TRACE_KEY, [])
    return context


def _append_trace(context: OperationContext, message: str) -> None:
    trace = context.items.get(TRACE_KEY, [])
    updated = list(trace)
    updated.append(message)
    context.items.set(TRACE_KEY, updated)


def apply_damage(entity: Entity, context: OperationContext) -> None:
    hp = entity.get(HEALTH_KEY, 0)
    armor = entity.get(ARMOR_KEY, 0)
    damage = entity.get(DAMAGE_KEY, 0)
    actual_damage = max(0, damage - armor)
    next_hp = max(0, hp - actual_damage)
    entity.set(HEALTH_KEY, next_hp)
    _append_trace(
        context,
        f"{entity.require(ENTITY_NAME)}: hp {hp}->{next_hp}, damage={damage}, armor={armor}",
    )


def grant_xp(entity: Entity, context: OperationContext) -> None:
    hp = entity.get(HEALTH_KEY, 0)
    if hp <= 0:
        _append_trace(context, f"{entity.require(ENTITY_NAME)}: dead, xp skipped")
        if context.items.get(STOP_ON_DEAD_KEY, False):
            context.is_done = True
        return

    current_xp = entity.get(XP_KEY, 0)
    multiplier = context.items.get(XP_MULTIPLIER_KEY, 1.0)
    gained = int(10 * multiplier)
    entity.set(XP_KEY, current_xp + gained)
    _append_trace(context, f"{entity.require(ENTITY_NAME)}: xp +{gained}")


def mark_elite(entity: Entity, context: OperationContext) -> None:
    xp = entity.get(XP_KEY, 0)
    is_elite = xp >= 15
    entity.set(ELITE_KEY, is_elite)
    _append_trace(context, f"{entity.require(ENTITY_NAME)}: elite={is_elite}")


def build_pipeline_for(entity: Entity) -> EntityPipeline:
    pipeline = EntityPipeline().add(apply_damage).add(grant_xp)

    faction = entity.get(FACTION_KEY, "")
    if faction == "Alliance":
        pipeline.add(mark_elite)
    return pipeline


def read_trace(context: OperationContext) -> List[str]:
    return context.items.require(TRACE_KEY)
