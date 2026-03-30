from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTime_Rift_Convergence(CardTestCaseBase):
    async def test_time_rift_convergence_adds_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Time_Rift_Convergence/model.py", "Time_Rift_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 1}})
        self.assertTrue(card.flag_dict.get("exile", False))

    async def test_time_rift_convergence_stacks_extra_turn_counter(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Time_Rift_Convergence/model.py", "Time_Rift_Convergence")
        env = self.make_env()
        env.p1.add_counter_dict("extra_turn", 1)
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(env.p1, {"counters": {"extra_turn": 2}})

    async def test_time_rift_convergence_opponent_extra_turn_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Time_Rift_Convergence/model.py", "Time_Rift_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.get_counter_from_dict("extra_turn"), 0)
