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
    TEST_CASES = [

        # ============================================================
        # 1. DRAW / amount
        # ============================================================

        {
            "name": "draw_1",
            "spec": {
                "effect": "DRAW",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "draw_2",
            "spec": {
                "effect": "DRAW",
                "amount": "N_2",
                "amount_value": 2,
            },
        },

        {
            "name": "draw_4",
            "spec": {
                "effect": "DRAW",
                "amount": "N_4",
                "amount_value": 4,
            },
        },

        # ============================================================
        # 2. DAMAGE
        # ============================================================

        {
            "name": "damage_creature_1",
            "spec": {
                "effect": "DEAL_DAMAGE",
                "target": "CREATURE",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "damage_creature_3",
            "spec": {
                "effect": "DEAL_DAMAGE",
                "target": "CREATURE",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "damage_any_3",
            "spec": {
                "effect": "DEAL_DAMAGE",
                "target": "ANY",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "damage_opponent_4",
            "spec": {
                "effect": "DEAL_DAMAGE",
                "target": "OPPONENT",
                "amount": "N_4",
                "amount_value": 4,
            },
        },

        {
            "name": "damage_each_opponent",
            "spec": {
                "effect": "DAMAGE_EACH",
                "target": "EACH_OPPONENT",
                "amount": "N_2",
                "amount_value": 2,
            },
        },

        {
            "name": "damage_each_creature",
            "spec": {
                "effect": "DAMAGE_EACH",
                "target": "EACH_CREATURE",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "damage_all_creatures",
            "spec": {
                "effect": "DAMAGE_EACH",
                "target": "ALL_CREATURES",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        # ============================================================
        # 3. LIFE
        # ============================================================

        {
            "name": "gain_life_1",
            "spec": {
                "effect": "GAIN_LIFE",
                "target": "YOU",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "gain_life_5",
            "spec": {
                "effect": "GAIN_LIFE",
                "target": "YOU",
                "amount": "N_5",
                "amount_value": 5,
            },
        },

        {
            "name": "opponent_loses_life",
            "spec": {
                "effect": "LOSE_LIFE",
                "target": "OPPONENT",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "each_opponent_loses_life",
            "spec": {
                "effect": "LOSE_LIFE",
                "target": "EACH_OPPONENT",
                "amount": "N_2",
                "amount_value": 2,
            },
        },

        # ============================================================
        # 4. DISCARD / MILL / SCRY
        # ============================================================

        {
            "name": "discard_1",
            "spec": {
                "effect": "DISCARD",
                "target": "OPPONENT",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "discard_3",
            "spec": {
                "effect": "DISCARD",
                "target": "OPPONENT",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "mill_self_3",
            "spec": {
                "effect": "MILL",
                "target": "YOU",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "mill_opponent_5",
            "spec": {
                "effect": "MILL",
                "target": "OPPONENT",
                "amount": "N_5",
                "amount_value": 5,
            },
        },

        {
            "name": "scry_1",
            "spec": {
                "effect": "SCRY",
                "target": "YOU",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "scry_3",
            "spec": {
                "effect": "SCRY",
                "target": "YOU",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        # ============================================================
        # 5. DESTROY / EXILE / RETURN
        # ============================================================

        {
            "name": "destroy_creature",
            "spec": {
                "effect": "DESTROY",
                "target": "CREATURE",
            },
        },

        {
            "name": "destroy_nonland",
            "spec": {
                "effect": "DESTROY",
                "target": "NONLAND_PERMANENT",
            },
        },

        {
            "name": "destroy_artifact_enchantment",
            "spec": {
                "effect": "DESTROY",
                "target": "ARTIFACT_OR_ENCHANTMENT",
            },
        },

        {
            "name": "exile_creature",
            "spec": {
                "effect": "EXILE",
                "target": "CREATURE",
            },
        },

        {
            "name": "exile_permanent",
            "spec": {
                "effect": "EXILE",
                "target": "PERMANENT",
            },
        },

        {
            "name": "return_creature",
            "spec": {
                "effect": "RETURN_HAND",
                "target": "CREATURE",
            },
        },

        {
            "name": "return_nonland",
            "spec": {
                "effect": "RETURN_HAND",
                "target": "NONLAND_PERMANENT",
            },
        },

        # ============================================================
        # 6. COUNTER
        # ============================================================

        {
            "name": "counter_spell",
            "spec": {
                "effect": "COUNTER_SPELL",
                "target": "SPELL",
            },
        },

        # ============================================================
        # 7. TEMP BUFF
        # 重点测试 subject target + duration
        # ============================================================

        {
            "name": "buff_creature_1_1",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURE",
                "duration": "UNTIL_EOT",
                "p": 1,
                "t": 1,
            },
        },

        {
            "name": "buff_your_creature_4_4",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURE_YOU_CONTROL",
                "duration": "UNTIL_EOT",
                "p": 4,
                "t": 4,
            },
        },

        {
            "name": "buff_all_your_creatures",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURES_YOU_CONTROL",
                "duration": "UNTIL_EOT",
                "p": 1,
                "t": 1,
            },
        },

        {
            "name": "buff_self",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "SELF",
                "duration": "UNTIL_EOT",
                "p": 2,
                "t": 2,
            },
        },

        {
            "name": "buff_as_long_as_control",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURE_YOU_CONTROL",
                "duration": "AS_LONG_AS_CONTROL",
                "p": 2,
                "t": 0,
            },
        },

        # ============================================================
        # 8. +1/+1 COUNTERS
        # ============================================================

        {
            "name": "counter_1",
            "spec": {
                "effect": "PLUS1_COUNTER",
                "target": "CREATURE",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "counter_3",
            "spec": {
                "effect": "PLUS1_COUNTER",
                "target": "CREATURE_YOU_CONTROL",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        # ============================================================
        # 9. KEYWORD
        # ============================================================

        {
            "name": "grant_flying",
            "spec": {
                "effect": "GRANT_KEYWORD",
                "target": "CREATURE",
                "keyword": "FLYING",
                "duration": "UNTIL_EOT",
            },
        },

        {
            "name": "grant_hexproof",
            "spec": {
                "effect": "GRANT_KEYWORD",
                "target": "CREATURE_YOU_CONTROL",
                "keyword": "HEXPROOF",
                "duration": "UNTIL_EOT",
            },
        },

        {
            "name": "grant_lifelink_team",
            "spec": {
                "effect": "GRANT_KEYWORD",
                "target": "CREATURES_YOU_CONTROL",
                "keyword": "LIFELINK",
                "duration": "UNTIL_EOT",
            },
        },

        {
            "name": "grant_indestructible",
            "spec": {
                "effect": "GRANT_KEYWORD",
                "target": "CREATURE_YOU_CONTROL",
                "keyword": "INDESTRUCTIBLE",
                "duration": "THIS_TURN",
            },
        },

        # ============================================================
        # 10. TOKENS
        # ============================================================

        {
            "name": "token_1",
            "spec": {
                "effect": "CREATE_TOKEN",
                "amount": "N_1",
                "amount_value": 1,
                "token": "1/1 white Soldier",
            },
        },

        {
            "name": "token_3",
            "spec": {
                "effect": "CREATE_TOKEN",
                "amount": "N_3",
                "amount_value": 3,
                "token": "1/1 red Goblin",
            },
        },

        {
            "name": "token_2_zombie",
            "spec": {
                "effect": "CREATE_TOKEN",
                "amount": "N_2",
                "amount_value": 2,
                "token": "2/2 black Zombie",
            },
        },

        # ============================================================
        # 11. SEARCH
        # ============================================================

        {
            "name": "search_library",
            "spec": {
                "effect": "SEARCH_LIBRARY",
                "target": "LIBRARY_CARD",
            },
        },

        {
            "name": "search_to_hand",
            "spec": {
                "effect": "SEARCH_TO_HAND",
                "target": "LIBRARY_CARD",
            },
        },

        # ============================================================
        # 12. REANIMATE / BATTLEFIELD
        # ============================================================

        {
            "name": "reanimate",
            "spec": {
                "effect": "REANIMATE",
                "target": "GRAVEYARD_CREATURE",
            },
        },

        {
            "name": "put_battlefield",
            "spec": {
                "effect": "PUT_BATTLEFIELD",
                "target": "LIBRARY_CARD",
            },
        },

        # ============================================================
        # 13. SACRIFICE
        # ============================================================

        {
            "name": "sacrifice_your_creature",
            "spec": {
                "effect": "SACRIFICE",
                "target": "CREATURE_YOU_CONTROL",
            },
        },

        {
            "name": "sacrifice_self",
            "spec": {
                "effect": "SACRIFICE",
                "target": "SELF",
            },
        },

        # ============================================================
        # 14. TAP
        # ============================================================

        {
            "name": "tap_creature",
            "spec": {
                "effect": "TAP",
                "target": "CREATURE",
            },
        },

        {
            "name": "tap_opponent_creature",
            "spec": {
                "effect": "TAP",
                "target": "CREATURE_OPPONENT",
            },
        },

        # ============================================================
        # 15. PREVENT DAMAGE
        # ============================================================

        {
            "name": "prevent_damage_creature",
            "spec": {
                "effect": "PREVENT_DAMAGE",
                "target": "CREATURE",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "prevent_damage_you",
            "spec": {
                "effect": "PREVENT_DAMAGE",
                "target": "YOU",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        # ============================================================
        # 16. MANA
        # ============================================================

        {
            "name": "add_mana",
            "spec": {
                "effect": "ADD_MANA",
                "amount": "N_1",
                "amount_value": 1,
                "color": "green",
            },
        },

        {
            "name": "add_three_mana",
            "spec": {
                "effect": "ADD_MANA",
                "amount": "N_3",
                "amount_value": 3,
                "color": "red",
            },
        },

        # ============================================================
        # 17. EXTRA TURN
        # 非常容易 duration 重复
        # ============================================================

        {
            "name": "extra_turn_clean",
            "spec": {
                "effect": "EXTRA_TURN",
            },
        },

        {
            "name": "extra_turn_with_redundant_duration",
            "spec": {
                "effect": "EXTRA_TURN",
                "duration": "EXTRA_TURN",
            },
        },

        # ============================================================
        # 18. TRIGGER + EFFECT
        # ============================================================

        {
            "name": "etb_draw",
            "spec": {
                "trigger": "ETB",
                "effect": "DRAW",
                "amount": "N_2",
                "amount_value": 2,
            },
        },

        {
            "name": "etb_gain_life",
            "spec": {
                "trigger": "ETB",
                "effect": "GAIN_LIFE",
                "target": "YOU",
                "amount": "N_3",
                "amount_value": 3,
            },
        },

        {
            "name": "attack_buff_self",
            "spec": {
                "trigger": "ATTACK",
                "effect": "TEMP_BUFF",
                "target": "SELF",
                "duration": "UNTIL_EOT",
                "p": 2,
                "t": 0,
            },
        },

        {
            "name": "dies_draw",
            "spec": {
                "trigger": "DIES",
                "effect": "DRAW",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "creature_dies_gain_life",
            "spec": {
                "trigger": "CREATURE_DIES",
                "effect": "GAIN_LIFE",
                "target": "YOU",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "upkeep_draw",
            "spec": {
                "trigger": "UPKEEP",
                "effect": "DRAW",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "cast_spell_draw",
            "spec": {
                "trigger": "CAST_SPELL",
                "effect": "DRAW",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "cast_instant_sorcery_scry",
            "spec": {
                "trigger": "CAST_INSTANT_SORCERY",
                "effect": "SCRY",
                "target": "YOU",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        {
            "name": "land_enters_gain_life",
            "spec": {
                "trigger": "LAND_ENTERS",
                "effect": "GAIN_LIFE",
                "target": "YOU",
                "amount": "N_1",
                "amount_value": 1,
            },
        },

        # ============================================================
        # 19. TRIGGER + TARGET + DURATION
        # 组合压力测试
        # ============================================================

        {
            "name": "etb_buff_team",
            "spec": {
                "trigger": "ETB",
                "effect": "TEMP_BUFF",
                "target": "CREATURES_YOU_CONTROL",
                "duration": "UNTIL_EOT",
                "p": 1,
                "t": 1,
            },
        },

        {
            "name": "attack_grant_trample",
            "spec": {
                "trigger": "ATTACK",
                "effect": "GRANT_KEYWORD",
                "target": "SELF",
                "keyword": "TRAMPLE",
                "duration": "UNTIL_EOT",
            },
        },

        {
            "name": "cast_spell_buff_creature",
            "spec": {
                "trigger": "CAST_SPELL",
                "effect": "TEMP_BUFF",
                "target": "CREATURE_YOU_CONTROL",
                "duration": "UNTIL_EOT",
                "p": 1,
                "t": 1,
            },
        },

        # ============================================================
        # 20. DURATION EDGE CASES
        # ============================================================

        {
            "name": "buff_this_turn",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURE",
                "duration": "THIS_TURN",
                "p": 2,
                "t": 2,
            },
        },

        {
            "name": "buff_until_leaves",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "SELF",
                "duration": "UNTIL_LEAVES",
                "p": 1,
                "t": 1,
            },
        },

        {
            "name": "grant_keyword_permanent",
            "spec": {
                "effect": "GRANT_KEYWORD",
                "target": "CREATURE",
                "keyword": "FLYING",
                "duration": "PERMANENT",
            },
        },

        {
            "name": "draw_instant_duration_should_omit",
            "spec": {
                "effect": "DRAW",
                "amount": "N_2",
                "amount_value": 2,
                "duration": "INSTANT",
            },
        },

        # ============================================================
        # 21. MASS TARGET
        # ============================================================

        {
            "name": "buff_all_creatures",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "ALL_CREATURES",
                "duration": "UNTIL_EOT",
                "p": 1,
                "t": -1,
            },
        },

        {
            "name": "grant_flying_all_yours",
            "spec": {
                "effect": "GRANT_KEYWORD",
                "target": "CREATURES_YOU_CONTROL",
                "keyword": "FLYING",
                "duration": "UNTIL_EOT",
            },
        },

        # ============================================================
        # 22. 不对称 P/T
        # ============================================================

        {
            "name": "buff_power_only",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURE",
                "duration": "UNTIL_EOT",
                "p": 3,
                "t": 0,
            },
        },

        {
            "name": "buff_toughness_only",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURE",
                "duration": "UNTIL_EOT",
                "p": 0,
                "t": 4,
            },
        },

        {
            "name": "negative_pt",
            "spec": {
                "effect": "TEMP_BUFF",
                "target": "CREATURE",
                "duration": "UNTIL_EOT",
                "p": -2,
                "t": -2,
            },
        },
    ]
    for i, case in enumerate(TEST_CASES, 1):

        print("=" * 80)
        print(
            f"[{i:03d}] {case['name']}"
        )

        query_spec = case["spec"]

        print(
            "query_spec:",
            query_spec,
        )

        try:

            candidate_spec = (
                generate_candidate_from_query(
                    query_spec,
                    "exact",
                )
            )

            print(
                "candidate_spec:",
                candidate_spec,
            )

            rendered = render_candidate_spec(
                candidate_spec,
                library,
            )

            print(
                "rendered:",
                rendered,
            )

        except Exception as e:

            print(
                "ERROR:",
                type(e).__name__,
                str(e),
            )