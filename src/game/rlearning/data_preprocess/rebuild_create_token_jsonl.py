"""Rebuild CREATE_TOKEN bindings from source card Ability text without touching other effects."""

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

from token_binding import TOKEN_FIELDS, extract_create_token_bindings, merge_create_token_bindings


DATA_DIR = Path(__file__).resolve().parents[1] / "data/retrieval"
DEFAULT_JSONL = DATA_DIR / "parsed_cards.jsonl"


def _source_ability(card: dict[str, Any]) -> str:
    source_path = Path(card["path"])
    source = json.loads(source_path.read_text(encoding="utf-8"))
    ability = source.get("Ability")
    if not isinstance(ability, str):
        raise ValueError(f"Missing Ability in {source_path}")
    return ability


def rebuild_cards(parsed_path: Path = DEFAULT_JSONL) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Reparse raw Ability text for CREATE_TOKEN while retaining existing non-token bindings."""
    cards, unparsed = [], []
    for line in parsed_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        ability = _source_ability(card)
        extracted = extract_create_token_bindings(ability)
        card["ability"] = ability
        card["index_text"] = ability
        card["bindings"], _ = merge_create_token_bindings(card.get("bindings", []), ability)
        if extracted and any(
            not any(field in binding for field in ("amount", *TOKEN_FIELDS))
            for binding in card["bindings"] if binding.get("effect") == "CREATE_TOKEN"
        ):
            unparsed.append(card["card_id"])
        cards.append(card)

    token_bindings = [
        binding for card in cards for binding in card["bindings"] if binding.get("effect") == "CREATE_TOKEN"
    ]
    stats = {
        "cards": len(cards), "create_token_bindings": len(token_bindings),
        "with_amount": sum("amount" in binding for binding in token_bindings),
        "with_token_power_toughness": sum(
            "token_power" in binding and "token_toughness" in binding for binding in token_bindings
        ),
        "with_token_keywords": sum("token_keywords" in binding for binding in token_bindings),
        "with_token_variants": sum("token_variants" in binding for binding in token_bindings),
        "effect_only": sum(
            not any(field in binding for field in ("amount", *TOKEN_FIELDS)) for binding in token_bindings
        ),
        "unparsed_cards": unparsed,
    }
    return cards, stats


def write_cards(cards: list[dict[str, Any]], output_path: Path) -> None:
    """Atomically replace the JSONL only after every source card has parsed successfully."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output_path.parent, delete=False) as temp:
        temp_path = Path(temp.name)
        for card in cards:
            temp.write(json.dumps(card, ensure_ascii=False, separators=(",", ":")) + "\n")
    temp_path.replace(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_JSONL)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write", action="store_true", help="Replace --output or --input atomically.")
    args = parser.parse_args()

    cards, stats = rebuild_cards(args.input)
    if args.write:
        write_cards(cards, args.output or args.input)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
