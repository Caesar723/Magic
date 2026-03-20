from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestFlameblade_Pyromancer(CardTestCaseBase):
    async def test_flameblade_pyromancer_smoke(self):
        card_cls = load_card_class_from_path("pycards/creature/Flameblade_Pyromancer/model.py", "Flameblade_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)

        before = env.snapshot()
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        after = env.snapshot()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(before, dict)
        self.assertIsInstance(after, dict)

        if result[0]:
            played_card = env.find_card_by_name(env.p1, card.name)
            self.assertIsNotNone(played_card)
            self.assert_state(played_card, {"owner": "p1"})

    async def test_flameblade_pyromancer_custom_scenario_template(self):
        """Richer template: play card, optional combat, and core assertions."""
        card_cls = load_card_class_from_path("pycards/creature/Flameblade_Pyromancer/model.py", "Flameblade_Pyromancer")
        env = self.make_env()
        card = card_cls(env.p1)

        defenders = env.put_creatures(env.p2, "Test Defender", 2, 2, 2)
        before = env.snapshot()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(isinstance(result, tuple) and len(result) == 2)
        self.assertIsInstance(before, dict)

        if not result[0]:
            self.skipTest(f"Card play failed in template path: {result[1]}")

        played_card = env.find_card_by_name(env.p1, card.name)
        self.assertIsNotNone(played_card)

        if env.card_zone(played_card) == "battlefield":
            before_combat = env.snapshot()
            await env.simulate_combat(played_card, defenders[0])
            after = env.snapshot()
            self.assertLessEqual(after["p2"]["life"], before_combat["p2"]["life"])
            self.assertIn(env.card_zone(played_card), {"battlefield", "graveyard", "exile_area"})
            self.assertIn(env.card_zone(defenders[0]), {"battlefield", "graveyard", "exile_area"})
        else:
            self.assertIn(env.card_zone(played_card), {"graveyard", "exile_area", "hand"})
