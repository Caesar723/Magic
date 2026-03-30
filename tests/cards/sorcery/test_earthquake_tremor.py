from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEarthquake_Tremor(CardTestCaseBase):
    async def test_earthquake_tremor_destroys_up_to_three_and_creates_tokens(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Earthquake_Tremor/model.py", "Earthquake_Tremor")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p2, "Enemy A", 2, 2, 1)
        env.put_creatures(env.p2, "Enemy B", 2, 2, 1)
        env.put_creatures(env.p2, "Enemy C", 2, 2, 1)
        before_self = len(env.p1.battlefield)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(len(env.p1.battlefield), before_self + 1)

    async def test_earthquake_tremor_no_opponent_creatures_no_tokens(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Earthquake_Tremor/model.py", "Earthquake_Tremor")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p2.battlefield)
        before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), before)

    async def test_earthquake_tremor_only_hits_opponent_battlefield(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Earthquake_Tremor/model.py", "Earthquake_Tremor")
        env = self.make_env()
        card = card_cls(env.p1)

        friendly = env.put_creatures(env.p1, "Friendly Wall", 4, 4, 1)[0]
        env.put_creatures(env.p2, "Solo Enemy", 2, 2, 1)
        bf_before = len(env.p1.battlefield)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(friendly, env.p1.battlefield)
        self.assertGreater(len(env.p1.battlefield), bf_before)
