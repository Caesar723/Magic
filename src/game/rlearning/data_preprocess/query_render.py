"""Query-side wording for CREATE_TOKEN constraints; it is separate from candidate rendering."""


def _join_text(parts) -> str:
    if len(parts) < 2:
        return "".join(parts)
    if len(parts) == 2:
        return " and ".join(parts)
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def _keywords(keywords, libraries) -> str:
    types = libraries["statics"]["types"]
    return _join_text([types[keyword]["label"].casefold() for keyword in keywords])


def _count_text(spec, libraries):
    value = spec.get("amount_value")
    if not isinstance(value, int):
        value = libraries["amounts"]["types"].get(spec.get("amount"), {}).get("value")
    if value == 1:
        return "a"
    if isinstance(value, int):
        return str(value)
    if spec.get("amount") == "VARIABLE_X":
        return "X"
    return None


def _token_phrase(profile, libraries) -> str:
    count = profile.get("count")
    prefix = "a" if count == 1 else str(count) if isinstance(count, int) else ""
    noun = "creature token" if count == 1 else "creature tokens"
    text = " ".join(part for part in (prefix, noun) if part)
    if "token_power" in profile and "token_toughness" in profile:
        text = text.replace(noun, f"{profile['token_power']}/{profile['token_toughness']} {noun}")
    elif "token_power" in profile:
        text += f" with base power {profile['token_power']}"
    elif "token_toughness" in profile:
        text += f" with base toughness {profile['token_toughness']}"
    if profile.get("token_keywords"):
        text += f" with {_keywords(profile['token_keywords'], libraries)}" if " with " not in text else f" and {_keywords(profile['token_keywords'], libraries)}"
    return text


def render_create_token_query(spec, libraries) -> str:
    """Render every CREATE_TOKEN constraint present in a query spec, without filling gaps."""
    config = libraries["query_templates"]["create_token_render"]
    if variants := spec.get("token_variants"):
        return f"{config['prefix']} {_join_text([_token_phrase(variant, libraries) for variant in variants])}"

    count = _count_text(spec, libraries)
    if spec.get("amount") == "EQUAL_COUNT":
        phrase = config["equal_count"]
    elif spec.get("amount") == "FIXED" and count is None:
        phrase = config["fixed_unknown"]
    else:
        phrase = " ".join(part for part in (count, "creature tokens") if part) or config["unknown"]
        if count == "a":
            phrase = phrase.replace("creature tokens", "creature token")
    if "token_power" in spec and "token_toughness" in spec:
        phrase = phrase.replace("creature", f"{spec['token_power']}/{spec['token_toughness']} creature", 1)
    elif "token_power" in spec:
        phrase += f" with base power {spec['token_power']}"
    elif "token_toughness" in spec:
        phrase += f" with base toughness {spec['token_toughness']}"
    if spec.get("token_keywords"):
        phrase += f" with {_keywords(spec['token_keywords'], libraries)}" if " with " not in phrase else f" and {_keywords(spec['token_keywords'], libraries)}"
    return f"{config['prefix']} {phrase}"


def render_query_card(bindings, libraries) -> str:
    """Use query wording for token constraints and keep the legacy renderer for other effects."""
    from spec_render import render_candidate_spec

    parts = [
        render_create_token_query(binding, libraries) if binding.get("effect") == "CREATE_TOKEN"
        else render_candidate_spec(binding, libraries)
        for binding in bindings
    ]
    return ". ".join(part.rstrip(".") for part in parts) + "."
