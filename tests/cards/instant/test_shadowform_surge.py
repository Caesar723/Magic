from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestShadowform_Surge(CardTestCaseBase):
    async def test_shadowform_surge_applies_minus_three_minus_three(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadowform_Surge/model.py", "Shadowform_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Surge Target", 3, 3, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(target, {"buffs_contains": ["StateBuff"]})

    async def test_shadowform_surge_can_kill_small_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadowform_Surge/model.py", "Shadowform_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        victim = env.put_creatures(env.p2, "Small Target", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(victim), "battlefield")

    async def test_shadowform_surge_requires_opponent_creature_target(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadowform_Surge/model.py", "Shadowform_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Only Ally", 3, 3, 1)
        result = await env.play_card(card, env.p1)

        self.assertFalse(result[0])
