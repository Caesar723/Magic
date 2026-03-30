"""
Cross-cutting land mana + zone contracts for every `pycards` land implementation.
"""

from __future__ import annotations

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path

# (model path relative to src/, Python class name)
ALL_LAND_SPECS: list[tuple[str, str]] = [
    ("pycards/land/Aetheric_Nexus/model.py", "Aetheric_Nexus"),
    ("pycards/land/Arcane_Haven/model.py", "Arcane_Haven"),
    ("pycards/land/Arcane_Sanctuary/model.py", "Arcane_Sanctuary"),
    ("pycards/land/Celestial_Haven/model.py", "Celestial_Haven"),
    ("pycards/land/Elysian_Grove/model.py", "Elysian_Grove"),
    ("pycards/land/Forest/model.py", "Forest"),
    ("pycards/land/Island/model.py", "Island"),
    ("pycards/land/Luminous_Glade/model.py", "Luminous_Glade"),
    ("pycards/land/Mountain/model.py", "Mountain"),
    ("pycards/land/Mystic_Reflection_Pool/model.py", "Mystic_Reflection_Pool"),
    ("pycards/land/Nexus_of_the_Eternal_Seas/model.py", "Nexus_of_the_Eternal_Seas"),
    ("pycards/land/Plains/model.py", "Plains"),
    ("pycards/land/Sanctum_of_Eternal_Flames/model.py", "Sanctum_of_Eternal_Flames"),
    ("pycards/land/Sanctum_of_Verdant_Growth/model.py", "Sanctum_of_Verdant_Growth"),
    ("pycards/land/Swamp/model.py", "Swamp"),
    ("pycards/land/Verdant_Sanctuary/model.py", "Verdant_Sanctuary"),
    ("pycards/land/Volcanic_Fumaroles/model.py", "Volcanic_Fumaroles"),
]


class TestLandManaContracts(CardTestCaseBase):
    async def test_each_land_play_then_resolve_is_in_land_area(self) -> None:
        for rel_path, cls_name in ALL_LAND_SPECS:
            with self.subTest(land=cls_name):
                card_cls = load_card_class_from_path(rel_path, cls_name)
                env = self.make_env()
                card = card_cls(env.p1)
                ok, _msg = await env.play_card(card, env.p1)
                await env.resolve_stack()
                self.assertTrue(ok)
                self.assertEqual(env.card_zone(card), "land_area")
                self.assertIn(card, env.p1.land_area)

    async def test_each_land_first_tap_matches_generate_mana(self) -> None:
        for rel_path, cls_name in ALL_LAND_SPECS:
            with self.subTest(land=cls_name):
                card_cls = load_card_class_from_path(rel_path, cls_name)
                env = self.make_env()
                card = card_cls(env.p1)
                env.put_in_land_area(card, env.p1)
                mana_before = {k: v for k, v in env.p1.mana.items()}
                expected = card.generate_mana()
                ok = await env.trigger(card, "when_clicked", env.p1, env.p2)
                self.assertTrue(ok)
                self.assertTrue(card.get_flag("tap"))
                for key, delta in expected.items():
                    self.assertEqual(env.p1.mana[key], mana_before[key] + delta)
                for key, before in mana_before.items():
                    if key not in expected:
                        self.assertEqual(env.p1.mana[key], before)

    async def test_each_land_second_click_while_tapped_adds_no_mana(self) -> None:
        for rel_path, cls_name in ALL_LAND_SPECS:
            with self.subTest(land=cls_name):
                card_cls = load_card_class_from_path(rel_path, cls_name)
                env = self.make_env()
                card = card_cls(env.p1)
                env.put_in_land_area(card, env.p1)
                await env.trigger(card, "when_clicked", env.p1, env.p2)
                mana_after_first = dict(env.p1.mana)
                second = await env.trigger(card, "when_clicked", env.p1, env.p2)
                self.assertFalse(second)
                self.assertEqual(dict(env.p1.mana), mana_after_first)

    async def test_forest_untap_allows_second_mana_activation(self) -> None:
        card_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_in_land_area(card, env.p1)
        expected = card.generate_mana()
        await env.trigger(card, "when_clicked", env.p1, env.p2)
        env.p1.action_store.start_record()
        card.untap()
        env.p1.action_store.end_record()
        self.assertFalse(card.get_flag("tap"))
        mana_mid = dict(env.p1.mana)
        again = await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertTrue(again)
        for key, delta in expected.items():
            self.assertEqual(env.p1.mana[key], mana_mid[key] + delta)

    async def test_land_on_battlefield_not_in_land_area_does_not_add_mana_when_clicked(
        self,
    ) -> None:
        """Mis-zoned lands (battlefield but not `land_area`) must not tap or produce mana."""
        card_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_on_battlefield(card, env.p1)
        self.assertEqual(env.card_zone(card), "battlefield")
        self.assertNotIn(card, env.p1.land_area)
        mana_before = dict(env.p1.mana)
        ok = await env.trigger(card, "when_clicked", env.p1, env.p2)
        self.assertFalse(ok)
        self.assertEqual(dict(env.p1.mana), mana_before)
        self.assertFalse(card.get_flag("tap"))
