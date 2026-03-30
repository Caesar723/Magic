from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSacred_Reinforcement(CardTestCaseBase):
    async def test_sacred_reinforcement_taps_two_enemy_creatures_and_buffs(self):
        card_cls = load_card_class_from_path("pycards/Instant/Sacred_Reinforcement/model.py", "Sacred_Reinforcement")
        env = self.make_env()
        card = card_cls(env.p1)

        e1 = env.put_creatures(env.p2, "Enemy A", 2, 2, 1)[0]
        e2 = env.put_creatures(env.p2, "Enemy B", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(e1.get_flag("tap") or e2.get_flag("tap"))
        self.assertTrue(e1.state[0] >= 3 or e2.state[0] >= 3)

    async def test_sacred_reinforcement_single_target_when_only_one_enemy(self):
        card_cls = load_card_class_from_path("pycards/Instant/Sacred_Reinforcement/model.py", "Sacred_Reinforcement")
        env = self.make_env()
        card = card_cls(env.p1)

        e1 = env.put_creatures(env.p2, "Enemy Solo", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(e1.get_flag("tap"))
        self.assertGreaterEqual(e1.state[0], 3)

    async def test_sacred_reinforcement_does_not_tap_friendly_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Sacred_Reinforcement/model.py", "Sacred_Reinforcement")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.put_creatures(env.p2, "Enemy", 2, 2, 1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertFalse(ally.get_flag("tap"))
