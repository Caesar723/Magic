from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAetherweaver(CardTestCaseBase):
    async def test_aetherweaver_etb_picks_spell_from_top_three(self):
        creature_cls = load_card_class_from_path("pycards/creature/Aetherweaver/model.py", "Aetherweaver")
        instant_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        sorcery_cls = load_card_class_from_path("pycards/sorcery/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = creature_cls(env.p1)

        spell_1 = instant_cls(env.p1)
        spell_2 = sorcery_cls(env.p1)
        spell_3 = instant_cls(env.p1)
        env.p1.library = [spell_1, spell_2, spell_3]
        env.script_selection(env.p1, [1])  # choose spell_2 from top-3 selectable spells

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        weaver = env.get_battlefield_creature(env.p1, "Aetherweaver")
        self.assert_state(weaver, {"zone": "battlefield", "state": (2, 3)})
        hand_names = [c.name for c in env.p1.hand]
        self.assertIn(spell_2.name, hand_names)
        self.assertEqual(len(env.p1.library), 2)

    async def test_aetherweaver_etb_no_instant_or_sorcery_in_library(self):
        creature_cls = load_card_class_from_path("pycards/creature/Aetherweaver/model.py", "Aetherweaver")
        env = self.make_env()
        card = creature_cls(env.p1)
        dummy = env.create_creature(env.p1, "Library Filler", 1, 1)
        env.p1.library = [dummy]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        weaver = env.get_battlefield_creature(env.p1, "Aetherweaver")
        self.assert_state(weaver, {"zone": "battlefield"})
        self.assertEqual(len(env.p1.library), 1)
        self.assertIs(env.p1.library[0], dummy)

    async def test_aetherweaver_etb_two_spell_window_skips_leading_non_spell(self):
        """First two instants/sorceries in library order are offered when fewer than three exist."""
        creature_cls = load_card_class_from_path("pycards/creature/Aetherweaver/model.py", "Aetherweaver")
        instant_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        sorcery_cls = load_card_class_from_path("pycards/sorcery/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = creature_cls(env.p1)

        filler = env.create_creature(env.p1, "Deck Filler", 1, 1)
        top = instant_cls(env.p1)
        second = sorcery_cls(env.p1)
        env.p1.library = [filler, top, second]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        hand_names = [c.name for c in env.p1.hand]
        self.assertIn(top.name, hand_names)
        self.assertNotIn(second.name, hand_names)
        self.assertEqual(len(env.p1.library), 2)
        lib_names = [c.name for c in env.p1.library]
        self.assertIn(second.name, lib_names)
        self.assertIn(filler.name, lib_names)
