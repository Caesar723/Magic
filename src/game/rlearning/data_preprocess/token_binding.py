"""Conservative CREATE_TOKEN semantic extraction from raw card ability text."""

import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


LIB_DIR = Path(__file__).resolve().parents[1] / "data/retrieval/libraries"
TOKEN_FIELDS = ("token_power", "token_toughness", "token_keywords", "token_variants")
NUMBER_WORDS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}
CREATE_RE = re.compile(r"\b(?:create|summon)\b", re.IGNORECASE)
COUNT_REF_RE = re.compile(r"\bfor\s+(?:each|every)\b", re.IGNORECASE)
DIFFERENT_ABILITY_RE = re.compile(
    r"\beach\s+with\s+(?:a\s+)?different\s+abilit(?:y|ies)\s*\(([^)]*)\)", re.IGNORECASE
)
TOKEN_RE = re.compile(
    r"\b(?:(?P<count>x|a|an|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+)?"
    r"(?:(?P<power>\d+)\s*/\s*(?P<toughness>\d+)\s+)?"
    r"(?:[a-z][a-z'’-]*\s+){0,6}?tokens?\b",
    re.IGNORECASE,
)


def _load_keyword_phrases() -> dict[str, tuple[str, ...]]:
    types = json.loads((LIB_DIR / "statics.json").read_text(encoding="utf-8"))["types"]
    phrases = {key: (config["label"].casefold(),) for key, config in types.items()}
    phrases["CANNOT_ATTACK"] += ("can't attack",)
    return phrases


KEYWORD_PHRASES = _load_keyword_phrases()


def _parse_count(value: str | None) -> int | str | None:
    """Return a concrete count, X, or None when the text gives no count."""
    if value is None:
        return None
    if value.casefold() == "x":
        return "X"
    if value.isdigit():
        return int(value)
    return NUMBER_WORDS[value.casefold()]


def _find_keywords(text: str) -> list[str]:
    matches = []
    normalized = text.casefold()
    for keyword, phrases in KEYWORD_PHRASES.items():
        for phrase in phrases:
            match = re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", normalized)
            if match:
                matches.append((match.start(), keyword))
                break
    return [keyword for _, keyword in sorted(matches)]


def _amount_fields(context: str, descriptors: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if COUNT_REF_RE.search(context):
        return {"amount": "EQUAL_COUNT"}

    counts = [descriptor["count"] for descriptor in descriptors]
    if "X" in counts:
        return {"amount": "VARIABLE_X"}
    if not counts or any(not isinstance(count, int) for count in counts):
        return {}

    total = sum(counts)
    return {"amount": f"N_{total}" if 1 <= total <= 5 else "FIXED", "amount_value": total}


def _parse_descriptors(text: str) -> list[dict[str, Any]]:
    matches = list(TOKEN_RE.finditer(text))
    descriptors = []
    for index, match in enumerate(matches):
        tail_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        descriptor = {"count": _parse_count(match.group("count"))}
        if match.group("power") is not None:
            descriptor["token_power"] = int(match.group("power"))
            descriptor["token_toughness"] = int(match.group("toughness"))
        if keywords := _find_keywords(text[match.end():tail_end]):
            descriptor["token_keywords"] = keywords
        descriptors.append(descriptor)
    return descriptors


def _descriptor_fields(descriptor: Mapping[str, Any]) -> dict[str, Any]:
    return {field: descriptor[field] for field in TOKEN_FIELDS[:-1] if field in descriptor}


def _profile_key(descriptor: Mapping[str, Any]) -> tuple[Any, ...]:
    fields = _descriptor_fields(descriptor)
    return fields.get("token_power"), fields.get("token_toughness"), tuple(fields.get("token_keywords", []))


def _group_variants(descriptors: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for descriptor in descriptors:
        key = (
            descriptor.get("token_power"), descriptor.get("token_toughness"),
            tuple(descriptor.get("token_keywords", [])),
        )
        if key not in grouped:
            grouped[key] = {"count": 0, **_descriptor_fields(descriptor)}
        grouped[key]["count"] += descriptor["count"]
    return list(grouped.values())


def _different_ability_variants(
    context: str, descriptor: Mapping[str, Any], amount: Mapping[str, Any]
) -> list[dict[str, Any]] | None:
    match = DIFFERENT_ABILITY_RE.search(context)
    if not match:
        return None

    keywords = _find_keywords(match.group(1))
    amount_value = amount.get("amount_value")
    if not keywords or not isinstance(amount_value, int) or len(keywords) != amount_value:
        raise ValueError("Different token abilities must match the explicit token count")
    return [{"count": 1, **_descriptor_fields(descriptor), "token_keywords": [keyword]} for keyword in keywords]


def _parse_creation(context: str, descriptor_text: str) -> dict[str, Any]:
    descriptors = _parse_descriptors(descriptor_text)
    if not descriptors:
        return {"effect": "CREATE_TOKEN"}

    amount = _amount_fields(context, descriptors)
    binding = {"effect": "CREATE_TOKEN", **amount}
    variants = _different_ability_variants(context, descriptors[0], amount)
    if variants is not None:
        binding["token_variants"] = variants
        return binding

    profiles = {_profile_key(descriptor) for descriptor in descriptors}
    if len(descriptors) == 1 or len(profiles) == 1:
        binding.update(_descriptor_fields(descriptors[0]))
        return binding

    if all(isinstance(descriptor["count"], int) for descriptor in descriptors):
        variants = _group_variants(descriptors)
        amount_value = binding.get("amount_value")
        if isinstance(amount_value, int) and sum(variant["count"] for variant in variants) != amount_value:
            raise ValueError("Token variant counts do not match amount_value")
        binding["token_variants"] = variants
    return binding


def extract_create_token_bindings(text: str) -> list[dict[str, Any]]:
    """Return one binding per create/summon token event without inventing unknown values."""
    matches = list(CREATE_RE.finditer(text))
    bindings = []
    for index, match in enumerate(matches):
        next_event = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sentence_end = re.search(r"[.;]", text[match.end():])
        end = min(next_event, match.end() + sentence_end.start() if sentence_end else len(text))
        descriptor_text = text[match.end():end]
        if not re.search(r"\btokens?\b", descriptor_text, re.IGNORECASE):
            continue
        sentence_start = max(text.rfind(".", 0, match.start()), text.rfind(";", 0, match.start())) + 1
        bindings.append(_parse_creation(text[sentence_start:end], descriptor_text))
    return bindings


def extract_create_token_binding(text: str) -> dict[str, Any]:
    """Extract exactly one token event, raising when a caller supplied ambiguous input."""
    bindings = extract_create_token_bindings(text)
    if len(bindings) != 1:
        raise ValueError(f"Expected one token creation event, found {len(bindings)}")
    return bindings[0]


def merge_create_token_bindings(
    bindings: Sequence[Mapping[str, Any]], ability: str
) -> tuple[list[dict[str, Any]], int]:
    """Replace only CREATE_TOKEN bindings, preserving old trigger and non-token semantics."""
    extracted = extract_create_token_bindings(ability)
    details = iter(extracted)
    merged, replaced = [], 0
    for binding in bindings:
        updated = dict(binding)
        if updated.get("effect") == "CREATE_TOKEN":
            try:
                updated.update(next(details))
                replaced += 1
            except StopIteration:
                pass
        merged.append(updated)
    merged.extend(details)
    return merged, replaced
