from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRighteous_Conviction(CardTestCaseBase):
    async def test_righteous_conviction_buffs_and_grants_lifelink(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Righteous_Conviction/model.py", "Righteous_Conviction")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Chosen", 2, 2, 1)[0]
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state, (before[0] + 2, before[1] + 2))
        self.assertTrue(target.get_flag("lifelink"))

    async def test_righteous_conviction_buffs_expire_after_end_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Righteous_Conviction/model.py", "Righteous_Conviction")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p1, "Chosen", 2, 2, 1)[0]
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state, (before[0] + 2, before[1] + 2))
        for buff in list(target.buffs):
            buff.when_end_turn()
        self.assertEqual(target.state, before)
        self.assertFalse(target.get_flag("lifelink"))

    async def test_righteous_conviction_opponent_creature_unbuffed(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Righteous_Conviction/model.py", "Righteous_Conviction")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Friendly", 2, 2, 1)
        enemy = env.put_creatures(env.p2, "Enemy", 3, 3, 1)[0]
        before = enemy.state
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(enemy.state, before)
        self.assertFalse(enemy.get_flag("lifelink"))
