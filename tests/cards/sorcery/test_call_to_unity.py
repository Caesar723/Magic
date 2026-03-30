from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCall_to_Unity(CardTestCaseBase):
    async def test_call_to_unity_creates_two_human_tokens(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_to_Unity/model.py", "Call_to_Unity")
        env = self.make_env()
        card = card_cls(env.p1)

        before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), before + 2)
        self.assertEqual(env.p1.battlefield[-1].name, "Human")
        self.assertEqual(env.p1.battlefield[-2].name, "Human")
        self.assertEqual(env.p1.battlefield[-1].state, (1, 1))
        self.assertEqual(env.p1.battlefield[-2].state, (1, 1))

    async def test_call_to_unity_adds_two_more_on_second_cast(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_to_Unity/model.py", "Call_to_Unity")
        env = self.make_env()
        first = card_cls(env.p1)
        second = card_cls(env.p1)

        before = len(env.p1.battlefield)
        res1 = await env.play_card(first, env.p1)
        await env.resolve_stack()
        res2 = await env.play_card(second, env.p1)
        await env.resolve_stack()

        self.assertTrue(res1[0])
        self.assertTrue(res2[0])
        self.assertEqual(len(env.p1.battlefield), before + 4)

    async def test_call_to_unity_does_not_add_tokens_to_opponent(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_to_Unity/model.py", "Call_to_Unity")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_before = len(env.p2.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.battlefield), opp_before)
