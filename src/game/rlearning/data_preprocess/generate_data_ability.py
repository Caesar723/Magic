from typing import Any, Mapping
import json
import random
from pathlib import Path

from candidate import get_random_bindings,build_valid_binding_pool,generate_exact_spec, generate_near_spec, generate_hard_spec, generate_random_spec, normalize_candidate_spec, validate_candidate_spec
from similarity import compute_binding_relevance
from spec_render import render_candidate_card
from query_render import render_query_card


def load_library():
    LIB_DIR = Path(__file__).resolve().parents[1] / "data/retrieval/libraries"
    result={
        "triggers":json.loads((LIB_DIR / "triggers.json").read_text(encoding="utf-8")),
        "durations":json.loads((LIB_DIR / "durations.json").read_text(encoding="utf-8")),
        "statics":json.loads((LIB_DIR / "statics.json").read_text(encoding="utf-8")),
        "amounts":json.loads((LIB_DIR / "amounts.json").read_text(encoding="utf-8")),
        "effects":json.loads((LIB_DIR / "effects.json").read_text(encoding="utf-8")),
        "targets":json.loads((LIB_DIR / "targets.json").read_text(encoding="utf-8")),
        "query_templates":json.loads((LIB_DIR / "query_templates.json").read_text(encoding="utf-8")),
    }
    return result

import json


def load_cards() -> list[dict]:
    CARDS_DIR = Path(__file__).resolve().parents[1] / "data/retrieval"
    cards = []

    with open(CARDS_DIR / "parsed_cards.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            card = json.loads(line)

            cards.append(card)

    return cards





def get_binding_from_card(card: dict):
    return card["bindings"]


def build_candidate_group(bindings,library,n_exact=2,n_near=3,n_hard=2,n_random=1,card_info:dict=None,valid_binding_pool=None):
    
    query_message = render_query_card(bindings,library)
    result={
        "query_bindings":bindings,
        "query_message":query_message,
        "candidates":[],
    }
    if card_info is not None:
        result["candidates"].append({
            "type": "card",
            "bindings": card_info["bindings"],
            "card_ability": card_info["ability"],
            "relevance": card_info["relevance"],
        })
    for type_name,num in [("exact",n_exact),("near",n_near),("hard",n_hard),("random",n_random)]:
        for _ in range(num):
            new_bindings = []
            avg_relevance = 0.0
            for query_spec in bindings:
                new_query_spec=generate_candidate_from_query(query_spec, type_name, library, valid_binding_pool)
                relevance=compute_binding_relevance(query_spec, new_query_spec,missing_policy="zero")
                avg_relevance += relevance
                new_bindings.append(new_query_spec)
            avg_relevance /= len(bindings)

            new_card_ability=render_candidate_card(new_bindings,library)
            
            result["candidates"].append({
                "type": type_name,
                "bindings": new_bindings,
                "card_ability": new_card_ability,
                "relevance": avg_relevance,
            })
    return result
            


def generate_candidate_from_query(
        query_spec: Mapping[str, Any],
        candidate_type: str,
        library=None,
        valid_binding_pool=None,
    ):
    """
    type:
    ①exact: Exact candidates
    ②near: Near candidates
    ③hard: Hard negatives
    ④random: Random negatives
    """
    if candidate_type == "exact":
        spec = generate_exact_spec(query_spec)

    elif candidate_type == "near":
        spec = generate_near_spec(query_spec, library, valid_binding_pool)

    elif candidate_type == "hard":
        spec = generate_hard_spec(
            query_spec, valid_binding_pool
        )

    else:
        spec = generate_random_spec(
            query_spec, valid_binding_pool
        )


    spec = normalize_candidate_spec(spec)
    if library is not None:
        validate_candidate_spec(spec, library)

    return spec




def generate_card_data():
    pass



def generate_fake_data():
    pass


if __name__ == "__main__":
    library = load_library()
    cards = load_cards()

    while True:
        
        
        valid_binding_pool = build_valid_binding_pool(
            cards,
            library,
        )
        bindings = get_random_bindings(
            valid_binding_pool,
            library,
        )

        print(bindings)
        
        result = build_candidate_group(bindings,library,valid_binding_pool=valid_binding_pool)

        print(json.dumps(result, ensure_ascii=False, indent=2))
            
