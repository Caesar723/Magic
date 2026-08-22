import random
from typing import Any, Mapping



def phrase_is_compatible(
    item: dict,
    spec: Mapping[str, Any],
) -> bool:

    phrase = item["phrase"]

    # =========================================
    # amount
    # =========================================

    amount_value = spec.get("amount_value")

    if amount_value is not None:

        # 数量不是 1：
        # 必须使用能够表达 amount 的模板
        if amount_value != 1:
            if "{amount}" not in phrase:
                return False

    # =========================================
    # token
    # =========================================

    # phrase 需要 token 信息，
    # 但 spec 没提供 token
    if "{token}" in phrase:
        if not spec.get("token"):
            return False

    # =========================================
    # p / t
    # =========================================

    if "{p}" in phrase:
        if spec.get("p") is None:
            return False

    if "{t}" in phrase:
        if spec.get("t") is None:
            return False

    # =========================================
    # keyword
    # =========================================

    if "{keyword}" in phrase:
        if not spec.get("keyword"):
            return False

    # =========================================
    # color
    # =========================================

    if "{color}" in phrase:
        if not spec.get("color"):
            return False

    return True

def pick_phrase(
    library,
    key,
    spec=None,
    style="oracle_template",
):
    items = library["phrases"][key]

    # 先筛 style
    pool = [
        item
        for item in items
        if item.get("style") == style
    ]

    if not pool:
        pool = items

    # 再根据 spec 筛兼容性
    if spec is not None:
        compatible = [
            item
            for item in pool
            if phrase_is_compatible(
                item,
                spec,
            )
        ]

        if compatible:
            pool = compatible

    if not pool:
        raise ValueError(
            f"No compatible phrase "
            f"for {key}: {spec}"
        )

    return random.choice(pool)



def fill_placeholders(
    text,
    spec,
    libraries,
):
    # amount
    if "{amount}" in text:
        amount_type = spec.get("amount")

        if spec.get("amount_value") is not None:
            amount = str(
                spec["amount_value"]
            )
        else:
            amount_item = pick_phrase(
                libraries["amounts"],
                amount_type,
            )
            amount = amount_item["phrase"]

        text = text.replace(
            "{amount}",
            amount,
        )

    # p / t
    text = text.replace(
        "{p}",
        str(spec.get("p", "")),
    )

    text = text.replace(
        "{t}",
        str(spec.get("t", "")),
    )

    # keyword
    if "{keyword}" in text:
        keyword = spec.get("keyword")

        keyword_item = pick_phrase(
            libraries["statics"],
            keyword,
        )

        text = text.replace(
            "{keyword}",
            keyword_item["phrase"],
        )

    # token
    text = text.replace(
        "{token}",
        str(spec.get("token", "")),
    )

    # color
    text = text.replace(
        "{color}",
        str(spec.get("color", "")),
    )

    # name
    text = text.replace(
        "{name}",
        str(
            spec.get(
                "name",
                "this permanent",
            )
        ),
    )

    return text


def render_candidate_spec(
    spec,
    libraries,
):
    parts = []

    # =================================
    # 1. Trigger
    # =================================

    trigger_type = spec.get("trigger")

    if trigger_type:
        trigger_item = pick_phrase(
            libraries["triggers"],
            trigger_type,
        )

        trigger = fill_placeholders(
            trigger_item["phrase"],
            spec,
            libraries,
        )

        parts.append(trigger)

    # =================================
    # 2. Effect
    # =================================

    effect_type = spec["effect"]

    effect_item = pick_phrase(
        libraries["effects"],
        effect_type,
        spec=spec,
    )

    effect = fill_placeholders(
        effect_item["phrase"],
        spec,
        libraries,
    )

    consumed = set(
        effect_item.get(
            "consumes",
            [],
        )
    )

    body = effect

    # =================================
    # 3. Target
    # effect 没吃掉 target 才追加
    # =================================

    target_type = spec.get("target")

    if (
        target_type
        and "target" not in consumed
    ):
        target_item = pick_phrase(
            libraries["targets"],
            target_type,
        )

        target = fill_placeholders(
            target_item["phrase"],
            spec,
            libraries,
        )

        body += f" to {target}"

    # =================================
    # 4. Duration
    # =================================

    duration_type = spec.get(
        "duration"
    )

    if (
        duration_type
        and "duration" not in consumed
    ):
        duration_item = pick_phrase(
            libraries["durations"],
            duration_type,
        )

        duration = fill_placeholders(
            duration_item["phrase"],
            spec,
            libraries,
        )

        body += f" {duration}"

    # =================================
    # 5. Trigger + body
    # =================================

    if parts:
        text = (
            f"{parts[0]}, "
            f"{body}"
        )
    else:
        text = body

    text = text.strip()

    if not text.endswith("."):
        text += "."

    return (
        text[0].upper()
        + text[1:]
    )