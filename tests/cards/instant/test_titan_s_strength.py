from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTitan_s_Strength(CardTestCaseBase):
    async def test_titan_s_strength_buffs_all_your_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Titan_s_Strength/model.py", "Titan_s_Strength")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Ally One", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p1, "Ally Two", 3, 3, 1)[0]
        b1, b2 = c1.state, c2.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(c1.state, (b1[0] + 4, b1[1] + 4))
        self.assertEqual(c2.state, (b2[0] + 4, b2[1] + 4))
        self.assertTrue(c1.get_flag("Trample"))
        self.assertTrue(c2.get_flag("Trample"))

    async def test_titan_s_strength_resolves_with_empty_battlefield(self):
        card_cls = load_card_class_from_path("pycards/Instant/Titan_s_Strength/model.py", "Titan_s_Strength")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.battlefield.clear()
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), 0)

    async def test_titan_s_strength_does_not_buff_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Titan_s_Strength/model.py", "Titan_s_Strength")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(foe.state, (2, 2))
        self.assertFalse(foe.get_flag("Trample"))
