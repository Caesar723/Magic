"""
Card text vs implementation: nonbasic lands offer a mana ability plus an optional
activated ability chosen via `send_selection_cards` (tests auto-pick the first option).

These tests assert that a single `when_clicked` with default selection only runs the
primary mana ability—no damage, bounce, tutor, extra draw, etc.
"""

from __future__ import annotations

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestLandCardTextGaps(CardTestCaseBase):
    async def test_volcanic_fumaroles_no_damage_on_standard_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Volcanic_Fumaroles/model.py", "Volcanic_Fumaroles"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("deal 1 damage", card.content.lower())
        env.put_creatures(env.p2, "Blocker", 1, 4)
        crea = env.get_battlefield_creature(env.p2, "Blocker")
        opp_life = env.p2.life
        env.put_in_land_area(card, env.p1)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(env.p2.life, opp_life)
        self.assertEqual(crea.actual_live, crea.live)

    async def test_nexus_of_the_eternal_seas_no_bounce_on_standard_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Nexus_of_the_Eternal_Seas/model.py", "Nexus_of_the_Eternal_Seas"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("return target creature", card.content.lower())
        env.put_creatures(env.p2, "Fish", 1, 1)
        crea = env.get_battlefield_creature(env.p2, "Fish")
        env.put_in_land_area(card, env.p1)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(env.card_zone(crea), "battlefield")

    async def test_mystic_reflection_pool_no_draw_on_standard_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Mystic_Reflection_Pool/model.py", "Mystic_Reflection_Pool"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("draw a card", card.content.lower())
        lib_before = len(env.p1.library)
        hand_before = len(env.p1.hand)
        env.put_in_land_area(card, env.p1)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(len(env.p1.library), lib_before)
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_arcane_sanctuary_no_pay_scry_draw_on_standard_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Arcane_Sanctuary/model.py", "Arcane_Sanctuary"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("pay 2 mana", card.content.lower())
        lib_before = len(env.p1.library)
        env.put_in_land_area(card, env.p1)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(len(env.p1.library), lib_before)

    async def test_elysian_grove_does_not_untap_opponent_land_on_mana_tap(self) -> None:
        cls = load_card_class_from_path("pycards/land/Elysian_Grove/model.py", "Elysian_Grove")
        env = self.make_env()
        grove = cls(env.p1)
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        opp_land = forest_cls(env.p2)
        env.put_in_land_area(opp_land, env.p2)
        opp_land.flag_dict["tap"] = True
        env.put_in_land_area(grove, env.p1)
        await env.trigger(grove, "when_clicked", env.p1, env.p2)
        self.assertTrue(opp_land.get_flag("tap"))

    async def test_sanctum_eternal_flames_no_extra_damage_on_mana_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Sanctum_of_Eternal_Flames/model.py", "Sanctum_of_Eternal_Flames"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("deal 2 damage", card.content.lower())
        life = env.p2.life
        env.put_in_land_area(card, env.p1)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(env.p2.life, life)

    async def test_luminous_glade_no_damage_prevention_setup_on_mana_tap(self) -> None:
        cls = load_card_class_from_path("pycards/land/Luminous_Glade/model.py", "Luminous_Glade")
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("prevent the next 1 damage", card.content.lower())
        env.put_in_land_area(card, env.p1)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertFalse(env.p1.get_flag("prevent_next_damage"))

    async def test_verdant_sanctuary_no_tutor_on_mana_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Verdant_Sanctuary/model.py", "Verdant_Sanctuary"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("search your library", card.content.lower())
        env.put_in_land_area(card, env.p1)
        lib_before = len(env.p1.library)
        lands_after_setup = len(env.p1.land_area)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(len(env.p1.library), lib_before)
        self.assertEqual(len(env.p1.land_area), lands_after_setup)

    async def test_sanctum_of_verdant_growth_no_tutor_on_mana_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Sanctum_of_Verdant_Growth/model.py", "Sanctum_of_Verdant_Growth"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("search your library", card.content.lower())
        env.put_in_land_area(card, env.p1)
        lib_before = len(env.p1.library)
        lands_after_setup = len(env.p1.land_area)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(len(env.p1.library), lib_before)
        self.assertEqual(len(env.p1.land_area), lands_after_setup)

    async def test_celestial_haven_no_combat_shield_on_mana_tap(self) -> None:
        cls = load_card_class_from_path(
            "pycards/land/Celestial_Haven/model.py", "Celestial_Haven"
        )
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("prevent all combat damage", card.content.lower())
        life_before = env.p1.life
        env.put_in_land_area(card, env.p1)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(env.p1.life, life_before)

    async def test_aetheric_nexus_primary_tap_is_colorless_only(self) -> None:
        cls = load_card_class_from_path("pycards/land/Aetheric_Nexus/model.py", "Aetheric_Nexus")
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("any color", card.content.lower())
        env.put_in_land_area(card, env.p1)
        mana_before = dict(env.p1.mana)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(env.p1.mana["colorless"], mana_before["colorless"] + 1)
        self.assertEqual(env.p1.mana["U"], mana_before["U"])

    async def test_arcane_haven_primary_tap_is_colorless_only(self) -> None:
        cls = load_card_class_from_path("pycards/land/Arcane_Haven/model.py", "Arcane_Haven")
        env = self.make_env()
        card = cls(env.p1)
        self.assertIn("any color", card.content.lower())
        env.put_in_land_area(card, env.p1)
        mana_before = dict(env.p1.mana)
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertEqual(env.p1.mana["colorless"], mana_before["colorless"] + 1)
        self.assertEqual(env.p1.mana["R"], mana_before["R"])
