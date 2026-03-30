from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEphemeral_Eruption(CardTestCaseBase):
    async def test_ephemeral_eruption_deals_four_to_each_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Ephemeral_Eruption/model.py", "Ephemeral_Eruption")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 5, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy C", 2, 5, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(c1.state[1], 1)
        self.assertEqual(c2.state[1], 1)

    async def test_ephemeral_eruption_no_creatures_resolves(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Ephemeral_Eruption/model.py", "Ephemeral_Eruption")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertFalse(env.p1.battlefield)
        self.assertFalse(env.p2.battlefield)

    async def test_ephemeral_eruption_lethal_creature_moves_to_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Ephemeral_Eruption/model.py", "Ephemeral_Eruption")
        env = self.make_env()
        card = card_cls(env.p1)
        doomed = env.put_creatures(env.p2, "Doomed", 1, 3, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(doomed), "graveyard")

    async def test_ephemeral_eruption_player_life_totals_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Ephemeral_Eruption/model.py", "Ephemeral_Eruption")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "A", 2, 5, 1)
        env.put_creatures(env.p2, "B", 2, 5, 1)
        p1l, p2l = env.p1.life, env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1l)
        self.assertEqual(env.p2.life, p2l)
