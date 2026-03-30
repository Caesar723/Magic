from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTemporal_Distortion(CardTestCaseBase):
    async def test_temporal_distortion_adds_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Temporal_Distortion/model.py", "Temporal_Distortion")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})
        self.assertTrue(card.flag_dict.get("exile", False))

    async def test_temporal_distortion_stacks_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Temporal_Distortion/model.py", "Temporal_Distortion")
        env = self.make_env()
        env.p1.add_counter_dict("extra_turn", 2)
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 3}})

    async def test_temporal_distortion_does_not_add_opponent_extra_turns(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Temporal_Distortion/model.py", "Temporal_Distortion")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.get_counter_from_dict("extra_turn"), 0)
