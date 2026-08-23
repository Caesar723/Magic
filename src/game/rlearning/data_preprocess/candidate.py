import random
from copy import deepcopy
from typing import Mapping, Any
import re

# Basic Definitions

ALL_EFFECTS = [
    "DEAL_DAMAGE", "DAMAGE_EACH", "STAT_EQUAL_DAMAGE",
    "GAIN_LIFE", "LOSE_LIFE", "DRAW", "DISCARD",
    "COUNTER_SPELL", "DESTROY", "EXILE", "RETURN_HAND",
    "PUT_BATTLEFIELD", "REANIMATE", "SEARCH_LIBRARY", "SEARCH_TO_HAND",
    "TEMP_BUFF", "PLUS1_COUNTER", "GRANT_KEYWORD", "CREATE_TOKEN",
    "SCRY", "PREVENT_DAMAGE", "TAP", "ADD_MANA", "SACRIFICE", "EXTRA_TURN", "MILL",
]
CREATE_TOKEN_FIELDS = ("token_power", "token_toughness", "token_keywords", "token_variants")


# near:
TARGET_NEIGHBORS = {
    "ANY": ["CREATURE", "PLAYER", "OPPONENT"],
    "CREATURE": ["ANY", "CREATURE_YOU_CONTROL", "CREATURE_OPPONENT", "RANDOM_CREATURE"],
    "CREATURE_YOU_CONTROL": ["CREATURE", "SELF", "CREATURES_YOU_CONTROL"],
    "CREATURE_OPPONENT": ["CREATURE", "RANDOM_CREATURE"],
    "CREATURES_YOU_CONTROL": ["CREATURE_YOU_CONTROL", "EACH_CREATURE", "ALL_CREATURES"],
    "PLAYER": ["OPPONENT", "YOU", "ANY"],
    "OPPONENT": ["PLAYER", "EACH_OPPONENT", "ANY"],
    "EACH_OPPONENT": ["OPPONENT", "PLAYER"],
    "EACH_CREATURE": ["ALL_CREATURES", "CREATURES_YOU_CONTROL", "CREATURE"],
    "ALL_CREATURES": ["EACH_CREATURE", "CREATURES_YOU_CONTROL", "CREATURE"],
    "SELF": ["CREATURE_YOU_CONTROL", "PERMANENT"],
    "YOU": ["PLAYER"],
    "PERMANENT": ["NONLAND_PERMANENT", "CREATURE", "ARTIFACT_OR_ENCHANTMENT"],
    "NONLAND_PERMANENT": ["PERMANENT", "CREATURE", "ARTIFACT_OR_ENCHANTMENT"],
    "SPELL": ["CREATURE"],
    "ARTIFACT_OR_ENCHANTMENT": ["NONLAND_PERMANENT", "PERMANENT"],
    "RANDOM_CREATURE": ["CREATURE", "CREATURE_OPPONENT", "RANDOM_PERMANENT"],
    "RANDOM_PERMANENT": ["PERMANENT", "NONLAND_PERMANENT", "RANDOM_CREATURE"],
    "GRAVEYARD_CREATURE": ["CREATURE", "LIBRARY_CARD"],
    "LIBRARY_CARD": ["GRAVEYARD_CREATURE", "CREATURE"],
}


TRIGGER_NEIGHBORS = {
    "ETB": ["ETB_OR_ATTACK", "CAST_CREATURE_SPELL", "CONSTELLATION", "LAND_ENTERS"],
    "ETB_OR_ATTACK": ["ETB", "ATTACK"],
    "ATTACK": ["ETB_OR_ATTACK", "DEALS_DAMAGE"],
    "DIES": ["CREATURE_DIES"],
    "CREATURE_DIES": ["DIES"],
    "SELF_DEALT_DAMAGE": ["DEALS_DAMAGE"],
    "DEALS_DAMAGE": ["SELF_DEALT_DAMAGE", "ATTACK"],
    "UPKEEP": ["END_STEP", "MAIN_PHASE"],
    "END_STEP": ["UPKEEP", "MAIN_PHASE"],
    "MAIN_PHASE": ["UPKEEP", "END_STEP"],
    "CAST_SPELL": ["CAST_INSTANT_SORCERY", "CAST_CREATURE_SPELL", "CAST_COLORED_SPELL"],
    "CAST_INSTANT_SORCERY": ["CAST_SPELL", "CAST_COLORED_SPELL"],
    "CAST_CREATURE_SPELL": ["CAST_SPELL", "ETB"],
    "CAST_COLORED_SPELL": ["CAST_SPELL", "CAST_INSTANT_SORCERY"],
    "CONSTELLATION": ["ETB"],
    "LAND_ENTERS": ["ETB"],
}


DURATION_NEIGHBORS = {
    "UNTIL_EOT": ["THIS_TURN", "PERMANENT", "NEXT_END_STEP"],
    "THIS_TURN": ["UNTIL_EOT", "INSTANT"],
    "NEXT_END_STEP": ["UNTIL_EOT", "NEXT_MAIN_PHASE"],
    "DONT_UNTAP_NEXT": ["NEXT_END_STEP", "UNTIL_EOT"],
    "AS_LONG_AS_CONTROL": ["UNTIL_LEAVES", "PERMANENT"],
    "UNTIL_LEAVES": ["AS_LONG_AS_CONTROL", "PERMANENT"],
    "PERMANENT": ["UNTIL_EOT", "UNTIL_LEAVES", "AS_LONG_AS_CONTROL"],
    "INSTANT": ["THIS_TURN", "UNTIL_EOT"],
    "NEXT_MAIN_PHASE": ["NEXT_END_STEP", "EXTRA_TURN"],
    "EXTRA_TURN": ["NEXT_MAIN_PHASE", "THIS_TURN"],
}


# hard:
# 核心 effect 改成容易混淆的 mechanic
EFFECT_HARD_NEIGHBORS = {
    "DEAL_DAMAGE": ["DAMAGE_EACH", "STAT_EQUAL_DAMAGE", "PREVENT_DAMAGE"],
    "DAMAGE_EACH": ["DEAL_DAMAGE", "STAT_EQUAL_DAMAGE"],
    "STAT_EQUAL_DAMAGE": ["DEAL_DAMAGE", "DAMAGE_EACH"],
    "GAIN_LIFE": ["LOSE_LIFE"],
    "LOSE_LIFE": ["GAIN_LIFE", "DEAL_DAMAGE"],
    "DRAW": ["SCRY", "DISCARD", "MILL"],
    "DISCARD": ["DRAW", "MILL"],
    "COUNTER_SPELL": ["RETURN_HAND", "EXILE"],
    "DESTROY": ["EXILE", "SACRIFICE"],
    "EXILE": ["DESTROY", "RETURN_HAND"],
    "RETURN_HAND": ["EXILE", "PUT_BATTLEFIELD"],
    "PUT_BATTLEFIELD": ["REANIMATE", "SEARCH_TO_HAND", "CREATE_TOKEN"],
    "REANIMATE": ["PUT_BATTLEFIELD", "RETURN_HAND"],
    "SEARCH_LIBRARY": ["SEARCH_TO_HAND", "PUT_BATTLEFIELD"],
    "SEARCH_TO_HAND": ["SEARCH_LIBRARY", "PUT_BATTLEFIELD"],
    "TEMP_BUFF": ["PLUS1_COUNTER", "GRANT_KEYWORD"],
    "PLUS1_COUNTER": ["TEMP_BUFF", "GRANT_KEYWORD"],
    "GRANT_KEYWORD": ["TEMP_BUFF", "PLUS1_COUNTER"],
    "CREATE_TOKEN": ["PUT_BATTLEFIELD", "REANIMATE"],
    "SCRY": ["DRAW", "MILL"],
    "PREVENT_DAMAGE": ["DEAL_DAMAGE"],
    "TAP": ["RETURN_HAND"],
    "ADD_MANA": ["SEARCH_LIBRARY", "PUT_BATTLEFIELD"],
    "SACRIFICE": ["DESTROY", "EXILE"],
    "EXTRA_TURN": ["ADD_MANA"],
    "MILL": ["DRAW", "SCRY", "DISCARD"],
}


def generate_exact_spec(
    query_spec: Mapping[str, Any],
) -> dict[str, Any]:
    """复制 query，生成语义完全相同的候选。"""

    return deepcopy(dict(query_spec))


def _mutate_number(value: int) -> int:
    return random.choice([value + 1, value - 1] if value > 0 else [value + 1])


def _mutate_token_keywords(keywords, libraries) -> list[str]:
    static_types = list((libraries or {}).get("statics", {}).get("types", {}))
    if not static_types:
        return list(keywords)
    index = random.randrange(len(keywords))
    choices = [keyword for keyword in static_types if keyword != keywords[index]]
    result = list(keywords)
    result[index] = random.choice(choices)
    return result


def _mutate_token_variant(variants, libraries) -> list[dict[str, Any]]:
    result = deepcopy(variants)
    candidates = [
        (index, field) for index, variant in enumerate(result)
        for field in ("token_power", "token_toughness", "token_keywords")
        if isinstance(variant.get(field), int) or (field == "token_keywords" and variant.get(field))
    ]
    index, field = random.choice(candidates)
    if field == "token_keywords":
        result[index][field] = _mutate_token_keywords(result[index][field], libraries)
    else:
        result[index][field] = _mutate_number(result[index][field])
    return result


def generate_near_spec(
    query_spec: Mapping[str, Any], libraries=None, valid_binding_pool=None,
) -> dict[str, Any]:
    """保持核心 effect，只随机改动一个辅助字段。"""
    spec = deepcopy(dict(query_spec))
    can_change_amount = isinstance(spec.get("amount_value"), (int, float)) and not spec.get("token_variants")
    mutation_options = ["amount"] if can_change_amount else []
    neighbor_maps = {
        "target": TARGET_NEIGHBORS,
        "duration": DURATION_NEIGHBORS,
        "trigger": TRIGGER_NEIGHBORS,
    }
    for field, neighbors in neighbor_maps.items():
        if spec.get(field) in neighbors and neighbors[spec[field]]:
            mutation_options.append(field)

    if spec.get("effect") == "CREATE_TOKEN":
        mutation_options += [
            field for field in ("token_power", "token_toughness") if isinstance(spec.get(field), int)
        ]
        if spec.get("token_keywords") and (libraries or {}).get("statics", {}).get("types"):
            mutation_options.append("token_keywords")
        if spec.get("token_variants"):
            mutation_options.append("token_variants")

    if not mutation_options:
        return generate_hard_spec(spec, valid_binding_pool)
    mutation = random.choice(mutation_options)
    if mutation == "amount":
        value = spec["amount_value"]
        candidates = [value + 1]
        if value > 1:
            candidates.insert(0, value - 1)
        new_value = random.choice(candidates)
        spec["amount_value"] = new_value
        if isinstance(new_value, int) and 1 <= new_value <= 5:
            spec["amount"] = f"N_{new_value}"
        else:
            spec["amount"] = "FIXED"
    elif mutation in {"token_power", "token_toughness"}:
        spec[mutation] = _mutate_number(spec[mutation])
    elif mutation == "token_keywords":
        spec[mutation] = _mutate_token_keywords(spec[mutation], libraries)
    elif mutation == "token_variants":
        spec[mutation] = _mutate_token_variant(spec[mutation], libraries)
    else:
        choices = neighbor_maps[mutation][spec[mutation]]
        if mutation == "target" and spec.get("effect") == "DAMAGE_EACH":
            choices = [target for target in choices if target in {
                "EACH_CREATURE", "ALL_CREATURES", "EACH_OPPONENT", "CREATURES_YOU_CONTROL"
            }]
        if not choices:
            return generate_hard_spec(spec, valid_binding_pool)
        spec[mutation] = random.choice(choices)

    return spec


def generate_hard_spec(
    query_spec: Mapping[str, Any], valid_binding_pool=None,
) -> dict[str, Any]:
    """把 effect 改为容易混淆的机制，并同步修正相关字段。"""

    spec = deepcopy(dict(query_spec))

    current_effect = spec.get("effect")

    if current_effect not in EFFECT_HARD_NEIGHBORS:
        return generate_random_spec(spec, valid_binding_pool)

    choices = list(EFFECT_HARD_NEIGHBORS[current_effect])
    token_donors = [
        binding for binding in valid_binding_pool or [] if binding.get("effect") == "CREATE_TOKEN"
    ]
    if "CREATE_TOKEN" in choices and not token_donors:
        choices.remove("CREATE_TOKEN")

    if not choices:
        return generate_random_spec(spec, valid_binding_pool)

    new_effect = random.choice(choices)
    effect_donors = [binding for binding in valid_binding_pool or [] if binding.get("effect") == new_effect]
    if effect_donors:
        return deepcopy(random.choice(effect_donors))
    return generate_valid_spec_for_effect(new_effect)


def generate_random_spec(
    query_spec: Mapping[str, Any], valid_binding_pool=None,
) -> dict[str, Any]:
    """选择与 query 明显不同的 effect，生成随机合法候选。"""
    query_effect = query_spec.get("effect")
    excluded = {query_effect}
    excluded.update(EFFECT_HARD_NEIGHBORS.get(query_effect, []))
    candidate_effects = [effect for effect in ALL_EFFECTS if effect not in excluded]
    if not candidate_effects:
        candidate_effects = [effect for effect in ALL_EFFECTS if effect != query_effect]
    real_candidates = [
        binding for binding in valid_binding_pool or [] if binding.get("effect") in candidate_effects
    ]
    if real_candidates:
        return deepcopy(random.choice(real_candidates))
    return generate_valid_spec_for_effect(random.choice(candidate_effects))


def random_fixed_amount(
    min_value=1,
    max_value=5,
):
    value = random.randint(min_value, max_value)
    return {
        "amount_value": value,
        "amount": f"N_{value}",
    }


def generate_valid_spec_for_effect(
    effect: str,
) -> dict[str, Any]:
    """为指定 effect 生成渲染所需字段齐全的最小随机 spec。"""
    spec = {"effect": effect}
    fixed_amount_targets = {
        "DEAL_DAMAGE": [
            "ANY", "CREATURE", "CREATURE_OPPONENT", "PLAYER", "OPPONENT"
        ],
        "DAMAGE_EACH": ["EACH_CREATURE", "ALL_CREATURES", "EACH_OPPONENT"],
        "LOSE_LIFE": ["OPPONENT", "PLAYER", "EACH_OPPONENT"],
        "DISCARD": ["OPPONENT", "PLAYER"],
        "MILL": ["YOU", "OPPONENT", "PLAYER"],
    }
    if effect in fixed_amount_targets:
        spec["target"] = random.choice(fixed_amount_targets[effect])
        spec.update(random_fixed_amount())
    elif effect == "STAT_EQUAL_DAMAGE":
        spec["target"] = random.choice(["CREATURE", "ANY"])
        spec["amount"] = random.choice(["EQUAL_POWER", "EQUAL_TOUGHNESS"])
    elif effect == "GAIN_LIFE":
        spec["target"] = "YOU"
        spec.update(random_fixed_amount())
    elif effect in {"DRAW", "SCRY", "PREVENT_DAMAGE"}:
        spec.update(random_fixed_amount())
    elif effect in {"DESTROY", "EXILE"}:
        spec["target"] = random.choice(
            [
                "CREATURE", "CREATURE_OPPONENT", "PERMANENT", "NONLAND_PERMANENT",
                "ARTIFACT_OR_ENCHANTMENT",
            ]
        )
    elif effect == "SACRIFICE":
        spec["target"] = random.choice(["OPPONENT", "EACH_OPPONENT", "CREATURE_YOU_CONTROL"])
    elif effect == "RETURN_HAND":
        spec["target"] = random.choice(["CREATURE", "PERMANENT", "NONLAND_PERMANENT"])
    elif effect in {
        "COUNTER_SPELL", "PUT_BATTLEFIELD", "REANIMATE", "SEARCH_LIBRARY", "SEARCH_TO_HAND"
    }:
        spec["target"] = {
            "COUNTER_SPELL": "SPELL",
            "PUT_BATTLEFIELD": "LIBRARY_CARD",
            "REANIMATE": "GRAVEYARD_CREATURE",
            "SEARCH_LIBRARY": "LIBRARY_CARD",
            "SEARCH_TO_HAND": "LIBRARY_CARD",
        }[effect]
    elif effect == "TEMP_BUFF":
        spec["target"] = random.choice(
            ["SELF", "CREATURE", "CREATURE_YOU_CONTROL", "CREATURES_YOU_CONTROL"]
        )
        value = random.randint(1, 4)
        spec.update(
            duration="UNTIL_EOT", amount=f"N_{value}", amount_value=value, p=value, t=value
        )
    elif effect == "PLUS1_COUNTER":
        spec["target"] = random.choice(["SELF", "CREATURE", "CREATURE_YOU_CONTROL"])
        value = random.randint(1, 3)
        spec.update(duration="PERMANENT", amount=f"N_{value}", amount_value=value, p=1, t=1)
    elif effect == "GRANT_KEYWORD":
        spec["target"] = random.choice(
            ["SELF", "CREATURE", "CREATURE_YOU_CONTROL", "CREATURES_YOU_CONTROL"]
        )
        spec["duration"] = random.choice(["UNTIL_EOT", "PERMANENT"])
        spec["keyword"] = random.choice(
            [
                "FLYING", "TRAMPLE", "VIGILANCE", "LIFELINK", "HEXPROOF", "INDESTRUCTIBLE",
                "HASTE", "MENACE", "DEATHTOUCH",
            ]
        )
    elif effect == "CREATE_TOKEN":
        spec["amount"] = random.choice(["N_1", "N_2", "N_3"])
        spec["amount_value"] = int(spec["amount"].split("_")[1])
    elif effect == "TAP":
        spec["target"] = random.choice(["CREATURE", "CREATURE_OPPONENT", "PERMANENT"])
    elif effect == "ADD_MANA":
        spec.update(random_fixed_amount(1, 3), color=random.choice(["white", "blue", "black", "red", "green"]))
    elif effect == "EXTRA_TURN":
        spec["duration"] = "EXTRA_TURN"

    return spec


def normalize_candidate_spec(
    spec: Mapping[str, Any],
) -> dict[str, Any]:
    """按 effect 补齐确定字段，并删除与该 effect 无关的字段。"""
    spec = deepcopy(dict(spec))
    effect = spec.get("effect")
    if effect is None:
        return spec

    if effect in {"DRAW", "SCRY", "CREATE_TOKEN", "ADD_MANA", "EXTRA_TURN"}:
        spec.pop("target", None)

    target_by_effect = {
        "COUNTER_SPELL": "SPELL",
        "SEARCH_LIBRARY": "LIBRARY_CARD",
        "SEARCH_TO_HAND": "LIBRARY_CARD",
        "PUT_BATTLEFIELD": "LIBRARY_CARD",
        "REANIMATE": "GRAVEYARD_CREATURE",
    }
    if effect in target_by_effect:
        spec["target"] = target_by_effect[effect]

    if effect == "DAMAGE_EACH":
        valid_targets = {"EACH_CREATURE", "ALL_CREATURES", "EACH_OPPONENT", "CREATURES_YOU_CONTROL"}
        target = spec.get("target")
        if target is None:
            spec["target"] = "EACH_CREATURE"
        elif target not in valid_targets:
            raise ValueError(f"Invalid target {target!r} for DAMAGE_EACH: {spec}")

    if effect == "TEMP_BUFF":
        spec.setdefault("duration", "UNTIL_EOT")
    elif effect == "PLUS1_COUNTER":
        spec["duration"] = "PERMANENT"
    elif effect == "EXTRA_TURN":
        for key in ("duration", "target", "amount", "amount_value", "p", "t", "keyword"):
            spec.pop(key, None)

    if effect != "GRANT_KEYWORD":
        spec.pop("keyword", None)
    if effect != "TEMP_BUFF":
        for key in ("p", "t"):
            spec.pop(key, None)
    if effect != "CREATE_TOKEN":
        for key in CREATE_TOKEN_FIELDS:
            spec.pop(key, None)
    elif isinstance(spec.get("token_variants"), list):
        variants = []
        for variant in spec["token_variants"]:
            if not isinstance(variant, Mapping):
                variants.append(variant)
                continue
            normalized = dict(variant)
            if isinstance(normalized.get("token_keywords"), list):
                normalized["token_keywords"] = sorted(set(normalized["token_keywords"]))
                if not normalized["token_keywords"]:
                    normalized.pop("token_keywords")
            variants.append(normalized)
        spec["token_variants"] = variants
        for key in ("token_power", "token_toughness", "token_keywords"):
            spec.pop(key, None)
    elif isinstance(spec.get("token_keywords"), list):
        spec["token_keywords"] = sorted(set(spec["token_keywords"]))
        if not spec["token_keywords"]:
            spec.pop("token_keywords")
    amount_value = spec.get("amount_value")
    if isinstance(amount_value, int):
        if 1 <= amount_value <= 5:
            spec["amount"] = f"N_{amount_value}"
        elif spec.get("amount") in {
            "N_1",
            "N_2",
            "N_3",
            "N_4",
            "N_5",
        }:
            spec["amount"] = "FIXED"

    return spec


PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


# 1. 从 candidate templates 自动判断需要哪些 slot


def get_required_candidate_slots(
    effect: str,
    libraries,
) -> set[str]:
    """从 effect 模板和 required_slots 推导渲染所需字段。"""
    if effect == "CREATE_TOKEN":
        return set()
    effect_configs = libraries["effects"]["candidate_render"]
    if effect not in effect_configs:
        raise ValueError(f"Unknown candidate effect: {effect}")
    config = effect_configs[effect]
    templates = config.get("templates", [])
    if not templates:
        raise ValueError(f"No candidate templates for effect: {effect}")
    slots = {slot for template in templates for slot in PLACEHOLDER_RE.findall(template)}
    slots.update(config.get("required_slots", []))
    return slots


# 2. 判断一个 slot 在 spec 里是否真的存在


def candidate_slot_exists(
    spec: Mapping[str, Any],
    slot: str,
) -> bool:
    if slot == "amount":
        return spec.get("amount") is not None or spec.get("amount_value") is not None
    if slot == "keyword":
        return spec.get("keyword") is not None or spec.get("static") is not None
    return spec.get(slot) is not None


# 3. 对 parsed binding 做保守的 canonicalize


def prepare_candidate_binding(
    binding: Mapping[str, Any],
    card: Mapping[str, Any] = None,
) -> dict[str, Any]:
    """只做可确定的字段统一，不猜测缺失语义。"""
    if not isinstance(binding, Mapping):
        raise TypeError(f"binding must be Mapping, got {type(binding)}")
    spec = deepcopy(dict(binding))
    if spec.get("effect") == "GRANT_KEYWORD":
        if spec.get("keyword") is None and spec.get("static") is not None:
            spec["keyword"] = spec.pop("static")
        if spec.get("keyword") is None and card is not None:
            statics = card.get("statics", [])
            if len(statics) == 1:
                spec["keyword"] = statics[0]

    if spec.get("effect") == "STAT_EQUAL_DAMAGE" and spec.get("stat") is None:
        stat_map = {
            "EQUAL_POWER": "its power",
            "EQUAL_TOUGHNESS": "its toughness",
            "EQUAL_LIFE": "your life total",
        }
        if (amount_type := spec.get("amount")) in stat_map:
            spec["stat"] = stat_map[amount_type]
    return normalize_candidate_spec(spec)


# 4. validate


def validate_candidate_spec(
    spec: dict[str, Any],
    libraries,
) -> None:
    """校验候选 spec 是否能被 renderer 完整且合法地渲染。"""
    effect = spec.get("effect")
    if effect is None:
        raise ValueError(f"Missing effect: {spec}")
    effect_configs = libraries["effects"]["candidate_render"]
    if effect not in effect_configs:
        raise ValueError(f"Unknown effect: {effect!r}")
    required_slots = get_required_candidate_slots(effect, libraries)
    missing = [slot for slot in required_slots if not candidate_slot_exists(spec, slot)]

    if missing:
        raise ValueError(
            f"Incomplete candidate spec: "
            f"effect={effect}, "
            f"missing={sorted(missing)}, "
            f"spec={spec}"
        )

    target = spec.get("target")
    if target is not None:
        target_types = libraries["targets"]["types"]
        if target not in target_types:
            raise ValueError(f"Unknown target {target!r} for effect={effect}")

    duration = spec.get("duration")
    if duration is not None:
        duration_types = libraries["durations"]["types"]
        if duration not in duration_types:
            raise ValueError(f"Unknown duration {duration!r} for effect={effect}")

    keyword = spec.get("keyword") or spec.get("static")
    if keyword is not None:
        static_types = libraries["statics"]["types"]
        if keyword not in static_types:
            raise ValueError(f"Unknown keyword {keyword!r} for effect={effect}")

    amount = spec.get("amount")
    if amount is not None:
        amount_types = libraries["amounts"]["types"]
        if amount not in amount_types:
            raise ValueError(f"Unknown amount {amount!r} for effect={effect}")

    for field in ("p", "t"):
        if field in required_slots and not isinstance(spec.get(field), int):
            raise ValueError(f"{field} must be int: {spec}")

    if "color" in required_slots:
        valid_colors = {"white", "blue", "black", "red", "green", "colorless"}
        if spec.get("color") not in valid_colors:
            raise ValueError(f"Invalid mana color {spec.get('color')!r}: {spec}")

    if effect == "CREATE_TOKEN":
        _validate_create_token_spec(spec, libraries)


def _validate_token_profile(profile: Mapping[str, Any], static_types, *, variant=False) -> None:
    if variant and "count" in profile:
        count = profile["count"]
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise ValueError(f"Token variant count must be a positive int: {profile}")
    for field in ("token_power", "token_toughness"):
        if field in profile and (not isinstance(profile[field], int) or isinstance(profile[field], bool)):
            raise ValueError(f"{field} must be int: {profile}")
    if "token_keywords" in profile:
        keywords = profile["token_keywords"]
        if not isinstance(keywords, list) or any(keyword not in static_types for keyword in keywords):
            raise ValueError(f"Unknown token keyword: {profile}")


def _validate_create_token_spec(spec: Mapping[str, Any], libraries) -> None:
    amount_value = spec.get("amount_value")
    if amount_value is not None and (not isinstance(amount_value, int) or isinstance(amount_value, bool) or amount_value < 1):
        raise ValueError(f"CREATE_TOKEN amount_value must be a positive int: {spec}")

    static_types = libraries["statics"]["types"]
    _validate_token_profile(spec, static_types)
    variants = spec.get("token_variants")
    if variants is None:
        return
    if not isinstance(variants, list) or not variants:
        raise ValueError(f"token_variants must be a non-empty list: {spec}")
    if any(field in spec for field in ("token_power", "token_toughness", "token_keywords")):
        raise ValueError(f"Flat token fields cannot be mixed with token_variants: {spec}")
    if any(not isinstance(variant, Mapping) for variant in variants):
        raise ValueError(f"Every token variant must be a mapping: {spec}")
    for variant in variants:
        _validate_token_profile(variant, static_types, variant=True)
    if isinstance(amount_value, int) and all("count" in variant for variant in variants):
        if sum(variant["count"] for variant in variants) != amount_value:
            raise ValueError(f"Token variant counts must equal amount_value: {spec}")


# 5. 从 parsed cards 建立真正合法的 binding pool


def build_valid_binding_pool(
    cards,
    libraries,
) -> list[dict[str, Any]]:
    """从解析卡牌中筛出能被 candidate renderer 完整渲染的 binding。"""
    pool = []
    for card in cards:
        for binding in card.get("bindings", []):
            if not isinstance(binding, Mapping) or not binding.get("effect"):
                continue
            try:
                spec = prepare_candidate_binding(binding, card=card)
                validate_candidate_spec(spec, libraries)
            except (ValueError, KeyError, TypeError):
                continue
            pool.append(spec)
    return pool


# 6. 随机生成一个 binding


def generate_random_binding(
    valid_binding_pool,
    libraries,
) -> dict[str, Any]:
    """从已验证的真实 binding pool 中随机抽取一个 binding。"""
    if not valid_binding_pool:
        raise ValueError("valid_binding_pool is empty")
    spec = deepcopy(random.choice(valid_binding_pool))
    validate_candidate_spec(spec, libraries)
    return spec


def get_random_bindings(
    valid_binding_pool,
    libraries,
    min_bindings: int = 1,
    max_bindings: int = 3,
    unique_effects: bool = True,
) -> list[dict[str, Any]]:
    """随机挑选多个合法 binding，默认避免重复 effect。"""
    if not valid_binding_pool:
        raise ValueError("valid_binding_pool is empty")

    if min_bindings < 1:
        raise ValueError("min_bindings must be >= 1")

    if max_bindings < min_bindings:
        raise ValueError("max_bindings must be >= min_bindings")

    n = random.randint(min_bindings, max_bindings)
    if not unique_effects:
        return [generate_random_binding(valid_binding_pool, libraries) for _ in range(n)]

    by_effect = {}
    for spec in valid_binding_pool:
        effect = spec.get("effect")
        if effect is None:
            continue
        by_effect.setdefault(effect, []).append(spec)
    effects = list(by_effect.keys())
    if not effects:
        raise ValueError("No valid effects in valid_binding_pool")
    chosen_effects = random.sample(effects, k=min(n, len(effects)))
    result = []
    for effect in chosen_effects:
        spec = deepcopy(random.choice(by_effect[effect]))
        validate_candidate_spec(spec, libraries)
        result.append(spec)
    return result
