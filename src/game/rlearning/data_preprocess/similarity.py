from __future__ import annotations

import json
from pathlib import Path
import math
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple

# ============================================================
# Semantic taxonomies
# ============================================================
LIB_DIR = Path(__file__).resolve().parents[1] / "data/retrieval/libraries"
def _load_type_keys(name: str) -> list[str]:
    data = json.loads((LIB_DIR / f"{name}.json").read_text(encoding="utf-8"))
    return list(data["types"].keys())

def _load_n_value() -> dict[str, float]:
    data = json.loads((LIB_DIR / "amounts.json").read_text(encoding="utf-8"))
    return {
        k: float(v["value"])
        for k, v in data["types"].items()
        if k.startswith("N_") and "value" in v
    }

EFFECT_TYPES = _load_type_keys("effects")
TARGET_TYPES = _load_type_keys("targets")
TRIGGER_TYPES = _load_type_keys("triggers")
DURATION_TYPES = _load_type_keys("durations")
AMOUNT_TYPES = _load_type_keys("amounts")
STATIC_TYPES = _load_type_keys("statics")

N_VALUE = _load_n_value()


def _full_matrix(types: Sequence[str], default: float = 0.0) -> Dict[Tuple[str, str], float]:
    m = {(q, c): float(default) for q in types for c in types}
    for t in types:
        m[(t, t)] = 1.0
    return m


def _set(m: Dict[Tuple[str, str], float], q: str, c: str, score: float) -> None:
    m[(q, c)] = float(score)


def _sym(m: Dict[Tuple[str, str], float], a: str, b: str, score: float) -> None:
    _set(m, a, b, score)
    _set(m, b, a, score)


# ============================================================
# EFFECT similarity: 26 x 26 = 676 complete combinations
#
# Meaning:
#   EFFECT_SIM[(query_effect, candidate_effect)]
# measures how well candidate_effect satisfies query_effect.
# Unspecified semantic relations remain 0.0, but no key is missing.
# ============================================================

def build_effect_sim() -> Dict[Tuple[str, str], float]:
    m = _full_matrix(EFFECT_TYPES)

    # Damage family
    _set(m, "DEAL_DAMAGE", "DAMAGE_EACH", 0.45)
    _set(m, "DAMAGE_EACH", "DEAL_DAMAGE", 0.35)
    _set(m, "DEAL_DAMAGE", "STAT_EQUAL_DAMAGE", 0.55)
    _set(m, "STAT_EQUAL_DAMAGE", "DEAL_DAMAGE", 0.45)
    _sym(m, "DAMAGE_EACH", "STAT_EQUAL_DAMAGE", 0.35)
    _sym(m, "DEAL_DAMAGE", "PREVENT_DAMAGE", 0.10)
    _sym(m, "DAMAGE_EACH", "PREVENT_DAMAGE", 0.08)
    _sym(m, "STAT_EQUAL_DAMAGE", "PREVENT_DAMAGE", 0.08)
    _set(m, "LOSE_LIFE", "DEAL_DAMAGE", 0.55)
    _set(m, "DEAL_DAMAGE", "LOSE_LIFE", 0.45)
    _set(m, "LOSE_LIFE", "STAT_EQUAL_DAMAGE", 0.35)
    _set(m, "STAT_EQUAL_DAMAGE", "LOSE_LIFE", 0.30)

    # Life family
    _sym(m, "GAIN_LIFE", "LOSE_LIFE", 0.10)
    _set(m, "GAIN_LIFE", "DEAL_DAMAGE", 0.05)
    _set(m, "DEAL_DAMAGE", "GAIN_LIFE", 0.05)

    # Card-flow family
    _sym(m, "DRAW", "DISCARD", 0.20)
    _sym(m, "DRAW", "MILL", 0.25)
    _sym(m, "DRAW", "SCRY", 0.45)
    _sym(m, "DISCARD", "MILL", 0.25)
    _sym(m, "DISCARD", "SCRY", 0.10)
    _sym(m, "MILL", "SCRY", 0.30)
    _set(m, "DRAW", "SEARCH_TO_HAND", 0.55)
    _set(m, "SEARCH_TO_HAND", "DRAW", 0.40)
    _set(m, "DRAW", "SEARCH_LIBRARY", 0.30)
    _set(m, "SEARCH_LIBRARY", "DRAW", 0.20)
    _set(m, "SCRY", "SEARCH_LIBRARY", 0.25)
    _set(m, "SEARCH_LIBRARY", "SCRY", 0.20)
    _set(m, "MILL", "SEARCH_LIBRARY", 0.15)
    _set(m, "SEARCH_LIBRARY", "MILL", 0.10)

    # Counter / removal / bounce
    _sym(m, "DESTROY", "EXILE", 0.55)
    _sym(m, "DESTROY", "SACRIFICE", 0.45)
    _sym(m, "EXILE", "RETURN_HAND", 0.40)
    _sym(m, "DESTROY", "RETURN_HAND", 0.35)
    _sym(m, "EXILE", "SACRIFICE", 0.35)
    _sym(m, "RETURN_HAND", "SACRIFICE", 0.20)
    _set(m, "COUNTER_SPELL", "EXILE", 0.30)
    _set(m, "EXILE", "COUNTER_SPELL", 0.20)
    _set(m, "COUNTER_SPELL", "RETURN_HAND", 0.30)
    _set(m, "RETURN_HAND", "COUNTER_SPELL", 0.20)
    _set(m, "COUNTER_SPELL", "DESTROY", 0.10)
    _set(m, "DESTROY", "COUNTER_SPELL", 0.08)

    # Search / move-to-zone / reanimate / token
    # "search to hand" implies a library search, so candidate is more specific.
    _set(m, "SEARCH_LIBRARY", "SEARCH_TO_HAND", 0.90)
    _set(m, "SEARCH_TO_HAND", "SEARCH_LIBRARY", 0.65)

    # A search that directly places onto battlefield is related to both.
    _set(m, "SEARCH_LIBRARY", "PUT_BATTLEFIELD", 0.55)
    _set(m, "PUT_BATTLEFIELD", "SEARCH_LIBRARY", 0.40)

    # Reanimate is a specialized put-onto-battlefield operation from graveyard.
    _set(m, "PUT_BATTLEFIELD", "REANIMATE", 0.85)
    _set(m, "REANIMATE", "PUT_BATTLEFIELD", 0.55)

    # Token creation creates a battlefield object but not a card moved from a zone.
    _set(m, "PUT_BATTLEFIELD", "CREATE_TOKEN", 0.45)
    _set(m, "CREATE_TOKEN", "PUT_BATTLEFIELD", 0.35)
    _sym(m, "REANIMATE", "CREATE_TOKEN", 0.20)

    _set(m, "SEARCH_TO_HAND", "PUT_BATTLEFIELD", 0.35)
    _set(m, "PUT_BATTLEFIELD", "SEARCH_TO_HAND", 0.30)
    _set(m, "SEARCH_TO_HAND", "REANIMATE", 0.15)
    _set(m, "REANIMATE", "SEARCH_TO_HAND", 0.15)

    # Buff / counters / keyword grant
    _sym(m, "TEMP_BUFF", "PLUS1_COUNTER", 0.55)
    _sym(m, "TEMP_BUFF", "GRANT_KEYWORD", 0.35)
    _sym(m, "PLUS1_COUNTER", "GRANT_KEYWORD", 0.20)

    # Tap is not a removal effect, but can temporarily neutralize a creature.
    _set(m, "DESTROY", "TAP", 0.15)
    _set(m, "EXILE", "TAP", 0.15)
    _set(m, "RETURN_HAND", "TAP", 0.20)
    _set(m, "TAP", "DESTROY", 0.10)
    _set(m, "TAP", "EXILE", 0.10)
    _set(m, "TAP", "RETURN_HAND", 0.15)

    # Mana / library movement (known confusion in this pool)
    _sym(m, "ADD_MANA", "SEARCH_LIBRARY", 0.15)
    _set(m, "ADD_MANA", "PUT_BATTLEFIELD", 0.25)
    _set(m, "PUT_BATTLEFIELD", "ADD_MANA", 0.15)

    # Extra turn is intentionally isolated.
    return m


EFFECT_SIM = build_effect_sim()


def effect_similarity(query_effect: Optional[str], candidate_effect: Optional[str]) -> Optional[float]:
    if query_effect is None:
        return None
    if candidate_effect is None:
        return None
    if query_effect not in EFFECT_TYPES or candidate_effect not in EFFECT_TYPES:
        raise KeyError(f"unknown effect: query={query_effect!r}, candidate={candidate_effect!r}")
    return EFFECT_SIM[(query_effect, candidate_effect)]


# ============================================================
# TARGET similarity: 20 x 20 = 400 complete combinations
# Directional "satisfaction" relation.
# ============================================================

def build_target_sim() -> Dict[Tuple[str, str], float]:
    m = _full_matrix(TARGET_TYPES)

    # ---- CREATURE query ----
    _set(m, "CREATURE", "ANY", 1.00)
    _set(m, "CREATURE", "PERMANENT", 1.00)
    _set(m, "CREATURE", "NONLAND_PERMANENT", 1.00)
    _set(m, "CREATURE", "CREATURE_YOU_CONTROL", 0.75)
    _set(m, "CREATURE", "CREATURE_OPPONENT", 0.75)
    _set(m, "CREATURE", "RANDOM_CREATURE", 0.55)
    _set(m, "CREATURE", "CREATURES_YOU_CONTROL", 0.45)
    _set(m, "CREATURE", "EACH_CREATURE", 0.50)
    _set(m, "CREATURE", "ALL_CREATURES", 0.50)
    _set(m, "CREATURE", "GRAVEYARD_CREATURE", 0.25)
    _set(m, "CREATURE", "LIBRARY_CARD", 0.15)
    _set(m, "CREATURE", "SPELL", 0.15)
    _set(m, "CREATURE", "RANDOM_PERMANENT", 0.35)

    # ---- CREATURE_YOU_CONTROL query ----
    _set(m, "CREATURE_YOU_CONTROL", "CREATURE", 1.00)
    _set(m, "CREATURE_YOU_CONTROL", "ANY", 1.00)
    _set(m, "CREATURE_YOU_CONTROL", "PERMANENT", 1.00)
    _set(m, "CREATURE_YOU_CONTROL", "NONLAND_PERMANENT", 1.00)
    _set(m, "CREATURE_YOU_CONTROL", "CREATURE_OPPONENT", 0.10)
    _set(m, "CREATURE_YOU_CONTROL", "SELF", 0.65)
    _set(m, "CREATURE_YOU_CONTROL", "CREATURES_YOU_CONTROL", 0.80)
    _set(m, "CREATURE_YOU_CONTROL", "EACH_CREATURE", 0.55)
    _set(m, "CREATURE_YOU_CONTROL", "ALL_CREATURES", 0.55)
    _set(m, "CREATURE_YOU_CONTROL", "RANDOM_CREATURE", 0.35)
    _set(m, "CREATURE_YOU_CONTROL", "RANDOM_PERMANENT", 0.25)

    # ---- CREATURE_OPPONENT query ----
    _set(m, "CREATURE_OPPONENT", "CREATURE", 1.00)
    _set(m, "CREATURE_OPPONENT", "ANY", 1.00)
    _set(m, "CREATURE_OPPONENT", "PERMANENT", 1.00)
    _set(m, "CREATURE_OPPONENT", "NONLAND_PERMANENT", 1.00)
    _set(m, "CREATURE_OPPONENT", "CREATURE_YOU_CONTROL", 0.10)
    _set(m, "CREATURE_OPPONENT", "RANDOM_CREATURE", 0.65)
    _set(m, "CREATURE_OPPONENT", "EACH_CREATURE", 0.55)
    _set(m, "CREATURE_OPPONENT", "ALL_CREATURES", 0.55)
    _set(m, "CREATURE_OPPONENT", "RANDOM_PERMANENT", 0.40)

    # ---- CREATURES_YOU_CONTROL query ----
    _set(m, "CREATURES_YOU_CONTROL", "CREATURE_YOU_CONTROL", 0.45)
    _set(m, "CREATURES_YOU_CONTROL", "CREATURE", 0.35)
    _set(m, "CREATURES_YOU_CONTROL", "ANY", 0.25)
    _set(m, "CREATURES_YOU_CONTROL", "EACH_CREATURE", 0.65)
    _set(m, "CREATURES_YOU_CONTROL", "ALL_CREATURES", 0.65)

    # ---- ANY query ----
    _set(m, "ANY", "CREATURE", 0.65)
    _set(m, "ANY", "PLAYER", 0.65)
    _set(m, "ANY", "OPPONENT", 0.50)
    _set(m, "ANY", "CREATURE_YOU_CONTROL", 0.45)
    _set(m, "ANY", "CREATURE_OPPONENT", 0.45)
    _set(m, "ANY", "PERMANENT", 0.45)
    _set(m, "ANY", "NONLAND_PERMANENT", 0.50)
    _set(m, "ANY", "RANDOM_CREATURE", 0.30)
    _set(m, "ANY", "RANDOM_PERMANENT", 0.25)
    _set(m, "ANY", "YOU", 0.45)

    # ---- PLAYER query ----
    _set(m, "PLAYER", "ANY", 1.00)
    _set(m, "PLAYER", "OPPONENT", 0.75)
    _set(m, "PLAYER", "YOU", 0.65)
    _set(m, "PLAYER", "EACH_OPPONENT", 0.55)

    # ---- OPPONENT query ----
    _set(m, "OPPONENT", "PLAYER", 1.00)
    _set(m, "OPPONENT", "ANY", 1.00)
    _set(m, "OPPONENT", "EACH_OPPONENT", 0.85)
    _set(m, "OPPONENT", "YOU", 0.00)

    # ---- EACH_OPPONENT query ----
    _set(m, "EACH_OPPONENT", "OPPONENT", 0.55)
    _set(m, "EACH_OPPONENT", "PLAYER", 0.40)
    _set(m, "EACH_OPPONENT", "ANY", 0.35)
    _set(m, "EACH_OPPONENT", "YOU", 0.00)

    # ---- EACH_CREATURE query ----
    _set(m, "EACH_CREATURE", "ALL_CREATURES", 0.90)
    _set(m, "EACH_CREATURE", "CREATURES_YOU_CONTROL", 0.55)
    _set(m, "EACH_CREATURE", "CREATURE", 0.35)
    _set(m, "EACH_CREATURE", "ANY", 0.20)

    # ---- ALL_CREATURES query ----
    _set(m, "ALL_CREATURES", "EACH_CREATURE", 0.90)
    _set(m, "ALL_CREATURES", "CREATURES_YOU_CONTROL", 0.55)
    _set(m, "ALL_CREATURES", "CREATURE", 0.35)
    _set(m, "ALL_CREATURES", "ANY", 0.20)

    # ---- SELF query ----
    _set(m, "SELF", "PERMANENT", 0.80)
    _set(m, "SELF", "NONLAND_PERMANENT", 0.75)
    _set(m, "SELF", "CREATURE_YOU_CONTROL", 0.60)
    _set(m, "SELF", "CREATURE", 0.55)
    _set(m, "SELF", "ANY", 0.50)
    _set(m, "SELF", "YOU", 0.15)

    # ---- YOU query ----
    _set(m, "YOU", "PLAYER", 1.00)
    _set(m, "YOU", "ANY", 1.00)
    _set(m, "YOU", "SELF", 0.15)
    _set(m, "YOU", "OPPONENT", 0.00)
    _set(m, "YOU", "EACH_OPPONENT", 0.00)

    # ---- PERMANENT query ----
    _set(m, "PERMANENT", "NONLAND_PERMANENT", 0.85)
    _set(m, "PERMANENT", "CREATURE", 0.65)
    _set(m, "PERMANENT", "CREATURE_YOU_CONTROL", 0.50)
    _set(m, "PERMANENT", "CREATURE_OPPONENT", 0.50)
    _set(m, "PERMANENT", "ARTIFACT_OR_ENCHANTMENT", 0.60)
    _set(m, "PERMANENT", "RANDOM_PERMANENT", 0.55)
    _set(m, "PERMANENT", "RANDOM_CREATURE", 0.35)
    _set(m, "PERMANENT", "ANY", 0.45)
    _set(m, "PERMANENT", "SELF", 0.40)
    _set(m, "PERMANENT", "SPELL", 0.05)

    # ---- NONLAND_PERMANENT query ----
    _set(m, "NONLAND_PERMANENT", "PERMANENT", 1.00)
    _set(m, "NONLAND_PERMANENT", "CREATURE", 0.70)
    _set(m, "NONLAND_PERMANENT", "CREATURE_YOU_CONTROL", 0.55)
    _set(m, "NONLAND_PERMANENT", "CREATURE_OPPONENT", 0.55)
    _set(m, "NONLAND_PERMANENT", "ARTIFACT_OR_ENCHANTMENT", 0.75)
    _set(m, "NONLAND_PERMANENT", "RANDOM_PERMANENT", 0.50)
    _set(m, "NONLAND_PERMANENT", "ANY", 0.60)
    _set(m, "NONLAND_PERMANENT", "SELF", 0.35)
    _set(m, "NONLAND_PERMANENT", "SPELL", 0.05)

    # ---- SPELL query ----
    _set(m, "SPELL", "CREATURE", 0.15)
    _set(m, "SPELL", "PERMANENT", 0.05)
    _set(m, "SPELL", "NONLAND_PERMANENT", 0.05)
    _set(m, "SPELL", "ANY", 0.05)

    # ---- ARTIFACT_OR_ENCHANTMENT query ----
    _set(m, "ARTIFACT_OR_ENCHANTMENT", "PERMANENT", 1.00)
    _set(m, "ARTIFACT_OR_ENCHANTMENT", "NONLAND_PERMANENT", 1.00)
    _set(m, "ARTIFACT_OR_ENCHANTMENT", "RANDOM_PERMANENT", 0.45)

    # ---- RANDOM_CREATURE query ----
    _set(m, "RANDOM_CREATURE", "CREATURE", 0.55)
    _set(m, "RANDOM_CREATURE", "CREATURE_OPPONENT", 0.50)
    _set(m, "RANDOM_CREATURE", "RANDOM_PERMANENT", 0.75)
    _set(m, "RANDOM_CREATURE", "PERMANENT", 0.35)
    _set(m, "RANDOM_CREATURE", "ANY", 0.30)

    # ---- RANDOM_PERMANENT query ----
    _set(m, "RANDOM_PERMANENT", "RANDOM_CREATURE", 0.70)
    _set(m, "RANDOM_PERMANENT", "PERMANENT", 0.55)
    _set(m, "RANDOM_PERMANENT", "NONLAND_PERMANENT", 0.50)
    _set(m, "RANDOM_PERMANENT", "CREATURE", 0.30)
    _set(m, "RANDOM_PERMANENT", "ANY", 0.20)

    # ---- GRAVEYARD_CREATURE query ----
    _set(m, "GRAVEYARD_CREATURE", "CREATURE", 0.25)
    _set(m, "GRAVEYARD_CREATURE", "CREATURE_YOU_CONTROL", 0.15)
    _set(m, "GRAVEYARD_CREATURE", "LIBRARY_CARD", 0.20)

    # ---- LIBRARY_CARD query ----
    _set(m, "LIBRARY_CARD", "GRAVEYARD_CREATURE", 0.20)
    _set(m, "LIBRARY_CARD", "CREATURE", 0.15)

    return m


TARGET_SIM = build_target_sim()


def target_similarity(query_target: Optional[str], candidate_target: Optional[str]) -> Optional[float]:
    if query_target is None:
        return None
    if candidate_target is None:
        return None
    if query_target not in TARGET_TYPES or candidate_target not in TARGET_TYPES:
        raise KeyError(f"unknown target: query={query_target!r}, candidate={candidate_target!r}")
    return TARGET_SIM[(query_target, candidate_target)]


# ============================================================
# TRIGGER similarity: 20 x 20 = 400 complete combinations
# Directional where one trigger is a semantic superset/subset.
# ============================================================

def build_trigger_sim() -> Dict[Tuple[str, str], float]:
    m = _full_matrix(TRIGGER_TYPES)

    # ETB family
    _set(m, "ETB", "ETB_OR_ATTACK", 0.95)   # candidate also triggers on ETB
    _set(m, "ETB_OR_ATTACK", "ETB", 0.65)   # misses attack half
    _set(m, "ATTACK", "ETB_OR_ATTACK", 0.95)
    _set(m, "ETB_OR_ATTACK", "ATTACK", 0.65)

    _set(m, "ETB", "LAND_ENTERS", 0.55)
    _set(m, "LAND_ENTERS", "ETB", 0.35)
    _set(m, "ETB", "CONSTELLATION", 0.45)
    _set(m, "CONSTELLATION", "ETB", 0.35)
    _set(m, "ETB", "CAST_CREATURE_SPELL", 0.25)
    _set(m, "CAST_CREATURE_SPELL", "ETB", 0.25)
    _set(m, "ETB", "CAST_INSTANT_SORCERY", 0.08)
    _set(m, "CAST_INSTANT_SORCERY", "ETB", 0.08)

    # Attack / combat family
    _sym(m, "ATTACK", "DEFEND", 0.15)
    _set(m, "ATTACK", "DEALS_DAMAGE", 0.35)
    _set(m, "DEALS_DAMAGE", "ATTACK", 0.45)
    _sym(m, "ATTACK", "SELF_DEALT_DAMAGE", 0.10)
    _sym(m, "DEFEND", "SELF_DEALT_DAMAGE", 0.25)
    _sym(m, "DEFEND", "DEALS_DAMAGE", 0.15)
    _sym(m, "SELF_DEALT_DAMAGE", "DEALS_DAMAGE", 0.15)

    # Dies family
    # "any creature dies" can include self; reverse is narrower.
    _set(m, "DIES", "CREATURE_DIES", 0.90)
    _set(m, "CREATURE_DIES", "DIES", 0.55)

    # Phase/timing family
    _sym(m, "UPKEEP", "END_STEP", 0.20)
    _sym(m, "UPKEEP", "MAIN_PHASE", 0.20)
    _sym(m, "END_STEP", "MAIN_PHASE", 0.35)

    # Cast family: CAST_SPELL is broadest.
    _set(m, "CAST_INSTANT_SORCERY", "CAST_SPELL", 1.00)
    _set(m, "CAST_CREATURE_SPELL", "CAST_SPELL", 1.00)
    _set(m, "CAST_COLORED_SPELL", "CAST_SPELL", 1.00)

    _set(m, "CAST_SPELL", "CAST_INSTANT_SORCERY", 0.65)
    _set(m, "CAST_SPELL", "CAST_CREATURE_SPELL", 0.65)
    _set(m, "CAST_SPELL", "CAST_COLORED_SPELL", 0.65)

    _sym(m, "CAST_INSTANT_SORCERY", "CAST_CREATURE_SPELL", 0.20)
    _sym(m, "CAST_INSTANT_SORCERY", "CAST_COLORED_SPELL", 0.45)
    _sym(m, "CAST_CREATURE_SPELL", "CAST_COLORED_SPELL", 0.35)

    _set(m, "OPPONENT_PROLIFERATES", "CAST_SPELL", 0.05)
    _set(m, "CAST_SPELL", "OPPONENT_PROLIFERATES", 0.05)

    # Land family
    _sym(m, "LAND_ENTERS", "LAND_MANA", 0.30)
    _sym(m, "LAND_ENTERS", "LAND_ACTIVATED", 0.25)
    _sym(m, "LAND_MANA", "LAND_ACTIVATED", 0.60)
    _set(m, "LAND_MANA", "ETB", 0.08)
    _set(m, "ETB", "LAND_MANA", 0.08)
    _set(m, "LAND_ACTIVATED", "ETB", 0.05)
    _set(m, "ETB", "LAND_ACTIVATED", 0.05)

    return m


TRIGGER_SIM = build_trigger_sim()


def trigger_similarity(query_trigger: Optional[str], candidate_trigger: Optional[str]) -> Optional[float]:
    if query_trigger is None:
        return None
    if candidate_trigger is None:
        return None
    if query_trigger not in TRIGGER_TYPES or candidate_trigger not in TRIGGER_TYPES:
        raise KeyError(f"unknown trigger: query={query_trigger!r}, candidate={candidate_trigger!r}")
    return TRIGGER_SIM[(query_trigger, candidate_trigger)]


# ============================================================
# DURATION similarity: 10 x 10 = 100 complete combinations
# ============================================================

def build_duration_sim() -> Dict[Tuple[str, str], float]:
    m = _full_matrix(DURATION_TYPES)

    # Current-turn family
    _sym(m, "UNTIL_EOT", "THIS_TURN", 0.90)
    _sym(m, "UNTIL_EOT", "INSTANT", 0.30)
    _sym(m, "THIS_TURN", "INSTANT", 0.40)

    # Delayed timing
    _sym(m, "NEXT_END_STEP", "NEXT_MAIN_PHASE", 0.35)
    _sym(m, "NEXT_END_STEP", "DONT_UNTAP_NEXT", 0.35)
    _sym(m, "NEXT_MAIN_PHASE", "DONT_UNTAP_NEXT", 0.20)

    _set(m, "UNTIL_EOT", "NEXT_END_STEP", 0.45)
    _set(m, "NEXT_END_STEP", "UNTIL_EOT", 0.45)

    _set(m, "UNTIL_EOT", "DONT_UNTAP_NEXT", 0.20)
    _set(m, "DONT_UNTAP_NEXT", "UNTIL_EOT", 0.20)

    _set(m, "THIS_TURN", "NEXT_END_STEP", 0.25)
    _set(m, "NEXT_END_STEP", "THIS_TURN", 0.25)

    # Conditional persistence
    _sym(m, "AS_LONG_AS_CONTROL", "UNTIL_LEAVES", 0.80)
    _set(m, "AS_LONG_AS_CONTROL", "PERMANENT", 0.55)
    _set(m, "PERMANENT", "AS_LONG_AS_CONTROL", 0.45)
    _set(m, "UNTIL_LEAVES", "PERMANENT", 0.55)
    _set(m, "PERMANENT", "UNTIL_LEAVES", 0.45)

    # Permanent vs temporary
    _sym(m, "PERMANENT", "UNTIL_EOT", 0.15)
    _sym(m, "PERMANENT", "THIS_TURN", 0.12)
    _sym(m, "PERMANENT", "INSTANT", 0.05)

    # Extra turn
    _sym(m, "EXTRA_TURN", "THIS_TURN", 0.20)
    _sym(m, "EXTRA_TURN", "NEXT_MAIN_PHASE", 0.20)
    _sym(m, "EXTRA_TURN", "NEXT_END_STEP", 0.15)
    _sym(m, "EXTRA_TURN", "UNTIL_EOT", 0.15)

    return m


DURATION_SIM = build_duration_sim()


def duration_similarity(query_duration: Optional[str], candidate_duration: Optional[str]) -> Optional[float]:
    if query_duration is None:
        return None
    if candidate_duration is None:
        return None
    if query_duration not in DURATION_TYPES or candidate_duration not in DURATION_TYPES:
        raise KeyError(f"unknown duration: query={query_duration!r}, candidate={candidate_duration!r}")
    return DURATION_SIM[(query_duration, candidate_duration)]


# ============================================================
# STATIC / KEYWORD similarity: 20 x 20 = 400 combinations
# ============================================================

def build_static_sim() -> Dict[Tuple[str, str], float]:
    m = _full_matrix(STATIC_TYPES)

    # File-defined confusable pairs
    _sym(m, "FLYING", "REACH", 0.30)

    # Shroud is broader targeting protection but also blocks your own targeting.
    _set(m, "HEXPROOF", "SHROUD", 0.80)
    _set(m, "SHROUD", "HEXPROOF", 0.65)

    # Double strike includes a first-strike damage step.
    _set(m, "FIRST_STRIKE", "DOUBLE_STRIKE", 0.95)
    _set(m, "DOUBLE_STRIKE", "FIRST_STRIKE", 0.65)

    _sym(m, "TRAMPLE", "MENACE", 0.25)
    _sym(m, "HASTE", "VIGILANCE", 0.15)

    # Additional functional relations.
    _sym(m, "HEXPROOF", "WARD", 0.55)
    _sym(m, "SHROUD", "WARD", 0.45)

    # Evasion family
    _set(m, "UNBLOCKABLE", "FLYING", 0.45)
    _set(m, "FLYING", "UNBLOCKABLE", 0.55)
    _sym(m, "UNBLOCKABLE", "MENACE", 0.40)
    _sym(m, "UNBLOCKABLE", "TRAMPLE", 0.30)
    _sym(m, "FLYING", "MENACE", 0.20)
    _sym(m, "FLYING", "TRAMPLE", 0.15)

    # Defender semantically entails cannot attack.
    _set(m, "CANNOT_ATTACK", "DEFENDER", 0.95)
    _set(m, "DEFENDER", "CANNOT_ATTACK", 0.90)

    # Combat keyword proximity.
    _sym(m, "DEATHTOUCH", "FIRST_STRIKE", 0.15)
    _sym(m, "DEATHTOUCH", "DOUBLE_STRIKE", 0.15)
    _sym(m, "LIFELINK", "DEATHTOUCH", 0.10)
    _sym(m, "LIFELINK", "DOUBLE_STRIKE", 0.10)
    _sym(m, "HASTE", "FLASH", 0.25)

    # Protection / durability
    _sym(m, "INDESTRUCTIBLE", "HEXPROOF", 0.25)
    _sym(m, "INDESTRUCTIBLE", "SHROUD", 0.20)
    _sym(m, "INDESTRUCTIBLE", "WARD", 0.20)

    # Spell-oriented mechanics
    _sym(m, "PROWESS", "FLASH", 0.10)

    # Infect is its own damage-modification mechanic.
    _sym(m, "INFECT", "DEATHTOUCH", 0.15)
    _sym(m, "INFECT", "LIFELINK", 0.05)

    return m


STATIC_SIM = build_static_sim()


def static_similarity(query_static: Optional[str], candidate_static: Optional[str]) -> Optional[float]:
    if query_static is None:
        return None
    if candidate_static is None:
        return None
    if query_static not in STATIC_TYPES or candidate_static not in STATIC_TYPES:
        raise KeyError(f"unknown static: query={query_static!r}, candidate={candidate_static!r}")
    return STATIC_SIM[(query_static, candidate_static)]


def static_set_similarity(query_statics: Sequence[str], candidate_statics: Sequence[str]) -> Optional[float]:
    """
    Query-side coverage:
    for every requested static keyword, take its best match in candidate statics,
    then average. Extra candidate statics do not hurt.
    """
    if not query_statics:
        return None
    if not candidate_statics:
        return None
    vals = []
    for q in query_statics:
        vals.append(max(static_similarity(q, c) or 0.0 for c in candidate_statics))
    return sum(vals) / len(vals)


# ============================================================
# AMOUNT type similarity: 15 x 15 = 225 complete combinations
# Plus numeric / P-T continuous comparison when values are available.
# ============================================================

def build_amount_type_sim() -> Dict[Tuple[str, str], float]:
    m = _full_matrix(AMOUNT_TYPES)

    fixed = ["N_1", "N_2", "N_3", "N_4", "N_5"]

    # Generic FIXED can represent any concrete integer.
    for n in fixed:
        _set(m, n, "FIXED", 0.90)
        _set(m, "FIXED", n, 0.90)

    # Fixed amounts vs counter count: numeric relation exists, semantics differ.
    for n in fixed:
        _set(m, n, "COUNTERS_N", 0.45)
        _set(m, "COUNTERS_N", n, 0.45)

    # Fixed vs P/T pair: may share a number, but different quantity shape.
    for n in fixed:
        _set(m, n, "BUFF_PT", 0.35)
        _set(m, "BUFF_PT", n, 0.35)

    # Fixed/scaled/variable relations
    for n in fixed:
        _set(m, n, "VARIABLE_X", 0.25)
        _set(m, "VARIABLE_X", n, 0.25)
        _set(m, n, "EQUAL_POWER", 0.20)
        _set(m, "EQUAL_POWER", n, 0.20)
        _set(m, n, "EQUAL_TOUGHNESS", 0.20)
        _set(m, "EQUAL_TOUGHNESS", n, 0.20)
        _set(m, n, "EQUAL_LIFE", 0.15)
        _set(m, "EQUAL_LIFE", n, 0.15)
        _set(m, n, "EQUAL_COUNT", 0.20)
        _set(m, "EQUAL_COUNT", n, 0.20)
        _set(m, n, "DIVIDED", 0.35)
        _set(m, "DIVIDED", n, 0.35)
        _set(m, n, "THAT_MUCH", 0.20)
        _set(m, "THAT_MUCH", n, 0.20)

    _sym(m, "FIXED", "COUNTERS_N", 0.50)
    _sym(m, "FIXED", "BUFF_PT", 0.40)
    _sym(m, "FIXED", "VARIABLE_X", 0.30)
    _sym(m, "FIXED", "EQUAL_POWER", 0.25)
    _sym(m, "FIXED", "EQUAL_TOUGHNESS", 0.25)
    _sym(m, "FIXED", "EQUAL_LIFE", 0.20)
    _sym(m, "FIXED", "EQUAL_COUNT", 0.30)
    _sym(m, "FIXED", "DIVIDED", 0.45)
    _sym(m, "FIXED", "THAT_MUCH", 0.30)

    _sym(m, "BUFF_PT", "COUNTERS_N", 0.55)
    _sym(m, "BUFF_PT", "EQUAL_POWER", 0.20)
    _sym(m, "BUFF_PT", "EQUAL_TOUGHNESS", 0.20)
    _sym(m, "BUFF_PT", "VARIABLE_X", 0.20)

    # Scaled/reference family
    _sym(m, "EQUAL_POWER", "EQUAL_TOUGHNESS", 0.55)
    _sym(m, "EQUAL_POWER", "EQUAL_LIFE", 0.30)
    _sym(m, "EQUAL_POWER", "EQUAL_COUNT", 0.35)
    _sym(m, "EQUAL_POWER", "VARIABLE_X", 0.40)
    _sym(m, "EQUAL_POWER", "THAT_MUCH", 0.45)
    _sym(m, "EQUAL_POWER", "DIVIDED", 0.15)

    _sym(m, "EQUAL_TOUGHNESS", "EQUAL_LIFE", 0.30)
    _sym(m, "EQUAL_TOUGHNESS", "EQUAL_COUNT", 0.35)
    _sym(m, "EQUAL_TOUGHNESS", "VARIABLE_X", 0.40)
    _sym(m, "EQUAL_TOUGHNESS", "THAT_MUCH", 0.45)
    _sym(m, "EQUAL_TOUGHNESS", "DIVIDED", 0.15)

    _sym(m, "EQUAL_LIFE", "EQUAL_COUNT", 0.35)
    _sym(m, "EQUAL_LIFE", "VARIABLE_X", 0.35)
    _sym(m, "EQUAL_LIFE", "THAT_MUCH", 0.55)
    _sym(m, "EQUAL_LIFE", "DIVIDED", 0.15)

    _sym(m, "EQUAL_COUNT", "VARIABLE_X", 0.60)
    _sym(m, "EQUAL_COUNT", "THAT_MUCH", 0.45)
    _sym(m, "EQUAL_COUNT", "DIVIDED", 0.20)

    _sym(m, "VARIABLE_X", "THAT_MUCH", 0.35)
    _sym(m, "VARIABLE_X", "DIVIDED", 0.25)

    _sym(m, "DIVIDED", "THAT_MUCH", 0.35)

    return m


AMOUNT_TYPE_SIM = build_amount_type_sim()


def _coerce_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _amount_numeric_value(amount_type: Optional[str], obj: Mapping[str, Any]) -> Optional[float]:
    val = _coerce_number(obj.get("amount_value"))
    if val is not None:
        return val
    if amount_type in N_VALUE:
        return N_VALUE[amount_type]
    # Generic templates may store n explicitly.
    val = _coerce_number(obj.get("n"))
    if val is not None:
        return val
    return None


def numeric_similarity(q: float, c: float, alpha: float = 0.35) -> float:
    return math.exp(-alpha * abs(float(q) - float(c)))


def pt_similarity(
    q_p: float, q_t: float, c_p: float, c_t: float, alpha: float = 0.35
) -> float:
    # Average L1 distance over power/toughness dimensions.
    d = (abs(q_p - c_p) + abs(q_t - c_t)) / 2.0
    return math.exp(-alpha * d)


def amount_similarity(
    query: Mapping[str, Any],
    candidate: Mapping[str, Any],
    alpha: float = 0.35,
) -> Optional[float]:
    """
    Expects dicts/bindings containing:
      amount: one of AMOUNT_TYPES
      amount_value: optional concrete number
      n: optional concrete number for FIXED/COUNTERS_N
      p/t: optional P/T components for BUFF_PT

    Logic:
      1) If both are BUFF_PT and p/t are known -> continuous P/T similarity.
      2) If both have concrete numeric values -> continuous numeric similarity.
      3) Otherwise use complete AMOUNT_TYPE_SIM matrix.
    """
    q_type = query.get("amount")
    c_type = candidate.get("amount")

    if q_type is None:
        return None
    if c_type is None:
        return None

    if q_type not in AMOUNT_TYPES or c_type not in AMOUNT_TYPES:
        raise KeyError(f"unknown amount type: query={q_type!r}, candidate={c_type!r}")

    if q_type == "BUFF_PT" and c_type == "BUFF_PT":
        qp = _coerce_number(query.get("p"))
        qt = _coerce_number(query.get("t"))
        cp = _coerce_number(candidate.get("p"))
        ct = _coerce_number(candidate.get("t"))
        if None not in (qp, qt, cp, ct):
            return pt_similarity(qp, qt, cp, ct, alpha=alpha)

    q_num = _amount_numeric_value(q_type, query)
    c_num = _amount_numeric_value(c_type, candidate)

    if q_num is not None and c_num is not None:
        # If both quantities are concrete, exact/near amount distance is the
        # most useful signal; effect similarity separately captures whether
        # "3 damage", "3 counters", etc. are the same mechanic.
        return numeric_similarity(q_num, c_num, alpha=alpha)

    return AMOUNT_TYPE_SIM[(q_type, c_type)]


# ============================================================
# Aggregate relevance
# ============================================================

SLOT_WEIGHTS = {
    "effect": 0.40,
    "target": 0.18,
    "amount": 0.14,
    "trigger": 0.16,
    "duration": 0.08,
    "keyword": 0.12,
    "static": 0.12,
}


def compute_binding_relevance(
    query_spec: Mapping[str, Any],
    candidate_binding: Mapping[str, Any],
    *,
    candidate_statics: Optional[Sequence[str]] = None,
    missing_policy: str = "unknown",
) -> Optional[float]:
    """
    Continuous relevance in [0, 1].

    missing_policy:
      "unknown" -> if query requires a slot but candidate binding lacks it,
                   return None rather than inventing a negative label.
      "zero"    -> missing required candidate slot contributes 0.0.
    """
    if missing_policy not in {"unknown", "zero"}:
        raise ValueError("missing_policy must be 'unknown' or 'zero'")

    parts: Dict[str, float] = {}

    def add_part(name: str, value: Optional[float]) -> bool:
        if value is None:
            if missing_policy == "unknown":
                return False
            parts[name] = 0.0
        else:
            parts[name] = float(value)
        return True

    if "effect" in query_spec:
        if not add_part(
            "effect",
            effect_similarity(query_spec.get("effect"), candidate_binding.get("effect")),
        ):
            return None

    if "target" in query_spec:
        if not add_part(
            "target",
            target_similarity(query_spec.get("target"), candidate_binding.get("target")),
        ):
            return None

    if "amount" in query_spec:
        if not add_part("amount", amount_similarity(query_spec, candidate_binding)):
            return None

    if "trigger" in query_spec:
        if not add_part(
            "trigger",
            trigger_similarity(query_spec.get("trigger"), candidate_binding.get("trigger")),
        ):
            return None

    if "duration" in query_spec:
        if not add_part(
            "duration",
            duration_similarity(query_spec.get("duration"), candidate_binding.get("duration")),
        ):
            return None

    # Recommended schema for GRANT_KEYWORD:
    # candidate_binding["keyword"] = "HEXPROOF" / ...
    if "keyword" in query_spec:
        if not add_part(
            "keyword",
            static_similarity(query_spec.get("keyword"), candidate_binding.get("keyword")),
        ):
            return None

    # STATIC_PLUS query can compare against card-level statics.
    if "static" in query_spec:
        q_static = query_spec.get("static")
        if q_static is None:
            return None
        if not candidate_statics:
            if missing_policy == "unknown":
                return None
            parts["static"] = 0.0
        else:
            parts["static"] = max(
                static_similarity(q_static, c) or 0.0 for c in candidate_statics
            )

    if not parts:
        return None

    total_weight = sum(SLOT_WEIGHTS[k] for k in parts)
    base = sum(SLOT_WEIGHTS[k] * v for k, v in parts.items()) / total_weight

    # Core-mechanic gates stop matching numbers/targets from rescuing
    # a candidate whose action or trigger is fundamentally wrong.
    if "effect" in parts:
        base *= 0.15 + 0.85 * parts["effect"]

    if "trigger" in parts:
        base *= 0.35 + 0.65 * parts["trigger"]

    return max(0.0, min(1.0, base))


def card_relevance(
    query_spec: Mapping[str, Any],
    card: Mapping[str, Any],
    *,
    missing_policy: str = "unknown",
) -> Optional[float]:
    """
    Single-binding query: card relevance is the best matching binding.
    For static-only queries, a synthetic empty binding is sufficient.
    MULTI_BINDING queries should use a separate assignment/matching routine.
    """
    bindings = list(card.get("bindings") or [])
    statics = list(card.get("statics") or [])

    if not bindings:
        bindings = [{}]

    scores = []
    for b in bindings:
        s = compute_binding_relevance(
            query_spec,
            b,
            candidate_statics=statics,
            missing_policy=missing_policy,
        )
        if s is not None:
            scores.append(s)

    if not scores:
        return None
    return max(scores)


# ============================================================
# Validation helpers
# ============================================================

def validate_matrices() -> Dict[str, int]:
    expected = {
        "effect": len(EFFECT_TYPES) ** 2,
        "target": len(TARGET_TYPES) ** 2,
        "trigger": len(TRIGGER_TYPES) ** 2,
        "duration": len(DURATION_TYPES) ** 2,
        "amount_type": len(AMOUNT_TYPES) ** 2,
        "static": len(STATIC_TYPES) ** 2,
    }
    actual = {
        "effect": len(EFFECT_SIM),
        "target": len(TARGET_SIM),
        "trigger": len(TRIGGER_SIM),
        "duration": len(DURATION_SIM),
        "amount_type": len(AMOUNT_TYPE_SIM),
        "static": len(STATIC_SIM),
    }
    assert actual == expected, (actual, expected)

    for matrix in [EFFECT_SIM, TARGET_SIM, TRIGGER_SIM, DURATION_SIM, AMOUNT_TYPE_SIM, STATIC_SIM]:
        assert all(0.0 <= v <= 1.0 for v in matrix.values())

    return actual


if __name__ == "__main__":
    print(validate_matrices())

    q = {
        "effect": "DEAL_DAMAGE",
        "target": "ANY",
        "amount": "N_3",
        "amount_value": 3,
    }

    exact = {
        "effect": "DEAL_DAMAGE",
        "target": "ANY",
        "amount": "N_3",
        "amount_value": 3,
    }

    near_amount = {
        "effect": "DEAL_DAMAGE",
        "target": "ANY",
        "amount": "N_2",
        "amount_value": 2,
    }

    near_target = {
        "effect": "DEAL_DAMAGE",
        "target": "OPPONENT",
        "amount": "N_3",
        "amount_value": 3,
    }

    unrelated = {
        "effect": "DESTROY",
        "target": "ARTIFACT_OR_ENCHANTMENT",
    }

    print("exact:", compute_binding_relevance(q, exact))
    print("near amount:", compute_binding_relevance(q, near_amount))
    print("near target:", compute_binding_relevance(q, near_target))
    print("unrelated:", compute_binding_relevance(q, unrelated, missing_policy="zero"))

