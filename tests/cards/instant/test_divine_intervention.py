from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDivine_Intervention(CardTestCaseBase):
    async def test_divine_intervention_exiles_all_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Intervention/model.py", "Divine_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p2, "Opp C", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(c1), "exile_area")
        self.assertEqual(env.card_zone(c2), "exile_area")

    async def test_divine_intervention_resolves_with_empty_battlefields(self):
        """Implementation clears both battlefields; empty boards stay empty."""
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Intervention/model.py", "Divine_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        self.assertEqual(len(env.p1.battlefield), 0)
        self.assertEqual(len(env.p2.battlefield), 0)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), 0)
        self.assertEqual(len(env.p2.battlefield), 0)

    async def test_divine_intervention_player_life_totals_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Intervention/model.py", "Divine_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "A", 1, 1, 1)
        env.put_creatures(env.p2, "B", 1, 1, 1)
        p1l, p2l = env.p1.life, env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1l)
        self.assertEqual(env.p2.life, p2l)
