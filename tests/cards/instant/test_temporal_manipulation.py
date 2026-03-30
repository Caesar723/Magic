from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTemporal_Manipulation(CardTestCaseBase):
    async def test_temporal_manipulation_adds_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Manipulation/model.py", "Temporal_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})
        self.assertEqual(env.card_zone(card), "graveyard")

    async def test_temporal_manipulation_stacks_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Manipulation/model.py", "Temporal_Manipulation")
        env = self.make_env()
        env.p1.add_counter_dict("extra_turn", 2)
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 3}})

    async def test_temporal_manipulation_does_not_grant_opponent_extra_turns(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Manipulation/model.py", "Temporal_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.get_counter_from_dict("extra_turn"), 0)
