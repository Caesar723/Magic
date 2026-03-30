from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTimeless_Intervention(CardTestCaseBase):
    async def test_timeless_intervention_exiles_then_returns_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Timeless_Intervention/model.py", "Timeless_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Self C", 2, 2, 1)
        env.put_creatures(env.p2, "Enemy C", 2, 2, 1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertGreaterEqual(len(env.p1.exile_area) + len(env.p2.exile_area), 2)

        await env.trigger(card, "when_start_turn", env.p1, env.p2)
        self.assertGreaterEqual(len(env.p1.battlefield) + len(env.p2.battlefield), 2)

    async def test_timeless_intervention_empty_battlefields_sets_return_flag(self):
        card_cls = load_card_class_from_path("pycards/Instant/Timeless_Intervention/model.py", "Timeless_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertTrue(card.get_flag("return_creature"))
        await env.trigger(card, "when_start_turn", env.p1, env.p2)
        self.assertFalse(card.get_flag("return_creature"))

    async def test_timeless_intervention_player_life_unchanged_on_resolve(self):
        card_cls = load_card_class_from_path("pycards/Instant/Timeless_Intervention/model.py", "Timeless_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "S", 2, 2, 1)
        env.put_creatures(env.p2, "E", 2, 2, 1)
        p1l, p2l = env.p1.life, env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1l)
        self.assertEqual(env.p2.life, p2l)
