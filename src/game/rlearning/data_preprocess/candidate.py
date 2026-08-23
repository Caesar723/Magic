import random
from copy import deepcopy
from typing import Mapping, Any
import re

# ============================================================
# Basic Definitions
# ============================================================

ALL_EFFECTS = [
    "DEAL_DAMAGE",
    "DAMAGE_EACH",
    "STAT_EQUAL_DAMAGE",
    "GAIN_LIFE",
    "LOSE_LIFE",
    "DRAW",
    "DISCARD",
    "COUNTER_SPELL",
    "DESTROY",
    "EXILE",
    "RETURN_HAND",
    "PUT_BATTLEFIELD",
    "REANIMATE",
    "SEARCH_LIBRARY",
    "SEARCH_TO_HAND",
    "TEMP_BUFF",
    "PLUS1_COUNTER",
    "GRANT_KEYWORD",
    "CREATE_TOKEN",
    "SCRY",
    "PREVENT_DAMAGE",
    "TAP",
    "ADD_MANA",
    "SACRIFICE",
    "EXTRA_TURN",
    "MILL",
]


# near:
# effect 不变，只改变 target / amount / duration / trigger 等
TARGET_NEIGHBORS = {
    "ANY": [
        "CREATURE",
        "PLAYER",
        "OPPONENT",
    ],

    "CREATURE": [
        "ANY",
        "CREATURE_YOU_CONTROL",
        "CREATURE_OPPONENT",
        "RANDOM_CREATURE",
    ],

    "CREATURE_YOU_CONTROL": [
        "CREATURE",
        "SELF",
        "CREATURES_YOU_CONTROL",
    ],

    "CREATURE_OPPONENT": [
        "CREATURE",
        "RANDOM_CREATURE",
    ],

    "CREATURES_YOU_CONTROL": [
        "CREATURE_YOU_CONTROL",
        "EACH_CREATURE",
        "ALL_CREATURES",
    ],

    "PLAYER": [
        "OPPONENT",
        "YOU",
        "ANY",
    ],

    "OPPONENT": [
        "PLAYER",
        "EACH_OPPONENT",
        "ANY",
    ],

    "EACH_OPPONENT": [
        "OPPONENT",
        "PLAYER",
    ],

    "EACH_CREATURE": [
        "ALL_CREATURES",
        "CREATURES_YOU_CONTROL",
        "CREATURE",
    ],

    "ALL_CREATURES": [
        "EACH_CREATURE",
        "CREATURES_YOU_CONTROL",
        "CREATURE",
    ],

    "SELF": [
        "CREATURE_YOU_CONTROL",
        "PERMANENT",
    ],

    "YOU": [
        "PLAYER",
    ],

    "PERMANENT": [
        "NONLAND_PERMANENT",
        "CREATURE",
        "ARTIFACT_OR_ENCHANTMENT",
    ],

    "NONLAND_PERMANENT": [
        "PERMANENT",
        "CREATURE",
        "ARTIFACT_OR_ENCHANTMENT",
    ],

    "SPELL": [
        "CREATURE",
    ],

    "ARTIFACT_OR_ENCHANTMENT": [
        "NONLAND_PERMANENT",
        "PERMANENT",
    ],

    "RANDOM_CREATURE": [
        "CREATURE",
        "CREATURE_OPPONENT",
        "RANDOM_PERMANENT",
    ],

    "RANDOM_PERMANENT": [
        "PERMANENT",
        "NONLAND_PERMANENT",
        "RANDOM_CREATURE",
    ],

    "GRAVEYARD_CREATURE": [
        "CREATURE",
        "LIBRARY_CARD",
    ],

    "LIBRARY_CARD": [
        "GRAVEYARD_CREATURE",
        "CREATURE",
    ],
}


TRIGGER_NEIGHBORS = {
    "ETB": [
        "ETB_OR_ATTACK",
        "CAST_CREATURE_SPELL",
        "CONSTELLATION",
        "LAND_ENTERS",
    ],

    "ETB_OR_ATTACK": [
        "ETB",
        "ATTACK",
    ],

    "ATTACK": [
        "ETB_OR_ATTACK",
        "DEALS_DAMAGE",
    ],

    "DIES": [
        "CREATURE_DIES",
    ],

    "CREATURE_DIES": [
        "DIES",
    ],

    "SELF_DEALT_DAMAGE": [
        "DEALS_DAMAGE",
    ],

    "DEALS_DAMAGE": [
        "SELF_DEALT_DAMAGE",
        "ATTACK",
    ],

    "UPKEEP": [
        "END_STEP",
        "MAIN_PHASE",
    ],

    "END_STEP": [
        "UPKEEP",
        "MAIN_PHASE",
    ],

    "MAIN_PHASE": [
        "UPKEEP",
        "END_STEP",
    ],

    "CAST_SPELL": [
        "CAST_INSTANT_SORCERY",
        "CAST_CREATURE_SPELL",
        "CAST_COLORED_SPELL",
    ],

    "CAST_INSTANT_SORCERY": [
        "CAST_SPELL",
        "CAST_COLORED_SPELL",
    ],

    "CAST_CREATURE_SPELL": [
        "CAST_SPELL",
        "ETB",
    ],

    "CAST_COLORED_SPELL": [
        "CAST_SPELL",
        "CAST_INSTANT_SORCERY",
    ],

    "CONSTELLATION": [
        "ETB",
    ],

    "LAND_ENTERS": [
        "ETB",
    ],
}


DURATION_NEIGHBORS = {
    "UNTIL_EOT": [
        "THIS_TURN",
        "PERMANENT",
        "NEXT_END_STEP",
    ],

    "THIS_TURN": [
        "UNTIL_EOT",
        "INSTANT",
    ],

    "NEXT_END_STEP": [
        "UNTIL_EOT",
        "NEXT_MAIN_PHASE",
    ],

    "DONT_UNTAP_NEXT": [
        "NEXT_END_STEP",
        "UNTIL_EOT",
    ],

    "AS_LONG_AS_CONTROL": [
        "UNTIL_LEAVES",
        "PERMANENT",
    ],

    "UNTIL_LEAVES": [
        "AS_LONG_AS_CONTROL",
        "PERMANENT",
    ],

    "PERMANENT": [
        "UNTIL_EOT",
        "UNTIL_LEAVES",
        "AS_LONG_AS_CONTROL",
    ],

    "INSTANT": [
        "THIS_TURN",
        "UNTIL_EOT",
    ],

    "NEXT_MAIN_PHASE": [
        "NEXT_END_STEP",
        "EXTRA_TURN",
    ],

    "EXTRA_TURN": [
        "NEXT_MAIN_PHASE",
        "THIS_TURN",
    ],
}


# hard:
# 核心 effect 改成容易混淆的 mechanic
EFFECT_HARD_NEIGHBORS = {
    "DEAL_DAMAGE": [
        "DAMAGE_EACH",
        "STAT_EQUAL_DAMAGE",
        "PREVENT_DAMAGE",
    ],

    "DAMAGE_EACH": [
        "DEAL_DAMAGE",
        "STAT_EQUAL_DAMAGE",
    ],

    "STAT_EQUAL_DAMAGE": [
        "DEAL_DAMAGE",
        "DAMAGE_EACH",
    ],

    "GAIN_LIFE": [
        "LOSE_LIFE",
    ],

    "LOSE_LIFE": [
        "GAIN_LIFE",
        "DEAL_DAMAGE",
    ],

    "DRAW": [
        "SCRY",
        "DISCARD",
        "MILL",
    ],

    "DISCARD": [
        "DRAW",
        "MILL",
    ],

    "COUNTER_SPELL": [
        "RETURN_HAND",
        "EXILE",
    ],

    "DESTROY": [
        "EXILE",
        "SACRIFICE",
    ],

    "EXILE": [
        "DESTROY",
        "RETURN_HAND",
    ],

    "RETURN_HAND": [
        "EXILE",
        "PUT_BATTLEFIELD",
    ],

    "PUT_BATTLEFIELD": [
        "REANIMATE",
        "SEARCH_TO_HAND",
        "CREATE_TOKEN",
    ],

    "REANIMATE": [
        "PUT_BATTLEFIELD",
        "RETURN_HAND",
    ],

    "SEARCH_LIBRARY": [
        "SEARCH_TO_HAND",
        "PUT_BATTLEFIELD",
    ],

    "SEARCH_TO_HAND": [
        "SEARCH_LIBRARY",
        "PUT_BATTLEFIELD",
    ],

    "TEMP_BUFF": [
        "PLUS1_COUNTER",
        "GRANT_KEYWORD",
    ],

    "PLUS1_COUNTER": [
        "TEMP_BUFF",
        "GRANT_KEYWORD",
    ],

    "GRANT_KEYWORD": [
        "TEMP_BUFF",
        "PLUS1_COUNTER",
    ],

    "CREATE_TOKEN": [
        "PUT_BATTLEFIELD",
        "REANIMATE",
    ],

    "SCRY": [
        "DRAW",
        "MILL",
    ],

    "PREVENT_DAMAGE": [
        "DEAL_DAMAGE",
    ],

    "TAP": [
        "RETURN_HAND",
    ],

    "ADD_MANA": [
        "SEARCH_LIBRARY",
        "PUT_BATTLEFIELD",
    ],

    "SACRIFICE": [
        "DESTROY",
        "EXILE",
    ],

    "EXTRA_TURN": [
        "ADD_MANA",
    ],

    "MILL": [
        "DRAW",
        "SCRY",
        "DISCARD",
    ],
}



def generate_exact_spec(
    query_spec: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Exact candidate:
    query 明确要求的语义全部保持不变。
    """

    return deepcopy(dict(query_spec))


def generate_near_spec(
    query_spec: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Near candidate:
    核心 effect 尽量不变，
    随机改变一个 modifier：
        amount
        target
        duration
        trigger
    """

    spec = deepcopy(dict(query_spec))

    mutation_options = []

    # -------------------------
    # amount 可以修改
    # -------------------------

    if isinstance(spec.get("amount_value"), (int, float)):
        mutation_options.append("amount")

    # -------------------------
    # target 可以修改
    # -------------------------

    target = spec.get("target")

    if target in TARGET_NEIGHBORS:
        if TARGET_NEIGHBORS[target]:
            mutation_options.append("target")

    # -------------------------
    # duration 可以修改
    # -------------------------

    duration = spec.get("duration")

    if duration in DURATION_NEIGHBORS:
        if DURATION_NEIGHBORS[duration]:
            mutation_options.append("duration")

    # -------------------------
    # trigger 可以修改
    # -------------------------

    trigger = spec.get("trigger")

    if trigger in TRIGGER_NEIGHBORS:
        if TRIGGER_NEIGHBORS[trigger]:
            mutation_options.append("trigger")

    # 没有 modifier 可以动
    # 则退化成 hard
    if not mutation_options:
        return generate_hard_spec(spec)

    # 可以以后改成 random.choices + weights
    mutation = random.choice(
        mutation_options
    )

    # =========================
    # mutate amount
    # =========================

    if mutation == "amount":

        value = spec["amount_value"]

        candidates = []

        # 差 1 最适合作为 near
        if value > 1:
            candidates.append(value - 1)

        candidates.append(value + 1)

        new_value = random.choice(
            candidates
        )

        spec["amount_value"] = new_value

        # 你的 N_1 ... N_5
        if (
            isinstance(new_value, int)
            and 1 <= new_value <= 5
        ):
            spec["amount"] = f"N_{new_value}"

        else:
            spec["amount"] = "FIXED"

    # =========================
    # mutate target
    # =========================

    elif mutation == "target":

        current = spec["target"]

        spec["target"] = random.choice(
            TARGET_NEIGHBORS[current]
        )

    # =========================
    # mutate duration
    # =========================

    elif mutation == "duration":

        current = spec["duration"]

        spec["duration"] = random.choice(
            DURATION_NEIGHBORS[current]
        )

    # =========================
    # mutate trigger
    # =========================

    elif mutation == "trigger":

        current = spec["trigger"]

        spec["trigger"] = random.choice(
            TRIGGER_NEIGHBORS[current]
        )

    return spec


def generate_hard_spec(
    query_spec: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Hard candidate:
    修改核心 mechanic，
    但只改成容易和原 mechanic 混淆的 effect。
    """

    spec = deepcopy(dict(query_spec))

    current_effect = spec.get("effect")

    # 当前 effect 没有定义 hard neighbor
    if current_effect not in EFFECT_HARD_NEIGHBORS:
        return generate_random_spec(spec)

    choices = EFFECT_HARD_NEIGHBORS[
        current_effect
    ]

    if not choices:
        return generate_random_spec(spec)

    new_effect = random.choice(
        choices
    )

    spec["effect"] = new_effect

    # ------------------------------------------------
    # 对一些 mechanic 做联动修改
    # ------------------------------------------------

    if new_effect == "DAMAGE_EACH":

        spec["target"] = random.choice([
            "EACH_CREATURE",
            "ALL_CREATURES",
        ])

    elif new_effect == "PREVENT_DAMAGE":

        # prevent damage 通常不是
        # "prevent damage to ANY target"
        spec.pop("target", None)

    elif new_effect == "DRAW":

        spec.pop("target", None)

    elif new_effect == "SCRY":

        spec.pop("target", None)

    elif new_effect == "MILL":

        # 可以根据你的数据决定 YOU / OPPONENT
        if spec.get("target") not in {
            "YOU",
            "PLAYER",
            "OPPONENT",
        }:
            spec.pop("target", None)

    elif new_effect == "COUNTER_SPELL":

        spec["target"] = "SPELL"

    elif new_effect == "SEARCH_LIBRARY":

        spec["target"] = "LIBRARY_CARD"

    elif new_effect == "SEARCH_TO_HAND":

        spec["target"] = "LIBRARY_CARD"

    elif new_effect == "REANIMATE":

        spec["target"] = "GRAVEYARD_CREATURE"

    elif new_effect == "PLUS1_COUNTER":

        # counter 一般是永久
        spec["duration"] = "PERMANENT"

    elif new_effect == "TEMP_BUFF":

        # temporary buff 通常直到 EOT
        if spec.get("duration") is None:
            spec["duration"] = "UNTIL_EOT"

    elif new_effect == "EXTRA_TURN":

        spec.pop("target", None)
        spec.pop("amount", None)
        spec.pop("amount_value", None)
        spec.pop("p", None)
        spec.pop("t", None)

    elif new_effect == "ADD_MANA":

        spec.pop("target", None)

    return spec

def generate_random_spec(
    query_spec: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Random candidate:
    从和 query effect 明显不同的 effect 中随机选，
    然后生成一个合法 spec。
    """

    query_effect = query_spec.get("effect")

    excluded = {
        query_effect,
    }

    # hard neighbors 也排除掉，
    # 不然 random 很容易生成成 hard
    excluded.update(
        EFFECT_HARD_NEIGHBORS.get(
            query_effect,
            []
        )
    )

    candidate_effects = [
        effect
        for effect in ALL_EFFECTS
        if effect not in excluded
    ]

    if not candidate_effects:
        candidate_effects = [
            effect
            for effect in ALL_EFFECTS
            if effect != query_effect
        ]

    new_effect = random.choice(
        candidate_effects
    )

    return generate_valid_spec_for_effect(
        new_effect
    )

def random_fixed_amount(
    min_value=1,
    max_value=5,
):
    value = random.randint(
        min_value,
        max_value,
    )

    return {
        "amount_value": value,
        "amount": f"N_{value}",
    }


def generate_valid_spec_for_effect(
    effect: str,
) -> dict[str, Any]:

    spec = {
        "effect": effect
    }

    # ========================================================
    # DAMAGE
    # ========================================================

    if effect == "DEAL_DAMAGE":

        spec["target"] = random.choice([
            "ANY",
            "CREATURE",
            "CREATURE_OPPONENT",
            "PLAYER",
            "OPPONENT",
        ])

        spec.update(
            random_fixed_amount()
        )

    elif effect == "DAMAGE_EACH":

        spec["target"] = random.choice([
            "EACH_CREATURE",
            "ALL_CREATURES",
            "EACH_OPPONENT",
        ])

        spec.update(
            random_fixed_amount()
        )

    elif effect == "STAT_EQUAL_DAMAGE":

        spec["target"] = random.choice([
            "CREATURE",
            "ANY",
        ])

        spec["amount"] = random.choice([
            "EQUAL_POWER",
            "EQUAL_TOUGHNESS",
        ])

    # ========================================================
    # LIFE
    # ========================================================

    elif effect == "GAIN_LIFE":

        spec["target"] = "YOU"
        spec.update(random_fixed_amount())

    elif effect == "LOSE_LIFE":

        spec["target"] = random.choice([
            "OPPONENT",
            "PLAYER",
            "EACH_OPPONENT",
        ])

        spec.update(random_fixed_amount())

    # ========================================================
    # CARD ADVANTAGE
    # ========================================================

    elif effect == "DRAW":

        spec.update(random_fixed_amount())

    elif effect == "DISCARD":

        spec["target"] = random.choice([
            "OPPONENT",
            "PLAYER",
        ])

        spec.update(random_fixed_amount())

    elif effect == "SCRY":

        spec.update(random_fixed_amount())

    elif effect == "MILL":

        spec["target"] = random.choice([
            "YOU",
            "OPPONENT",
            "PLAYER",
        ])

        spec.update(random_fixed_amount())

    # ========================================================
    # COUNTER
    # ========================================================

    elif effect == "COUNTER_SPELL":

        spec["target"] = "SPELL"

    # ========================================================
    # REMOVAL
    # ========================================================

    elif effect in {
        "DESTROY",
        "EXILE",
    }:

        spec["target"] = random.choice([
            "CREATURE",
            "CREATURE_OPPONENT",
            "PERMANENT",
            "NONLAND_PERMANENT",
            "ARTIFACT_OR_ENCHANTMENT",
        ])

    elif effect == "SACRIFICE":

        spec["target"] = random.choice([
            "OPPONENT",
            "EACH_OPPONENT",
            "CREATURE_YOU_CONTROL",
        ])

    # ========================================================
    # MOVE ZONES
    # ========================================================

    elif effect == "RETURN_HAND":

        spec["target"] = random.choice([
            "CREATURE",
            "PERMANENT",
            "NONLAND_PERMANENT",
        ])

    elif effect == "PUT_BATTLEFIELD":

        spec["target"] = "LIBRARY_CARD"

    elif effect == "REANIMATE":

        spec["target"] = "GRAVEYARD_CREATURE"

    elif effect == "SEARCH_LIBRARY":

        spec["target"] = "LIBRARY_CARD"

    elif effect == "SEARCH_TO_HAND":

        spec["target"] = "LIBRARY_CARD"

    # ========================================================
    # BUFF
    # ========================================================

    elif effect == "TEMP_BUFF":

        spec["target"] = random.choice([
            "SELF",
            "CREATURE",
            "CREATURE_YOU_CONTROL",
            "CREATURES_YOU_CONTROL",
        ])

        spec["duration"] = "UNTIL_EOT"

        value = random.randint(1, 4)

        spec["amount"] = f"N_{value}"
        spec["amount_value"] = value

        spec["p"] = value
        spec["t"] = value

    elif effect == "PLUS1_COUNTER":

        spec["target"] = random.choice([
            "SELF",
            "CREATURE",
            "CREATURE_YOU_CONTROL",
        ])

        spec["duration"] = "PERMANENT"

        value = random.randint(1, 3)

        spec["amount"] = f"N_{value}"
        spec["amount_value"] = value

        spec["p"] = 1
        spec["t"] = 1

    elif effect == "GRANT_KEYWORD":

        spec["target"] = random.choice([
            "SELF",
            "CREATURE",
            "CREATURE_YOU_CONTROL",
            "CREATURES_YOU_CONTROL",
        ])

        spec["duration"] = random.choice([
            "UNTIL_EOT",
            "PERMANENT",
        ])

        spec["keyword"] = random.choice([
            "FLYING",
            "TRAMPLE",
            "VIGILANCE",
            "LIFELINK",
            "HEXPROOF",
            "INDESTRUCTIBLE",
            "HASTE",
            "MENACE",
            "DEATHTOUCH",
        ])

    # ========================================================
    # TOKEN
    # ========================================================

    elif effect == "CREATE_TOKEN":

        spec["amount"] = random.choice([
            "N_1",
            "N_2",
            "N_3",
        ])

        spec["amount_value"] = int(
            spec["amount"].split("_")[1]
        )

    # ========================================================
    # PREVENT / TAP
    # ========================================================

    elif effect == "PREVENT_DAMAGE":

        spec.update(random_fixed_amount())

    elif effect == "TAP":

        spec["target"] = random.choice([
            "CREATURE",
            "CREATURE_OPPONENT",
            "PERMANENT",
        ])

    # ========================================================
    # MANA
    # ========================================================

    elif effect == "ADD_MANA":

        spec.update(
            random_fixed_amount(
                min_value=1,
                max_value=3,
            )
        )

    # ========================================================
    # TURN
    # ========================================================

    elif effect == "EXTRA_TURN":

        spec["duration"] = "EXTRA_TURN"

    return spec

def normalize_candidate_spec(
    spec: Mapping[str, Any],
) -> dict[str, Any]:

    spec = deepcopy(dict(spec))

    effect = spec.get("effect")

    if effect is None:
        return spec

    # ========================================================
    # 1. 真正没有 target semantic slot 的 effects
    # ========================================================

    NO_TARGET_EFFECTS = {
        "DRAW",
        "SCRY",
        "CREATE_TOKEN",
        "ADD_MANA",
        "EXTRA_TURN",
    }

    if effect in NO_TARGET_EFFECTS:
        spec.pop("target", None)

    # ========================================================
    # 2. COUNTER_SPELL
    # target 固定为 SPELL
    # ========================================================

    if effect == "COUNTER_SPELL":
        spec["target"] = "SPELL"

    # ========================================================
    # 3. Search family
    # ========================================================

    if effect in {
        "SEARCH_LIBRARY",
        "SEARCH_TO_HAND",
        "PUT_BATTLEFIELD",
    }:
        spec["target"] = "LIBRARY_CARD"

    # ========================================================
    # 4. Reanimate
    # ========================================================

    if effect == "REANIMATE":
        spec["target"] = "GRAVEYARD_CREATURE"

    # ========================================================
    # 5. DAMAGE_EACH
    # 不要静默改变已有语义
    # ========================================================

    if effect == "DAMAGE_EACH":

        valid_targets = {
            "EACH_CREATURE",
            "ALL_CREATURES",
            "EACH_OPPONENT",
            "CREATURES_YOU_CONTROL",
        }

        target = spec.get("target")

        # 只有完全缺失时才补默认值
        if target is None:
            spec["target"] = "EACH_CREATURE"

        # 有值但是非法，直接报错
        elif target not in valid_targets:
            raise ValueError(
                f"Invalid target {target!r} "
                f"for DAMAGE_EACH: {spec}"
            )

    # ========================================================
    # 6. TEMP_BUFF
    # ========================================================

    if effect == "TEMP_BUFF":
        if "duration" not in spec:
            spec["duration"] = "UNTIL_EOT"

    # ========================================================
    # 7. PLUS1_COUNTER
    # ========================================================

    if effect == "PLUS1_COUNTER":
        spec["duration"] = "PERMANENT"

    # ========================================================
    # 8. EXTRA_TURN
    # ========================================================

    if effect == "EXTRA_TURN":

        # 我更建议不要强制 duration=EXTRA_TURN
        # effect 本身已经表达 extra turn

        spec.pop("duration", None)

        for key in [
            "target",
            "amount",
            "amount_value",
            "p",
            "t",
            "keyword",
        ]:
            spec.pop(key, None)

    # ========================================================
    # 9. keyword
    # ========================================================

    if effect != "GRANT_KEYWORD":
        spec.pop("keyword", None)

    # ========================================================
    # 10. p / t
    # ========================================================

    if effect != "TEMP_BUFF":
        spec.pop("p", None)
        spec.pop("t", None)

    # ========================================================
    # 11. amount consistency
    # ========================================================

    amount_value = spec.get(
        "amount_value"
    )

    if isinstance(amount_value, int):

        if 1 <= amount_value <= 5:

            spec["amount"] = (
                f"N_{amount_value}"
            )

        elif spec.get("amount") in {
            "N_1",
            "N_2",
            "N_3",
            "N_4",
            "N_5",
        }:

            spec["amount"] = "FIXED"

    return spec


PLACEHOLDER_RE = re.compile(
    r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}"
)


# ============================================================
# 1. 从 candidate templates 自动判断需要哪些 slot
# ============================================================

def get_required_candidate_slots(
    effect: str,
    libraries,
) -> set[str]:
    """
    根据 effects.candidate_render 中的 templates
    自动得到这个 effect 渲染时需要的 slot。

    例如：

    LOSE_LIFE:
        "{target} loses {amount} life"
        -> {"target", "amount"}

    STAT_EQUAL_DAMAGE:
        "Deal damage equal to {stat} to {target}"
        -> {"stat", "target"}

    DRAW:
        "Draw {amount} cards"
        -> {"amount"}
    """

    effect_configs = (
        libraries["effects"]
        ["candidate_render"]
    )

    if effect not in effect_configs:
        raise ValueError(
            f"Unknown candidate effect: {effect}"
        )

    config = effect_configs[effect]

    templates = config.get(
        "templates",
        [],
    )

    if not templates:
        raise ValueError(
            f"No candidate templates for effect: {effect}"
        )

    slots = set()

    for template in templates:
        slots.update(
            PLACEHOLDER_RE.findall(
                template
            )
        )

    # 如果 JSON 里已经手动写了 required_slots，
    # 也一起算进去。
    #
    # 这样 ADD_MANA 现在的
    # required_slots = ["amount", "color"]
    # 仍然有效。
    slots.update(
        config.get(
            "required_slots",
            []
        )
    )

    return slots


# ============================================================
# 2. 判断一个 slot 在 spec 里是否真的存在
# ============================================================

def candidate_slot_exists(
    spec: Mapping[str, Any],
    slot: str,
) -> bool:

    # amount 可以由 amount 或 amount_value 表示
    if slot == "amount":
        return (
            spec.get("amount") is not None
            or
            spec.get("amount_value") is not None
        )

    # keyword 兼容你 parser 以前的 static 字段
    if slot == "keyword":
        return (
            spec.get("keyword") is not None
            or
            spec.get("static") is not None
        )

    return spec.get(slot) is not None


# ============================================================
# 3. 对 parsed binding 做保守的 canonicalize
# ============================================================

def prepare_candidate_binding(
    binding: Mapping[str, Any],
    card: Mapping[str, Any] = None,
) -> dict[str, Any]:
    """
    这里只做确定性的字段统一。
    不凭空猜语义。
    """

    if not isinstance(
        binding,
        Mapping,
    ):
        raise TypeError(
            f"binding must be Mapping, "
            f"got {type(binding)}"
        )

    spec = deepcopy(
        dict(binding)
    )

    # --------------------------------------------------------
    # static -> keyword
    # --------------------------------------------------------

    if (
        spec.get("effect")
        == "GRANT_KEYWORD"
    ):
        if (
            spec.get("keyword") is None
            and
            spec.get("static") is not None
        ):
            spec["keyword"] = (
                spec.pop("static")
            )

        # 有些 parser 把 keyword 放到了 card["statics"]
        # 如果而且只有一个 static，可以安全恢复。
        if (
            spec.get("keyword") is None
            and
            card is not None
        ):
            statics = card.get(
                "statics",
                [],
            )

            if len(statics) == 1:
                spec["keyword"] = (
                    statics[0]
                )

    # --------------------------------------------------------
    # STAT_EQUAL_DAMAGE
    #
    # 如果 parser 已经给了 amount=EQUAL_POWER /
    # EQUAL_TOUGHNESS，可以确定性转成 stat。
    # 如果完全没信息，就不猜。
    # --------------------------------------------------------

    if (
        spec.get("effect")
        == "STAT_EQUAL_DAMAGE"
        and
        spec.get("stat") is None
    ):
        amount_type = spec.get(
            "amount"
        )

        stat_map = {
            "EQUAL_POWER":
                "its power",

            "EQUAL_TOUGHNESS":
                "its toughness",

            "EQUAL_LIFE":
                "your life total",
        }

        if amount_type in stat_map:
            spec["stat"] = (
                stat_map[amount_type]
            )

    # --------------------------------------------------------
    # 你原来的 normalize
    # --------------------------------------------------------

    spec = normalize_candidate_spec(
        spec
    )

    return spec


# ============================================================
# 4. validate
# ============================================================

def validate_candidate_spec(
    spec: dict[str, Any],
    libraries,
) -> None:
    """
    不合法直接 raise。

    这里的 invariant 是：

        validate_candidate_spec(spec)
        没有抛异常
        =>
        spec 至少具备 candidate renderer
        所要求的所有字段。
    """

    effect = spec.get(
        "effect"
    )

    if effect is None:
        raise ValueError(
            f"Missing effect: {spec}"
        )

    effect_configs = (
        libraries["effects"]
        ["candidate_render"]
    )

    if effect not in effect_configs:
        raise ValueError(
            f"Unknown effect: "
            f"{effect!r}"
        )

    # --------------------------------------------------------
    # 自动根据 templates 判断 required slots
    # --------------------------------------------------------

    required_slots = (
        get_required_candidate_slots(
            effect,
            libraries,
        )
    )

    missing = []

    for slot in required_slots:

        if not candidate_slot_exists(
            spec,
            slot,
        ):
            missing.append(
                slot
            )

    if missing:
        raise ValueError(
            f"Incomplete candidate spec: "
            f"effect={effect}, "
            f"missing={sorted(missing)}, "
            f"spec={spec}"
        )

    # --------------------------------------------------------
    # target 必须存在于 target taxonomy
    # --------------------------------------------------------

    target = spec.get(
        "target"
    )

    if target is not None:

        target_types = (
            libraries["targets"]
            ["types"]
        )

        if target not in target_types:
            raise ValueError(
                f"Unknown target "
                f"{target!r} "
                f"for effect={effect}"
            )

    # --------------------------------------------------------
    # duration
    # --------------------------------------------------------

    duration = spec.get(
        "duration"
    )

    if duration is not None:

        duration_types = (
            libraries["durations"]
            ["types"]
        )

        if duration not in duration_types:
            raise ValueError(
                f"Unknown duration "
                f"{duration!r} "
                f"for effect={effect}"
            )

    # --------------------------------------------------------
    # keyword
    # --------------------------------------------------------

    keyword = (
        spec.get("keyword")
        or
        spec.get("static")
    )

    if keyword is not None:

        static_types = (
            libraries["statics"]
            ["types"]
        )

        if keyword not in static_types:
            raise ValueError(
                f"Unknown keyword "
                f"{keyword!r} "
                f"for effect={effect}"
            )

    # --------------------------------------------------------
    # amount taxonomy
    # --------------------------------------------------------

    amount = spec.get(
        "amount"
    )

    if amount is not None:

        amount_types = (
            libraries["amounts"]
            ["types"]
        )

        if amount not in amount_types:
            raise ValueError(
                f"Unknown amount "
                f"{amount!r} "
                f"for effect={effect}"
            )

    # --------------------------------------------------------
    # p / t
    # --------------------------------------------------------

    if "p" in required_slots:
        if not isinstance(
            spec.get("p"),
            int,
        ):
            raise ValueError(
                f"p must be int: {spec}"
            )

    if "t" in required_slots:
        if not isinstance(
            spec.get("t"),
            int,
        ):
            raise ValueError(
                f"t must be int: {spec}"
            )

    # --------------------------------------------------------
    # ADD_MANA color
    # --------------------------------------------------------

    if "color" in required_slots:

        valid_colors = {
            "white",
            "blue",
            "black",
            "red",
            "green",
            "colorless",
        }

        color = spec.get(
            "color"
        )

        if color not in valid_colors:
            raise ValueError(
                f"Invalid mana color "
                f"{color!r}: {spec}"
            )


# ============================================================
# 5. 从 parsed cards 建立真正合法的 binding pool
# ============================================================

def build_valid_binding_pool(
    cards,
    libraries,
) -> list[dict[str, Any]]:
    """
    cards:
        parsed_cards.jsonl 读出来的 card list

    这里只留下：
        1. 有 effect
        2. normalize 后完整
        3. candidate renderer 所需 slot 全部存在
        4. taxonomy 合法

    的 bindings。
    """

    pool = []

    rejected = []

    for card in cards:

        bindings = card.get(
            "bindings",
            [],
        )

        for binding_idx, binding in enumerate(
            bindings
        ):

            if not isinstance(
                binding,
                Mapping,
            ):
                continue

            if not binding.get(
                "effect"
            ):
                continue

            try:
                spec = prepare_candidate_binding(
                    binding,
                    card=card,
                )

                validate_candidate_spec(
                    spec,
                    libraries,
                )

            except (
                ValueError,
                KeyError,
                TypeError,
            ) as exc:

                rejected.append({
                    "card_id":
                        card.get("card_id"),

                    "binding_idx":
                        binding_idx,

                    "binding":
                        deepcopy(binding),

                    "reason":
                        str(exc),
                })

                continue

            pool.append(
                spec
            )

    return pool


# ============================================================
# 6. 随机生成一个 binding
# ============================================================

def generate_random_binding(
    valid_binding_pool,
    libraries,
) -> dict[str, Any]:
    """
    不再随机 effect 然后猜 slots。

    直接从已经验证过的真实 binding pool 中抽。
    """

    if not valid_binding_pool:
        raise ValueError(
            "valid_binding_pool is empty"
        )

    spec = deepcopy(
        random.choice(
            valid_binding_pool
        )
    )

    # 理论上 pool 中都 valid，
    # 这里再做最后一道 invariant 检查。
    validate_candidate_spec(
        spec,
        libraries,
    )

    return spec




def get_random_bindings(
    valid_binding_pool,
    libraries,
    min_bindings: int = 1,
    max_bindings: int = 3,
    unique_effects: bool = True,
) -> list[dict[str, Any]]:

    if not valid_binding_pool:
        raise ValueError(
            "valid_binding_pool is empty"
        )

    if min_bindings < 1:
        raise ValueError(
            "min_bindings must be >= 1"
        )

    if max_bindings < min_bindings:
        raise ValueError(
            "max_bindings must be >= "
            "min_bindings"
        )

    n = random.randint(
        min_bindings,
        max_bindings,
    )

    # --------------------------------------------------------
    # 不要求 effect 唯一
    # --------------------------------------------------------

    if not unique_effects:

        return [
            generate_random_binding(
                valid_binding_pool,
                libraries,
            )
            for _ in range(n)
        ]

    # --------------------------------------------------------
    # 默认：一张随机卡里尽量不要重复 effect
    # --------------------------------------------------------

    by_effect = {}

    for spec in valid_binding_pool:

        effect = spec.get(
            "effect"
        )

        if effect is None:
            continue

        by_effect.setdefault(
            effect,
            []
        ).append(
            spec
        )

    effects = list(
        by_effect.keys()
    )

    if not effects:
        raise ValueError(
            "No valid effects in "
            "valid_binding_pool"
        )

    n = min(
        n,
        len(effects),
    )

    chosen_effects = random.sample(
        effects,
        k=n,
    )

    result = []

    for effect in chosen_effects:

        spec = deepcopy(
            random.choice(
                by_effect[effect]
            )
        )

        validate_candidate_spec(
            spec,
            libraries,
        )

        result.append(
            spec
        )

    return result