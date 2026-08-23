import random
from typing import Any, Mapping


def render_candidate_duration(
    body,
    duration_type,
    libraries,
):
    """按 duration 配置为候选文本追加可安全渲染的时限描述。"""
    if not duration_type:
        return body

    config = libraries["durations"]["candidate_render"][duration_type]

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

    raise ValueError(f"Unknown duration mode: {mode}")


def fill_candidate_placeholders(
    text,
    spec,
    libraries,
):
    """用 spec 填充候选模板，并校验模板实际使用的字段。"""
    if "{target}" in text:
        target_type = spec.get("target")
        if target_type is None:
            raise ValueError(f"Missing target: {spec}")
        target_config = libraries["targets"]["candidate_render"][target_type]
        phrases = target_config["phrases"] if isinstance(target_config, dict) else target_config
        text = text.replace("{target}", random.choice(phrases))

    if "{amount}" in text:
        text = text.replace("{amount}", render_candidate_amount(spec, libraries))
        amount = spec.get("amount_value")
        if amount is None:
            amount = libraries["amounts"]["types"].get(spec.get("amount"), {}).get("value")

        if amount == 1:
            for plural, singular in (
                ("tokens", "token"),
                ("cards", "card"),
                ("counters", "counter"),
                ("points", "point"),
                ("that are", "that is"),
            ):
                text = text.replace(plural, singular)

    for field in ("p", "t"):
        placeholder = f"{{{field}}}"
        if placeholder in text:
            value = spec.get(field)
            if value is None:
                raise ValueError(f"Missing {field}: {spec}")
            text = text.replace(placeholder, format_signed(value))

    if "{stat}" in text:
        stat = {
            "EQUAL_POWER": "its power",
            "EQUAL_TOUGHNESS": "its toughness",
        }.get(spec.get("amount"))
        if stat is None:
            raise ValueError(f"Missing stat selector: {spec}")
        text = text.replace("{stat}", stat)

    if "{keyword}" in text:
        keyword_type = spec.get("keyword")
        if keyword_type is None:
            raise ValueError(f"Missing keyword: {spec}")
        text = text.replace("{keyword}", pick_phrase(libraries["statics"], keyword_type)["phrase"])

    for field in ("token", "color"):
        placeholder = f"{{{field}}}"
        if placeholder in text:
            value = spec.get(field)
            if value is None:
                raise ValueError(f"Missing {field}: {spec}")
            text = text.replace(placeholder, str(value))

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
    amount_value = spec.get("amount_value")
    if amount_value is not None and amount_value != 1 and "{amount}" not in phrase:
        return False
    if any(
        f"{{{field}}}" in phrase and not spec.get(field) for field in ("token", "keyword", "color")
    ):
        return False
    return all(f"{{{field}}}" not in phrase or spec.get(field) is not None for field in ("p", "t"))


def pick_phrase(
    library,
    key,
    spec=None,
    style="oracle_template",
):
    items = library["phrases"][key]
    pool = [item for item in items if item.get("style") == style] or items
    if spec is not None:
        pool = [item for item in pool if phrase_is_compatible(item, spec)] or pool
    if not pool:
        raise ValueError(f"No compatible phrase for {key}: {spec}")
    return random.choice(pool)


def fill_placeholders(
    text,
    spec,
    libraries,
):
    if "{amount}" in text:
        amount_type = spec.get("amount")
        amount = (
            str(spec["amount_value"])
            if spec.get("amount_value") is not None
            else pick_phrase(libraries["amounts"], amount_type)["phrase"]
        )
        text = text.replace("{amount}", amount)

    for field in ("p", "t"):
        placeholder = f"{{{field}}}"
        if placeholder in text:
            value = spec.get(field)
            if value is None:
                raise ValueError(f"Missing {field}: {spec}")
            text = text.replace(placeholder, format_signed(value))

    if "{keyword}" in text:
        text = text.replace(
            "{keyword}", pick_phrase(libraries["statics"], spec.get("keyword"))["phrase"]
        )

    text = text.replace("{token}", str(spec.get("token", "")))
    text = text.replace("{color}", str(spec.get("color", "")))
    text = text.replace("{name}", str(spec.get("name", "this permanent")))
    return text


def render_candidate_amount(
    spec: dict,
    libraries,
) -> str:
    """将 amount 配置渲染为候选文本，必要时使用库中的固定值。"""
    amount_type = spec.get("amount")
    amount_value = spec.get("amount_value")

    if amount_type is None:
        raise ValueError(f"Missing amount: {spec}")

    amount_types = libraries["amounts"]["types"]
    if amount_type not in amount_types:
        raise ValueError(f"Unknown amount type {amount_type!r}: {spec}")
    amount_config = amount_types[amount_type]
    if amount_value is None:
        amount_value = amount_config.get("value")

    render_config = libraries["amounts"].get("candidate_render", {}).get(amount_type)

    if render_config is not None:
        templates = render_config.get("templates")
        if templates is None:
            text = render_config.get("text")
            templates = [text] if text else []
        if templates:
            text = random.choice(templates)
            if amount_value is None and ("{n}" in text or "{word_n}" in text):
                raise ValueError(f"Amount template requires amount_value: {spec}")
            if amount_value is not None:
                text = text.replace("{n}", str(amount_value))
                text = text.replace("{word_n}", number_to_words(amount_value))

            for field in ("p", "t"):
                placeholder = f"{{{field}}}"
                if placeholder in text:
                    value = spec.get(field)
                    if value is None:
                        raise ValueError(f"Missing {field}: {spec}")
                    text = text.replace(placeholder, format_signed(value))
            return text

    if amount_type == "FIXED":
        raise ValueError(f"FIXED amount requires amount_value: {spec}")

    raise ValueError(f"No candidate rendering for amount={amount_type!r}: {spec}")


def render_candidate_spec(
    spec,
    libraries,
):
    """把一个规范化 binding 渲染成完整的候选规则句。"""
    trigger = None
    if trigger_type := spec.get("trigger"):
        trigger_config = libraries["triggers"]["candidate_render"][trigger_type]
        if trigger_config.get("mode") == "omit":
            pass
        else:
            trigger_template = random.choice(trigger_config["templates"])
            trigger = fill_placeholders(trigger_template, spec, libraries)

    config = libraries["effects"]["candidate_render"][spec["effect"]]
    templates = config.get("templates_by_target", {}).get(spec.get("target"), config["templates"])
    body = fill_candidate_placeholders(random.choice(templates), spec, libraries)
    body = render_candidate_duration(body, spec.get("duration"), libraries)

    if trigger:
        body = body[0].lower() + body[1:]
        text = f"{trigger}, {body}"
    else:
        text = body
    text = text.strip()
    if not text.endswith("."):
        text += "."
    return text[0].upper() + text[1:]


def render_candidate_card(
    bindings,
    libraries,
    shuffle=False,
):
    """把多个 binding 拼成一段卡牌规则文本。"""
    bindings = list(bindings)
    if shuffle:
        random.shuffle(bindings)
    rendered_parts = [render_candidate_spec(binding, libraries).rstrip(".") for binding in bindings]
    return ". ".join(rendered_parts) + "."
