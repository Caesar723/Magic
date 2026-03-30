from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTemporal_Shift(CardTestCaseBase):
    async def test_temporal_shift_adds_time_counter_and_freezes(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Shift/model.py", "Temporal_Shift")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p2, "Enemy A", 2, 4, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy B", 2, 4, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"time_counter": 1}})
        self.assertTrue(c1.get_flag("frozen") or c2.get_flag("frozen") or c1.state[1] < 4 or c2.state[1] < 4)

    async def test_temporal_shift_with_no_enemy_creatures_still_adds_time_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Shift/model.py", "Temporal_Shift")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.battlefield = []
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"time_counter": 1}})

    async def test_temporal_shift_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Shift/model.py", "Temporal_Shift")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Enemy", 2, 4, 1)
        opp_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
