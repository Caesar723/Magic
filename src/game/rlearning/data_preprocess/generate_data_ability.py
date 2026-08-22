from typing import Any, Mapping
import json
from pathlib import Path

from candidate import generate_exact_spec, generate_near_spec, generate_hard_spec, generate_random_spec, normalize_candidate_spec
from similarity import compute_binding_relevance
from spec_render import render_candidate_spec


def load_library():
    LIB_DIR = Path(__file__).resolve().parents[1] / "data/retrieval/libraries"
    result={
        "triggers":json.loads((LIB_DIR / "triggers.json").read_text(encoding="utf-8")),
        "durations":json.loads((LIB_DIR / "durations.json").read_text(encoding="utf-8")),
        "statics":json.loads((LIB_DIR / "statics.json").read_text(encoding="utf-8")),
        "amounts":json.loads((LIB_DIR / "amounts.json").read_text(encoding="utf-8")),
        "effects":json.loads((LIB_DIR / "effects.json").read_text(encoding="utf-8")),
        "targets":json.loads((LIB_DIR / "targets.json").read_text(encoding="utf-8")),
    }
    return result







def get_query_from_card():
    pass


def build_candidate_group(query_spec,cards,n_exact=2,n_near=3,n_hard=2,n_random=1):
    pass
def generate_candidate_from_query(
        query_spec: Mapping[str, Any],
        candidate_type: str,
    ):
    """
    type:
    ①exact: Exact candidates
    ②near: Near candidates
    ③hard: Hard negatives
    ④random: Random negatives
    """
    if candidate_type == "exact":
        spec = generate_exact_spec(
            query_spec
        )

    elif candidate_type == "near":
        spec = generate_near_spec(
            query_spec
        )

    elif candidate_type == "hard":
        spec = generate_hard_spec(
            query_spec
        )

    else:
        spec = generate_random_spec(
            query_spec
        )


    spec = normalize_candidate_spec(spec)

    return spec



def get_random_query():
    pass


def generate_card_data():
    pass



def generate_fake_data():
    pass


if __name__ == "__main__":
    library = load_library()
    query_spec = {
        "effect": "DRAW",
        "amount_value": 4,
        "amount": "N_4",
    }
    candidate_spec = generate_candidate_from_query(query_spec, "random")
    print(candidate_spec)
    rendered_candidate_spec = render_candidate_spec(candidate_spec, library)
    print(rendered_candidate_spec)