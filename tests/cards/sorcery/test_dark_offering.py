from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDark_Offering(CardTestCaseBase):
    async def test_dark_offering_opponent_loses_two_you_gain_two(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Dark_Offering/model.py", "Dark_Offering")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.life = 10
        env.p2.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 12)
        self.assertEqual(env.p2.life, 8)
        self.assertEqual(len(env.p2.battlefield), 0)

    async def test_dark_offering_can_reduce_opponent_below_starting_life(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Dark_Offering/model.py", "Dark_Offering")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.life = 5
        env.p2.life = 3

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, 1)
        self.assertEqual(env.p1.life, 7)

    async def test_dark_offering_does_not_change_creature_board_presence(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Dark_Offering/model.py", "Dark_Offering")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        env.put_creatures(env.p2, "Foe", 2, 2, 1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), 1)
        self.assertEqual(len(env.p2.battlefield), 1)
