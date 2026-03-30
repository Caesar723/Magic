from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCataclysmic_Surge(CardTestCaseBase):
    async def test_cataclysmic_surge_damages_players_and_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Cataclysmic_Surge/model.py", "Cataclysmic_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 6, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy C", 2, 6, 1)[0]
        env.p1.life = 10
        env.p2.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 5)
        self.assertEqual(env.p2.life, 5)
        self.assertEqual(c1.state[1], 1)
        self.assertEqual(c2.state[1], 1)

    async def test_cataclysmic_surge_no_creatures_only_players_take_damage(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Cataclysmic_Surge/model.py", "Cataclysmic_Surge")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 20
        env.p2.life = 20
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 15)
        self.assertEqual(env.p2.life, 15)

    async def test_cataclysmic_surge_only_opponent_creature_still_hits_both_players_for_five(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Cataclysmic_Surge/model.py", "Cataclysmic_Surge")
        env = self.make_env()
        card = card_cls(env.p1)
        tank = env.put_creatures(env.p2, "Enemy Tank", 2, 6, 1)[0]
        env.p1.life = 20
        env.p2.life = 20

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 15)
        self.assertEqual(env.p2.life, 15)
        self.assertEqual(tank.state[1], 1)
        self.assertEqual(len(env.p1.battlefield), 0)
