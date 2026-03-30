from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVampiric_Revelry(CardTestCaseBase):
    async def test_vampiric_revelry_sacrifice_and_gain_toughness(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Vampiric_Revelry/model.py", "Vampiric_Revelry")
        env = self.make_env()
        card = card_cls(env.p1)

        victim = env.put_creatures(env.p2, "Victim", 2, 4, 1)[0]
        env.p1.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(victim), "graveyard")
        self.assertEqual(env.p1.life, 14)

    async def test_vampiric_revelry_empty_opponent_battlefield_is_noop(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Vampiric_Revelry/model.py", "Vampiric_Revelry")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 20
        self.assertFalse(env.p2.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 20)

    async def test_vampiric_revelry_opponent_life_unchanged_when_sacrificing(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Vampiric_Revelry/model.py", "Vampiric_Revelry")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Victim", 2, 5, 1)
        env.p1.life = 12
        opp_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
        self.assertEqual(env.p1.life, 17)
