from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTime_Warp(CardTestCaseBase):
    async def test_time_warp_adds_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Time_Warp/model.py", "Time_Warp")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})
        self.assertEqual(env.card_zone(card), "graveyard")

    async def test_time_warp_accumulates_existing_extra_turns(self):
        card_cls = load_card_class_from_path("pycards/Instant/Time_Warp/model.py", "Time_Warp")
        env = self.make_env()
        env.p1.add_counter_dict("extra_turn", 1)
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 2}})

    async def test_time_warp_leaves_opponent_extra_turn_counter_zero(self):
        card_cls = load_card_class_from_path("pycards/Instant/Time_Warp/model.py", "Time_Warp")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.get_counter_from_dict("extra_turn"), 0)
