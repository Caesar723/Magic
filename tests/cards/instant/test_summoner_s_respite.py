from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSummoner_s_Respite(CardTestCaseBase):
    async def test_summoner_s_respite_gains_life_and_buffs_team(self):
        card_cls = load_card_class_from_path("pycards/Instant/Summoner_s_Respite/model.py", "Summoner_s_Respite")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.p1.life = 10
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 14)
        self.assertGreaterEqual(creature.state[0], 3)
        self.assertGreaterEqual(creature.state[1], 3)
        self.assertEqual(env.p2.life, 20)

    async def test_summoner_s_respite_gains_life_with_no_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Summoner_s_Respite/model.py", "Summoner_s_Respite")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.life = 8
        self.assertEqual(len(env.p1.battlefield), 0)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 12)
        self.assertEqual(len(env.p1.battlefield), 0)

    async def test_summoner_s_respite_does_not_buff_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Summoner_s_Respite/model.py", "Summoner_s_Respite")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]
        b0, b1 = foe.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(foe.state, (b0, b1))
