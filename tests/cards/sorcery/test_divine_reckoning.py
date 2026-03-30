from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDivine_Reckoning(CardTestCaseBase):
    async def test_divine_reckoning_destroys_non_angels_and_grants_life(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Reckoning/model.py", "Divine_Reckoning")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy C", 2, 2, 1)[0]
        env.p1.life = 10
        env.p2.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(c1), "graveyard")
        self.assertEqual(env.card_zone(c2), "graveyard")
        self.assertEqual(env.p1.life, 11)
        self.assertEqual(env.p2.life, 11)
        self.assertEqual(len(env.p2.exile_area), 0)

    async def test_divine_reckoning_spares_angel_type_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Reckoning/model.py", "Divine_Reckoning")
        env = self.make_env()
        card = card_cls(env.p1)

        angel = env.create_creature(env.p1, "Test Angel", 3, 3)
        angel.type_creature = "Angel"
        env.put_on_battlefield(angel, env.p1)
        fodder = env.put_creatures(env.p2, "Enemy C", 2, 2, 1)[0]
        env.p1.life = 10
        env.p2.life = 10
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(angel), "battlefield")
        self.assertEqual(env.card_zone(fodder), "graveyard")
        self.assertEqual(env.p1.life, 10)
        self.assertEqual(env.p2.life, 11)

    async def test_divine_reckoning_only_angels_no_destroys_no_life_gain(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Reckoning/model.py", "Divine_Reckoning")
        env = self.make_env()
        card = card_cls(env.p1)
        a1 = env.create_creature(env.p1, "A1", 2, 2)
        a1.type_creature = "Angel"
        a2 = env.create_creature(env.p2, "A2", 2, 2)
        a2.type_creature = "Angel"
        env.put_on_battlefield(a1, env.p1)
        env.put_on_battlefield(a2, env.p2)
        env.p1.life = 15
        env.p2.life = 16

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(a1), "battlefield")
        self.assertEqual(env.card_zone(a2), "battlefield")
        self.assertEqual(env.p1.life, 15)
        self.assertEqual(env.p2.life, 16)
