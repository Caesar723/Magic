import random
from typing import Any, Mapping


def render_candidate_duration(
    body,
    duration_type,
    libraries,
):
    if not duration_type:
        return body

    config = (
        libraries["durations"]
        ["candidate_render"]
        [duration_type]
    )

    mode = config["mode"]
    phrases = config.get("phrases", [])

    # PERMANENT / INSTANT / EXTRA_TURN 等
    if mode == "omit":
        return body

    if not phrases:
        return body

    phrase = random.choice(phrases)

    if mode == "suffix":
        return f"{body} {phrase}"

    if mode == "clause":
        body = body.rstrip(".")
        return f"{body}. {phrase}"

    # NEXT_END_STEP / NEXT_MAIN_PHASE
    # 暂时不要乱拼
    if mode == "delayed":
        return body

    raise ValueError(
        f"Unknown duration mode: {mode}"
    )

def fill_candidate_placeholders(
    text,
    spec,
    libraries,
):
    if "{target}" in text:
        target_type = spec.get("target")

        if target_type is None:
            raise ValueError(
                f"Missing target: {spec}"
            )

        target_config = (
            libraries["targets"]
            ["candidate_render"]
            [target_type]
        )

        if isinstance(target_config, dict):
            phrases = target_config["phrases"]
        else:
            phrases = target_config

        target = random.choice(phrases)

        text = text.replace(
            "{target}",
            target,
        )

    if "{amount}" in text:

        amount_text = (
            render_candidate_amount(
                spec,
                libraries,
            )
        )

        text = text.replace(
            "{amount}",
            amount_text,
        )

        amount = spec.get("amount_value")

        if amount is None:
            amount_config = (
                libraries["amounts"]
                ["types"]
                .get(spec.get("amount"), {})
            )
            amount = amount_config.get(
                "value"
            )

        if amount == 1:
            text = text.replace(
                "tokens",
                "token",
            )
            text = text.replace(
                "cards",
                "card",
            )
            text = text.replace(
                "counters",
                "counter",
            )
            text = text.replace(
                "points",
                "point",
            )
            text = text.replace(
                "that are",
                "that is",
            )

    # p / t
    if "{p}" in text:
        p = spec.get("p")

        if p is None:
            raise ValueError(
                f"Missing p: {spec}"
            )

        text = text.replace(
            "{p}",
            format_signed(p),
        )

    if "{t}" in text:
        t = spec.get("t")

        if t is None:
            raise ValueError(
                f"Missing t: {spec}"
            )

        text = text.replace(
            "{t}",
            format_signed(t),
        )

    if "{stat}" in text:
        amount_type = spec.get("amount")

        stat = {
            "EQUAL_POWER": "its power",
            "EQUAL_TOUGHNESS": "its toughness",
        }.get(amount_type)

        if stat is None:
            raise ValueError(
                f"Missing stat selector: {spec}"
            )

        text = text.replace(
            "{stat}",
            stat,
        )

    if "{keyword}" in text:
        keyword_type = spec.get("keyword")

        if keyword_type is None:
            raise ValueError(
                f"Missing keyword: {spec}"
            )

        keyword_item = pick_phrase(
            libraries["statics"],
            keyword_type,
        )

        text = text.replace(
            "{keyword}",
            keyword_item["phrase"],
        )

    if "{token}" in text:
        token = spec.get("token")

        if token is None:
            raise ValueError(
                f"Missing token: {spec}"
            )

        text = text.replace(
            "{token}",
            str(token),
        )

    if "{color}" in text:
        color = spec.get("color")

        if color is None:
            raise ValueError(
                f"Missing color: {spec}"
            )

        text = text.replace(
            "{color}",
            str(color),
        )

    return text

def format_signed(value: int) -> str:
    if value > 0:
        return f"+{value}"

    if value < 0:
        return str(value)

    return "0"


def number_to_words(value) -> str:
    """Render common integer amounts without leaving a placeholder behind."""

    if not isinstance(value, int) or isinstance(value, bool):
        return str(value)

    ones = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]

    if 0 <= value < len(ones):
        return ones[value]

    if value < 0:
        return f"negative {number_to_words(-value)}"

    tens = [
        "",
        "",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
    ]

    if value < 100:
        prefix = tens[value // 10]
        remainder = value % 10
        if remainder == 0:
            return prefix
        return f"{prefix}-{ones[remainder]}"

    if value < 1000:
        hundreds = f"{ones[value // 100]} hundred"
        remainder = value % 100
        if remainder == 0:
            return hundreds
        return f"{hundreds} {number_to_words(remainder)}"

    return str(value)

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
    if "{p}" in text:
        p = spec.get("p")

        if p is None:
            raise ValueError(
                f"Missing p: {spec}"
            )

        text = text.replace(
            "{p}",
            format_signed(p),
        )

    if "{t}" in text:
        t = spec.get("t")

        if t is None:
            raise ValueError(
                f"Missing t: {spec}"
            )

        text = text.replace(
            "{t}",
            format_signed(t),
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

def render_candidate_amount(
    spec: dict,
    libraries,
) -> str:

    amount_type = spec.get("amount")
    amount_value = spec.get(
        "amount_value"
    )

    if amount_type is None:
        raise ValueError(
            f"Missing amount: {spec}"
        )

    amount_types = (
        libraries["amounts"]["types"]
    )

    if amount_type not in amount_types:
        raise ValueError(
            f"Unknown amount type "
            f"{amount_type!r}: {spec}"
        )

    amount_config = (
        amount_types[amount_type]
    )

    # -----------------------------------------
    # N_1 ~ N_5 can carry their value in the
    # library even when the parser omitted it.
    # -----------------------------------------

    if amount_value is None:
        amount_value = amount_config.get(
            "value"
        )

    # -----------------------------------------
    # Candidate amount templates
    # -----------------------------------------

    candidate_render = (
        libraries["amounts"]
        .get(
            "candidate_render",
            {}
        )
    )

    render_config = (
        candidate_render.get(
            amount_type
        )
    )

    if render_config is not None:

        templates = render_config.get(
            "templates"
        )

        if templates is None:
            text = render_config.get(
                "text"
            )
            templates = (
                [text]
                if text
                else []
            )

        if templates:
            text = random.choice(
                templates
            )

            if amount_value is None and (
                "{n}" in text
                or "{word_n}" in text
            ):
                raise ValueError(
                    f"Amount template requires "
                    f"amount_value: {spec}"
                )

            if amount_value is not None:
                text = text.replace(
                    "{n}",
                    str(amount_value),
                )
                text = text.replace(
                    "{word_n}",
                    number_to_words(
                        amount_value
                    ),
                )

            if "{p}" in text:
                p = spec.get("p")
                if p is None:
                    raise ValueError(
                        f"Missing p: {spec}"
                    )
                text = text.replace(
                    "{p}",
                    format_signed(p),
                )

            if "{t}" in text:
                t = spec.get("t")
                if t is None:
                    raise ValueError(
                        f"Missing t: {spec}"
                    )
                text = text.replace(
                    "{t}",
                    format_signed(t),
                )

            return text

    # -----------------------------------------
    # FIXED 没数字不完整
    # -----------------------------------------

    if amount_type == "FIXED":
        raise ValueError(
            f"FIXED amount requires "
            f"amount_value: {spec}"
        )

    raise ValueError(
        f"No candidate rendering for "
        f"amount={amount_type!r}: {spec}"
    )

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
        trigger_config = (
            libraries["triggers"]
            ["candidate_render"]
            [trigger_type]
        )

        if trigger_config.get("mode") == "omit":
            trigger = None
        else:
            trigger_template = random.choice(
                trigger_config["templates"]
            )

            trigger = fill_placeholders(
                trigger_template,
                spec,
                libraries,
            )

        if trigger:
            parts.append(trigger)

    # =================================
    # 2. Effect
    # =================================

    effect_type = spec["effect"]

    config = (
        libraries["effects"]
        ["candidate_render"]
        [effect_type]
    )

    templates = config.get(
        "templates_by_target",
        {},
    ).get(
        spec.get("target"),
        config["templates"],
    )

    template = random.choice(
        templates
    )

    body = fill_candidate_placeholders(
        template,
        spec,
        libraries,
    )

    # =================================
    # 4. Duration
    # =================================

    body = render_candidate_duration(
        body,
        spec.get("duration"),
        libraries,
    )

    # =================================
    # 5. Trigger + body
    # =================================

    if parts:
        body = (
            body[0].lower()
            + body[1:]
        )
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

def render_candidate_card(
    bindings,
    libraries,
    shuffle=False,
):
    bindings = list(bindings)

    if shuffle:
        random.shuffle(bindings)

    rendered_parts = []

    for binding in bindings:
        text = render_candidate_spec(
            binding,
            libraries,
        )

        rendered_parts.append(
            text.rstrip(".")
        )

    return ". ".join(
        rendered_parts
    ) + "."
