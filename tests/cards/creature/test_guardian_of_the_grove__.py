from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestGuardian_of_the_Grove__(CardTestCaseBase):
    async def test_guardian_of_the_grove_etb_only_checks_for_forest(self):
        card_cls = load_card_class_from_path("pycards/creature/Guardian_of_the_Grove__/model.py", "Guardian_of_the_Grove__")
        mountain_cls = load_card_class_from_path("pycards/land/Mountain/model.py", "Mountain")
        env = self.make_env()
        card = card_cls(env.p1)

        mountain = mountain_cls(env.p1)
        env.p1.library = [mountain]

        env.put_on_battlefield(card, env.p1)
        await env.trigger(card, "when_enter_battlefield", env.p1, env.p2)
        guardian = env.get_battlefield_creature(env.p1, "Guardian of the Grove")
        self.assert_state(guardian, {"zone": "battlefield", "state": (3, 3)})
        self.assertEqual(len(env.p1.library), 1)
        self.assertEqual(env.p1.library[0].name, "Mountain")

    async def test_guardian_of_the_grove_play_resolves_guardian_to_battlefield(self):
        """Full cast path; ETB library effect is covered by the direct trigger test above."""
        card_cls = load_card_class_from_path("pycards/creature/Guardian_of_the_Grove__/model.py", "Guardian_of_the_Grove__")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        g = env.get_battlefield_creature(env.p1, "Guardian of the Grove")
        self.assert_state(g, {"zone": "battlefield", "state": (3, 3)})

    async def test_guardian_of_the_grove_play_with_empty_library_skips_land_search(self):
        card_cls = load_card_class_from_path("pycards/creature/Guardian_of_the_Grove__/model.py", "Guardian_of_the_Grove__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 0)
        env.get_battlefield_creature(env.p1, "Guardian of the Grove")
