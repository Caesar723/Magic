from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTitan_Giant(CardTestCaseBase):
    async def test_titan_giant_etb_destroys_other_small_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Titan_Giant/model.py", "Titan_Giant")
        env = self.make_env()
        card = card_cls(env.p1)

        friendly_small = env.put_creatures(env.p1, "Friendly Small", 2, 2, 1)[0]
        friendly_big = env.put_creatures(env.p1, "Friendly Big", 6, 6, 1)[0]
        enemy_small = env.put_creatures(env.p2, "Enemy Small", 3, 3, 1)[0]
        enemy_big = env.put_creatures(env.p2, "Enemy Big", 6, 6, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        titan = env.get_battlefield_creature(env.p1, "Titan Giant")
        self.assert_state(titan, {"zone": "battlefield", "state": (8, 8)})
        self.assertEqual(env.card_zone(friendly_small), "graveyard")
        self.assertEqual(env.card_zone(enemy_small), "graveyard")
        self.assertEqual(env.card_zone(friendly_big), "battlefield")
        self.assertEqual(env.card_zone(enemy_big), "battlefield")

    async def test_titan_giant_preserves_five_power_creatures(self):
        """ETB destroys only creatures with power strictly less than 5."""
        card_cls = load_card_class_from_path("pycards/creature/Titan_Giant/model.py", "Titan_Giant")
        env = self.make_env()
        card = card_cls(env.p1)
        five = env.put_creatures(env.p1, "Five Power", 5, 5, 1)[0]
        four = env.put_creatures(env.p2, "Four Power", 4, 4, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(five), "battlefield")
        self.assertEqual(env.card_zone(four), "graveyard")

    async def test_titan_giant_etb_with_empty_board_only_enters(self):
        card_cls = load_card_class_from_path("pycards/creature/Titan_Giant/model.py", "Titan_Giant")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        titan = env.get_battlefield_creature(env.p1, "Titan Giant")
        self.assert_state(titan, {"zone": "battlefield", "state": (8, 8)})
        self.assertFalse(env.p2.battlefield)
