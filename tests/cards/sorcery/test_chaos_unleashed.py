from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestChaos_Unleashed(CardTestCaseBase):
    async def test_chaos_unleashed_hits_both_players_and_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Chaos_Unleashed/model.py", "Chaos_Unleashed")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 4, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy C", 2, 4, 1)[0]
        env.p1.life = 10
        env.p2.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 7)
        self.assertEqual(env.p2.life, 7)
        self.assertEqual(c1.state[1], 1)
        self.assertEqual(c2.state[1], 1)

    async def test_chaos_unleashed_lethal_to_two_toughness_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Chaos_Unleashed/model.py", "Chaos_Unleashed")
        env = self.make_env()
        card = card_cls(env.p1)

        d1 = env.put_creatures(env.p1, "Fragile", 2, 2, 1)[0]
        d2 = env.put_creatures(env.p2, "Fragile Two", 2, 2, 1)[0]
        env.p1.life = 15
        env.p2.life = 15

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 12)
        self.assertEqual(env.p2.life, 12)
        self.assertEqual(env.card_zone(d1), "graveyard")
        self.assertEqual(env.card_zone(d2), "graveyard")

    async def test_chaos_unleashed_no_creatures_only_hits_players(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Chaos_Unleashed/model.py", "Chaos_Unleashed")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 20
        env.p2.life = 20
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 17)
        self.assertEqual(env.p2.life, 17)
        self.assertFalse(env.p1.battlefield)
        self.assertFalse(env.p2.battlefield)
