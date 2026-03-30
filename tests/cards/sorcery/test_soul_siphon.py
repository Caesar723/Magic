from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSoul_Siphon(CardTestCaseBase):
    async def test_soul_siphon_sacrifice_and_life_gain(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Soul_Siphon/model.py", "Soul_Siphon")
        env = self.make_env()
        card = card_cls(env.p1)

        victim = env.put_creatures(env.p2, "Victim", 3, 3, 1)[0]
        env.p1.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(victim), "graveyard")
        self.assertEqual(env.p1.life, 13)

    async def test_soul_siphon_no_opponent_creature_no_life_gain(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Soul_Siphon/model.py", "Soul_Siphon")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.battlefield = []
        env.p1.life = 10
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 10)

    async def test_soul_siphon_opponent_life_unchanged_when_sacrificing(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Soul_Siphon/model.py", "Soul_Siphon")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Victim", 4, 2, 1)
        env.p1.life = 5
        opp_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
        self.assertEqual(env.p1.life, 9)
